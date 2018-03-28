From https://gist.github.com/eddies/f37d696567f15b33029277ee9084c4a0

if $SPARK_HOME/conf/spark-defaults.conf does not exist, create a copy from $SPARK_HOME/conf/spark-defaults.conf.template

In $SPARK_HOME/conf/spark-defaults.conf include:

spark.jars.packages                com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.2

$SPARK_HOME/conf/hdfs-site.xml

<?xml version="1.0"?>
<configuration>
<property>
  <name>fs.s3a.access.key</name>
  <value>YOUR_KEY_HERE</value>
</property>
<property>
  <name>fs.s3a.secret.key</name>
  <value>YOUR_SECRET_HERE</value>
</property>
<property>
  <name>fs.s3n.awsAccessKeyId</name>
  <value>YOUR_KEY_HERE </value>
</property>
<property>
  <name>fs.s3n.awsSecretAccessKey</name>
  <value> YOUR_SECRET_HERE </value>
</property>
</configuration>



Things that also worked but were less optimal

Calling pyspark with --packages argument:

pyspark --packages com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.2

Defining AWS credentials in code, e.g.:

sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "YOUR_KEY_HERE")
sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "YOUR_SECRET_HERE")

Actually, for credentials, I had to:
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=


Main: 47, -68
Florida: 25, -80
Washington State: 49, -123
California: 33, -117


dataframe
  .write
    .mode(SaveMode.Append)
      .partitionBy("year", "month", "date", "country", "predicate")
        .parquet(outputPath)

https://stackoverflow.com/questions/33823172/how-to-control-number-of-parquet-files-generated-when-using-partitionby
