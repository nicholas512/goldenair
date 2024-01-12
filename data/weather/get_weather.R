library(weathercan)


stn <- stations_search(coords = c(51.2961, -116.9631), dist=20)

# 54318 52980 1364 

df <- weather_dl(c(54318,52980,1364), start="2010-01-01", end="2024-01-01", interval="hour")

write.csv(df, "C:\\Users\\Nick\\src\\goldenair\\data\\weather\\meteo.csv")
golden_meteo <- df
save(golden_meteo, file="C:\\Users\\Nick\\src\\goldenair\\data\\weather\\meteo.R")
