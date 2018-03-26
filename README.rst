if $SPARK_HOME/conf/spark-defaults.conf does not exist, create a copy from $SPARK_HOME/conf/spark-defaults.conf.template

In $SPARK_HOME/conf/spark-defaults.conf include:

spark.jars.packages                com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.2

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
