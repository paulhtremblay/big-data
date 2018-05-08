"""BigQuery I/O PySpark example."""
from __future__ import absolute_import
import json
import pprint
import subprocess
import pyspark
from pyspark.sql import SQLContext

sc = pyspark.SparkContext()
