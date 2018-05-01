library("ggplot2")
library("tidyr")
data <- read.csv("perm_data/index_inner_join.csv")
df_index <- subset(data, type=="index")
df_index <- df_index[c("num_rows", "time")]
constant <- mean(df_index$time/(df_index$num_rows * log(df_index$num_rows)))
df_index$fitted <- constant * df_index$num_rows  * log(df_index$num_rows)
colnames(df_index) <- c("num_rows", "actual", "fitted")
df_tidy <- gather(df_index, type, time, -num_rows)
print(df_tidy)
ggplot(data = df_tidy, aes(x=num_rows, y= time, color = type)) + 
	geom_line() + 
	ggtitle("Index") +  
	ylab("time in seconds") + 
	scale_x_continuous(name="number rows", labels = scales::comma)
ggsave("data_out/index.png")

