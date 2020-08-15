import os
import mysql.connector
PW = os.environ['MYSQL_GCP_PW']

cnx = mysql.connector.connect(user='root', password=PW,
        
                              host='34.70.55.50',
                              database='henry1')
cnx.close()
