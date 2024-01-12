library(ecdf)

load("C:\\Users\\Nick\\src\\goldenair\\data\\weather\\meteo.R")

golden_a <- golden_meteo[golden_meteo$station_id == 52980,]
t_max <- 10
cooling_hours <- golden_a[golden_a$temp < t_max,]  # hours with T < t_max

E <- ecdf(cooling_hours$temp)
cutoffs <- list(-10,-5)
p_cuts <- lapply(cutoffs, function(cut) round(E(cut) * 100,0))
names(p_cuts) <- cutoffs


get_y <- function(H, cutoff){
  i <- which.min(abs(H$mids - cutoff))
  y <- H$density[i] * 1.4
  return(y)
}

par(mfrow=c(1,2))

H <- hist(cooling_hours$temp, 
     breaks=seq(min(cooling_hours$temp, na.rm=T), t_max, 1),
     freq=F, 
     ylab="probability",
     main="% heating hours below cutoff temperature",
     xlab="Hourly Air Temperature")

lapply(cutoffs, function(t) abline(v=t, col='red', lty=2))
lapply(seq_along(cutoffs),
       function(i) text(x=cutoffs[[i]],
                        y=get_y(H, cutoffs[[i]]),
                        paste0(p_cuts[i],"%"), 
                        srt=90)
       )

plot(E, main="Hourly Air Temperature ECDF", ylab="P(t <= T)", xlab="Hourly Air Temperature")
lapply(cutoffs, function(t) abline(v=t, col='red', lty=2))
