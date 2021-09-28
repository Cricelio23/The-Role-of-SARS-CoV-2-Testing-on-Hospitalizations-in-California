# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 16:44:11 2021
@author: crice
"""
import pandas as pd
from os import getcwd
import numpy as np
from datetime import date,timedelta
# work directory
path = getcwd() + "/"
#  Daily reported cases
data_Testing = pd.read_csv(path+"covid19cases_test.csv")
# Daily hospitalization admissions
data = pd.read_csv(path+"covid19hospitalbycounty.csv")
# Demographics variables
Demographics = pd.read_excel(path+"Demographics-CA-Counties.xlsx",sheet_name="Per_among_county_pop")
Demographics.index = Demographics.county
data = data.rename(columns={'todays_date': 'date'})
data_Testing = data_Testing.rename(columns={'area': 'county'})

# Remove rows with nan dates
data_Testing.dropna(subset = ["date"], inplace=True)
#data.dropna(subset = ["date"], inplace=True)

county_all = ['Alameda', 'Amador', 'Butte','Contra Costa',
    'El Dorado', 'Fresno', 'Humboldt', 'Imperial',
    'Kern', 'Kings', 'Lake', 'Los Angeles', 'Madera',
   'Marin', 'Mendocino', 'Merced', 'Monterey',
   'Napa', 'Nevada', 'Orange', 'Placer', 'Riverside',
   'Sacramento', 'San Bernardino', 'San Diego',
   'San Francisco', 'San Joaquin', 'San Luis Obispo', 'San Mateo',
   'Santa Barbara', 'Santa Clara', 'Santa Cruz', 'Shasta',
   'Solano', 'Sonoma', 'Stanislaus', 'Tehama', 'Tulare', 'Tuolumne',
   'Ventura', 'Yolo', 'Yuba']
# Wave to analize    
wave = 3
if wave==1:
    # Mobility Reports
    data_mob = pd.read_csv(path+"mob_google_county_wave_1_.csv")
    date_ini = '2020-04-21'
    date_end = '2020-09-30'
elif wave==2:
    data_mob = pd.read_csv(path+"mob_google_county_wave_2_.csv")
    date_ini = '2020-10-01'
    date_end = '2021-02-28'
else:
    data_mob = pd.read_csv(path+"mob_google_county_wave_3_.csv")
    date_ini = '2021-03-01'
    date_end = '2021-09-05' 

# Lag between positivity rate and hospitalization
lag = 14
date_ini_T = str(date.fromisoformat(date_ini) - timedelta(days=lag))
date_end_T = str(date.fromisoformat(date_end) - timedelta(days=lag))

dataHos = data[(data["date"] >= date_ini) & (data["date"] <= date_end)]
dataTes = data_Testing[(data_Testing["date"] >= date_ini_T) & (data_Testing["date"] <= date_end_T)]

# We consider cases per 10k inhabitants
k = 10000.0
#We select only the variables to analyze
population = dataTes[["county","population"]]
population["population_std"]= population.population / population.population.max()

dataTes = dataTes[["date","county","cases","total_tests"]]
dataHos = dataHos[["date","county","hospitalized_covid_confirmed_patients","all_hospital_beds"]]


Data_all = pd.DataFrame({})#,columns=var_names)
ii = 0
cou_i = 1
for county in county_all:
    data_test_i = dataTes[data_Testing.county==county]
    data_hosp_i = dataHos[dataHos.county==county]
    #data_test_i["Rate"] = data_test_i.cases/data_test_i.total_tests
    data_test_i.index = pd.to_datetime(data_hosp_i.date)
    data_hosp_i.index = pd.to_datetime(data_hosp_i.date)
    
    # Gruped by date weekly
    test = data_test_i.groupby(pd.Grouper(freq="W")).mean() # Cambiar a mean
    hosp = data_hosp_i.groupby(pd.Grouper(freq="W")).mean()
    
    pop = population.population[population.county==county].values[0]
    pop_std= population.population_std[population.county==county].values[0]
    test["population"] = pop
    test["Cases_10k"] = k*test.cases/pop
    test["Test_10k"] = k*test.total_tests/pop
    test["Rate"] = test.cases/test.total_tests
    hosp["Hosp_10k"] = k*hosp.hospitalized_covid_confirmed_patients/pop
    hosp["beds_10k"] = k*hosp.all_hospital_beds/pop
    if sum(test.cases==0.)>1:
        ii+=1
        print("nulos caso")
    #if sum(test.total_tests==0.)==0:
    if (sum(test.total_tests==0.)<1)&(sum(test.cases==0.)<20):
        Data_full = pd.merge_ordered(test,hosp,on= ["date"])
        Data_full["Week"] = np.arange(len(hosp))#/len(hosp)
        Data_full["county"] = county
        Data_full['Male'] =  Demographics.loc[county].Male
        Data_full["Hispanic"] = Demographics.loc[county].Hispanic_or_Latino
        Data_full["Over_65"] = Demographics.loc[county].Over_65
        Data_full["Over_85"] = Demographics.loc[county].Over_85
        Data_full["White"] = Demographics.loc[county].White
        Data_full["Asian"] = Demographics.loc[county].Asian
        Data_full["HPI"] = Demographics.loc[county].HPI
        Data_full["anycondition"] = Demographics.loc[county].anycondition_prevalence
        Data_full["Obesity"] = Demographics.loc[county].Obesity_prevalence
        Data_full["Heart_disease"] = Demographics.loc[county].Heart_disease_prevalence 
        Data_full["COPD"] = Demographics.loc[county].COPD_prevalence
        Data_full["diabetes"] = Demographics.loc[county].diabetes_prevalence
        Data_full["CKD"] = Demographics.loc[county].CKD_prevalence
        Data_full["Urban_rural"] = Demographics.loc[county].Urban_rural_code
        Data_full["Morenitos"] = Demographics.loc[county].Black_or_African_American
        Data_full["C_i"] = cou_i
        Data_full["pop_std"] = pop_std
        Data_full["mobility"] = 100*data_mob[county]
        Data_all = pd.concat([Data_all, Data_full], ignore_index=True)
        cou_i +=1 
    else:
        continue
Data_all.to_csv(path+"base_10k_wave_%s.csv"%wave,index=False)

