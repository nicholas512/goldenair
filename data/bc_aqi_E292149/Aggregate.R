library(lubridate)

rootdir <- "C:\\Users\\Nick\\src\\goldenair\\data\\bc_aqi_E292149"
output_aggregated <- file.path(rootdir, "aggregated.csv")

csv_files <- list.files(rootdir, pattern=".*csv", full.names = TRUE)
csv_files <- csv_files[grepl("[0-9]{4}.csv", csv_files) | 
                       grepl("E292149_unverified", csv_files)  ]


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

agg_21_onward <- do.call(rbind, df_list[10])[,matching_cols]


all <- do.call(rbind, list(agg_13_16, agg_17_19, agg_20, agg_21, agg_21_onward))


write.csv(all, output_aggregated, row.names=F)

