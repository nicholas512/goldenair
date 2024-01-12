library(openair)
library(data.table)
library(lubridate)

df <- data.table::fread("C:\\Users\\Nick\\src\\goldenair\\data\\aggregated_long.csv")
df <- read.csv("C:\\Users\\Nick\\src\\goldenair\\data\\aggregated_long.csv")
df$time <- as_datetime(df$time)
parson<- df[df$station == 47891 ,]

names(parson)[1] <- "date"
parson$wind_dir = parson$wind_dir * 10
parson$wd <- parson$wind_dir
parson$ws <- parson$wind_spd
parson <- parson[month(parson$date) %in% c(10,11,12,1,2,3),]

## openair
windRose(parson)

pollutionRose(parson, pollutant = "pm2.5_alt")

polarFreq(parson, pollutant = "pm2.5_alt", 
          statistic = "mean", 
          min.bin = 2)


polarFreq(parson, pollutant = "pm2.5_alt", 
          statistic = "weighted.mean", 
          min.bin = 2)



