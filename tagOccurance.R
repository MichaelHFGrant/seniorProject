#! /usr/bin/Rscript
args = commandArgs(trailingOnly= TRUE)
library(RSQLite)
print(args)
con <- dbConnect(RSQLite::SQLite(),"database/csci491")
query <- paste0("select siteID from websiteSamples WHERE testID = ",args[1])
siteIDs = c(dbGetQuery(con,query))
print(siteIDs)
for (i in 1:length(siteIDs)){
   query <- paste0("select pageID from webpages where siteID = ",siteIDs[[i]])
   pageIDs <-c(dbGetQuery(con,query))
   for(x in 1:length(pageIDs)){
      innerQuery <- paste0("select count from tagCount WHERE pageID = ", pageIDs[[x]]," and  tag = '",args[2],"'")
      tagCount <- dbGetQuery(con,innerQuery[[x]])
      print(pageIDs[[x]])
      print(tagCount[[x]])
   }
}
var = dbGetQuery(con,"select SUM(count) FROM tagCount GROUP BY pageID")
query <- paste0("select pageID from webpages where siteID = ",siteIDs[[1]])
