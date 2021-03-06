# The Role of SARS-CoV-2 Testing on Hospitalizations in California

## Data
Epidemiological data.  Publicly available information of COVID-19 regarding daily reported cases (covid19cases_test.csv) and hospitalization admissions (covid19hospitalbycounty.csv) at county-level was obtained from the official website of the California Department of Public Health (CDPH) [1]. The hospitalized data are not a cumulative number. Data includes all inpatients (including those in ICUs and Medical/Surgical units) and does not include patients in affiliated clinics, outpatient departments, emergency departments, and overflow locations awaiting an inpatient bed. As of April 21, 2020, COVID emergency department patients were removed from the Hospitalized COVID count and counted separately.
 
The Demographics-CA-Counties.xlsx file contains:
- Demographic characteristics such as age, ethnicity, and race by county reported by the United State Census Bureau [2].
- The California Healthy Place Index [3]. This value combines twenty-five community characteristics  (the number of people living below the poverty line, the number of people with lower levels of education, areas with more renters and fewer homeowners, among others.) into a single value (HPI) to account for the level of poverty, education, and life expectancy in a particular community. 

Google’s Community Mobility Reports [4]. The six Google-specific data streams, gro-cery  and  pharmacy,  parks,  residential,  retail  and  recreation,  transit  stations,  andworkplaces were combined to obtain a single county mobility measure using an un-supervised machine learning method known as principal component analysis (PCA) for each wave: 
mob_google_county_wave_1_.csv, mob_google_county_wave_2_.csv, and mob_google_county_wave_3_.csv.

## Codes
- With file Create_Data.py the databases to be analyzed in each wave are created, to have the data on a weekly level.
- The file Fitting_Linear_Mixed_Effects_Models.R contains the code that reads the data created with Create_Data.py and fits the linear mixed effects model using the lme4 library.

## References
[1] Californial Department of Public Health.  Covid-19 time-series metrics by county andstate - datasets - california health and human services open data portal. https://data.chhs.ca.gov/dataset/covid-19-time-series-metrics-by-county-and-state. (Accessed on 09/16/2021).

[2] 2019 data profiles — american community survey — us census bureau. https://www.census.gov/acs/www/data/data-tables-and-tools/data-profiles/. (Accessed on 09/16/2021).

[3] The  California  Healthy  Places  Index  (HPI). Data  &  reports – california  healthyplaces index. https://healthyplacesindex.org/data-reports/. (Accessed  on 09/16/2021)

[4] COVID-19 Community Mobility Reports.  Google (2020). https://www.google.com/covid19/mobility/. (Accessed on 11/09/2021).
