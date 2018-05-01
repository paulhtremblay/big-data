library("ggplot2")
library("tidyr")
data <- read.csv("perm_data/index_inner_join.csv")
df_no_index <- subset(data, type=="no index")
df_no_index <- df_no_index[c("num_rows", "time")]
constant <- median(df_no_index$time/df_no_index$num_rows ^2)
df_no_index$fitted <- constant * df_no_index$num_rows ^2
colnames(df_no_index) <- c("num_rows", "actual", "fitted")
df_tidy <- gather(df_no_index, type, time, -num_rows)
ggplot(data = df_tidy, aes(x=num_rows, y= time, color = type)) + 
	geom_line() + 
	ggtitle("No Index") +  
	ylab("time in seconds") + 
	scale_x_continuous(name="number rows", labels = scales::comma)
ggsave("data_out/no_index.png")

