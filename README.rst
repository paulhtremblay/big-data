if $SPARK_HOME/conf/spark-defaults.conf does not exist, create a copy from $SPARK_HOME/conf/spark-defaults.conf.template

In $SPARK_HOME/conf/spark-defaults.conf include:

spark.jars.packages                com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.2

