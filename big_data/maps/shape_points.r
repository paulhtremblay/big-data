library(rgdal)
library(ggplot2)
#shape file
sh <- readOGR("/tmp/shapes/CA_State_TIGER2016.shp")
#sh_df <- fortify(sh)
points <- data.frame(lat=c(37), long = c(-120))
coordinates(points) <-~long+lat
proj4string(points)<-CRS("+proj=longlat +datum=NAD83")
points <- spTransform(points, CRS(proj4string(sh)))
identical(proj4string(sh), proj4string(points))
points <- data.frame(points)
map<-ggplot() + geom_polygon(data = sh, aes(x=long, y=lat, group = group)) + geom_point(data= points, aes(x=long, y = lat), color="red")
ggsave('file.png', plot=map)
