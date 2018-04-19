import pprint
pp = pprint.PrettyPrinter(indent = 4)
a = ['Accident_Index', 'Location_Easting_OSGR', 'Location_Northing_OSGR', 'Longitude', 'Latitude', 'Police_Force', 'Accident_Severity', 'Number_of_Vehicles', 'Number_of_Casualties', 'Date', 'Day_of_Week', 'Time', 'Local_Authority_(District)', 'Local_Authority_(Highway)', '1st_Road_Class', '1st_Road_Number', 'Road_Type', 'Speed_limit', 'Junction_Detail', 'Junction_Control', '2nd_Road_Class', '2nd_Road_Number', 'Pedestrian_Crossing-Human_Control', 'Pedestrian_Crossing-Physical_Facilities', 'Light_Conditions', 'Weather_Conditions', 'Road_Surface_Conditions', 'Special_Conditions_at_Site', 'Carriageway_Hazards', 'Urban_or_Rural_Area', 'Did_Police_Officer_Attend_Scene_of_Accident', 'LSOA_of_Accident_Location\n']

b = ['201501BS70001', '525130', '180050', '-0.198465', '51.505538', '1', '3', '1', '1', '12/01/2015', '2', '18:45', '12', 'E09000020', '5', '0', '6', '30', '3', '4', '6', '0', '0', '0', '4', '1', '1', '0', '0', '1', '1', 'E01002825\n']

f = []
for counter, item in enumerate(a):
    f.append((item.lower(), b[counter]))

pp.pprint(f)
