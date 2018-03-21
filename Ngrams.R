#! /usr/bin/Rscript
args = commandArgs(trailingOnly= TRUE)
library(RSQLite)
N <- args[3]
siteID = args[2]
con <- dbConnect(RSQLite::SQLite(),"database/csci491")
query = paste0("select pageID from webpages where siteID =",siteID)
pageIDs = dbGetQuery(con,query)
page.data <- data.frame()

for (i in 1:length(pageIDs$pageID)){
   query <- paste0("select pageID, Ngram,  tagString, count From Ngrams where pageID = ",pageIDs$pageID[[i]])
   data = dbGetQuery(con,query)
   page.data <- rbind(page.data,data)
}
print(length(page.data$tagString))
tagString <- unique(page.data$tagString)

print(length(tagString))
print(names(page.data))
Ngram <- page.data[page.data$tagString == "<a",]
temp.list <- list()
tag.data <- matrix(numeric(0),nrow=length(tagString), ncol =length(pageIDs$pageID))
rownames(tag.data) <- tagString
colnames(tag.data) <- pageIDs$pageID
print(typeof(tag.data[1,1]))
for (i in 1:length(pageIDs$pageID)){
   for (x in 1:length(tagString)){
      temp <- page.data[page.data$tagString == tagString[[x]] & page.data$pageID == pageIDs$pageID[[i]],]
#      print(temp$count)
 #     print(1 + numeric(temp$count))
      count <- tag.data[x,i]+ temp$count
#      print(typeof(count))
#      print(typeof(tag.data[x,i]))
  #    tag.data[x,i] <- "anythhine"
      
   }
}
#print(tag.data)










#names(temp.list) <- pageIDs$pageID
#tag.data <- data.frame(tagString,temp.list)
#print(tag.data)
#temp <- page.data[page.data$tagString == "<a",]
#print(temp)
#page <- as.list(paste0("X",temp$pageID))
#print(page)

#print(tag.data[tag.data$page[[1]] ==0 & tag.data$tagString == "<a",])






#print(tag.data[tag.data$var == 0 & tag.data$tagString == "<a",])
#for (i in 1:length(temp)){
 #  print(temp[[i]])
#}
#print(tag.data[tag.data$X23 == 0 & tag.data$tagString == "<a",])








#for (i in 1:length(tagString)){
#   print(page.data[page.data$tagString == tagString[[i]],])
#   print(tag.data[tag.data$tagString == tagString[[i]],tag.data$c(page.data$pageID],)
#    print(page.data[page.data$pageID == 23,])
#}












#query = paste0("select  Ngrams.pageID, tagString,count from  Ngrams,webpages Where siteID =" ,#siteID)
#data <- c(dbGetQuery(con,query))
#print(data$pageID)
#pages <- split(data,f = data$pageID)
#print(names(npages))
#print(pages[[1]])
#print(names(var))
#print(var$pageID)
#dotchart(var$count)


#var = dbGetQuery(con,"select SUM(count) FROM tagCount GROUP BY pageID")
#query <- paste0("select pageID from webpages where siteID = ",siteIDs[[1]])
