#rm(list=ls())
library(tidyverse)
library(lme4)
library(lmerTest)

# Weve is the wave to analize (1, 2, or, 3)
wave = 2
data1 <- read.csv(sprintf("base_10k_wave_%s.csv",wave))
epsilon = .00000001
data <- data1 %>%
  mutate(county = as.factor(county),
         Urban_rural = as.factor(Urban_rural),
         Hosp_10k = Hosp_10k+epsilon,
         Rate = Rate+epsilon,
         log.hosp = log(Hosp_10k),
         log.Rate = log(Rate),
         HPI2 =as.factor(ifelse(HPI<25,1,ifelse(HPI<50,2,ifelse(HPI<75,3,4)))))

# Fitting Linear Mixed-Effects Models Using lme4
fit_ran <- lmer(log.hosp~ Over_65+Asian+Hispanic+Morenitos+HPI+
                  mobility+Week+log.Rate+(log.Rate|county), data = data)

summary(fit_ran)
# To interpretate the coefficients
epx = function(x){100*(exp(x)-1)}
nr = 3
pastM = function(x1,x2,x3,x4){
  x2 = round(x2,nr)
  x3 = round(x3,nr)
  paste(paste(x1,x2,sep=""),paste(x3,x4,sep=""),sep=",")
}
# Fixed effects estimates
est = summary(fit_ran)$coefficients
# Interpretation with log response
est[2:8,"Estimate"] = 100*(exp(est[2:8,"Estimate"])-1)
IC = confint(fit_ran)
IC[6:12,1] = epx(IC[6:12,1])
IC[6:12,2] = epx(IC[6:12,2])

Est. = paste(round(est[,1],nr),pastM("(",IC[5:13,1],IC[5:13,2],")"))
p_value = ifelse(est[,5]<0.001,"<0.001",round(est[,5],3))

# Random effects Coefficients
co = coef(fit_ran)$county 
RR = co[,"log.Rate"] # random slope stimate for log.Rate
namess= rownames(co)

# Fixed effect estimates
cbind(Est.,p_value)
# Random slope by county
data.frame(Wave1=RR,row.names=rownames(co))
