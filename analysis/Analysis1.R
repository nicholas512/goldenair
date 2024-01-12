library(lubridate)

rootdir <- "C:\\Users\\Nick\\src\\goldenair\\E292149"

csv_files <- list.files(rootdir, pattern=".*csv", full.names = TRUE)


try_open <- function(csv_file){

  tryCatch({
    df <- read.csv(csv_file)
    return(df)
  }, error = function (e) {return(NA)},
  finally = print(csv_file))
}

df_list <- lapply(csv_files, try_open)

df_list <- df_list[sapply(df_list, class) == 'data.frame']

matching_cols <- c("DATE_PST", "DATE", "TIME", "PM25", "PM10")

agg_13_16 <- do.call(rbind, df_list[1:4])[,matching_cols]

agg_17_19 <- do.call(rbind, df_list[5:7])[,matching_cols]

agg_20 <- do.call(rbind, df_list[8])[,matching_cols]

agg_21 <- do.call(rbind, df_list[9])[,matching_cols]



all <- do.call(rbind, list(agg_13_16, agg_17_19, agg_20, agg_21))

# end prep

#begin functions
gm_mean = function(x, na.rm=TRUE){
  exp(sum(log(x[x > 0]), na.rm=na.rm) / length(x))
}


# Define the lerp function
lerp <- function(a, b, c, d, x) {
  return(a + (x - c) * (b - a) / (d - c))
}


pm25_aqi <- function(pm25) {
  c <- floor(10 * pm25) / 10
  if (c < 0) {
    return(0)
  } else if (c < 12.1) {
    a <- lerp(0, 50, 0.0, 12.0, c)
  } else if (c < 35.5) {
    a <- lerp(51, 100, 12.1, 35.4, c)
  } else if (c < 55.5) {
    a <- lerp(101, 150, 35.5, 55.4, c)
  } else if (c < 150.5) {
    a <- lerp(151, 200, 55.5, 150.4, c)
  } else if (c < 250.5) {
    a <- lerp(201, 300, 150.5, 250.4, c)
  } else if (c < 350.5) {
    a <- lerp(301, 400, 250.5, 350.4, c)
  } else if (c < 500.5) {
    a <- lerp(401, 500, 350.5, 500.4, c)
  } else {
    a <- 500
  }
  return(round(a))
}

aqi_pm25 <- function(aqi) {
  a <- round(aqi)
  if (a < 0) {
    return(0)
  } else if (a <= 50) {
    c <- lerp(0.0, 12.0, 0, 50, a)
  } else if (a <= 100) {
    c <- lerp(12.1, 35.4, 51, 100, a)
  } else if (a <= 150) {
    c <- lerp(35.5, 55.4, 101, 150, a)
  } else if (a <= 200) {
    c <- lerp(55.5, 150.4, 151, 200, a)
  } else if (a <= 300) {
    c <- lerp(150.5, 250.4, 201, 300, a)
  } else if (a <= 400) {
    c <- lerp(250.5, 350.4, 301, 400, a)
  } else if (a <= 500) {
    c <- lerp(350.5, 500.4, 401, 500, a)
  } else {
    c <- 500
  }
  return(floor(10 * c) / 10)
}
# end functions

# begin analysis
all$DATE_PST <- as.POSIXct(all$DATE_PST, "%Y-%m-%d %H:%M:%S", tz="Canada/Pacific")

# 
plot(all$DATE_PST, all$PM25, type='l')
plot(all$DATE_PST, log(all$PM25), type='l')

winter <- all[month(all$DATE_PST) %in% c(10,11,12,1,2,3,4),]
winter_hourly_avg <- by(winter$PM25, winter$TIME, function(x) mean(x, na.rm=TRUE))
winter_hourly_sd <- by(winter$PM25, winter$TIME, function(x) sd(x, na.rm=TRUE))

plot(winter_hourly_avg, type='l', xaxt='n', xlab="", ylab='PM2.5', ylim=c(0,30), main="October - April mean hourly PM2.5")
axis(side=1, at=c(1:24), labels = names(winter_hourly_avg), las=2)
lines(winter_hourly_avg + winter_hourly_sd)
lines(winter_hourly_avg - winter_hourly_sd)


## Correlation with temperature

## day of week effect

##  wind direction effect

## cross-station correlation

##  