import arcpy
import io
import numpy
import pandas
import matplotlib.pyplot as plt

import os

#create a feature class polygon
#create a feature class with polygon
arcpy.management.CreateFeatureclass(r"C:\Users\laure\OneDrive\Documents\ArcGIS II Labs\Lab1\lab1.gdb", 'linked', 'POLYGON')
spatial_reference= arcpy.SpatialReference(4326)

linked = arcpy.Polygon(arcpy.Array([arcpy.Point(-93.32295119774095, 44.96157921686313), arcpy.Point(-93.30630004421299, 44.94888479428342), arcpy.Point(-93.30733001246776, 44.95265089674996)]), spatial_reference)

curs = arcpy.da.InsertCursor(os.path.join(r"C:\Users\laure\OneDrive\Documents\ArcGIS II Labs\Lab1\lab1.gdb", 'linked'), ['SHAPE@'])
curs.insertRow([linked])
del curs

linked

lakes_wkt = linked.WKT

lakes_wkt

import psycopg2
#which allows SQL in Jupyter

#establish the connection with the database in the server which is Google Cloud Console 
connection = psycopg2.connect(host='34.27.25.117',
                             database= 'lab0',
                             user='postgres',
                             password='gobadgers')

cursor = connection.cursor()

#create and populate table in my database
cursor.execute("CREATE TABLE IF NOT EXISTS lakestable (id SERIAL PRIMARY KEY, geom GEOMETRY)")
cursor.execute("INSERT INTO lakestable (geom) VALUES (ST_GeomFromText('{}', 4326))".format(linked.WKT))
connection.commit()
connection.close()
print("Table created and populated with my polygon")


