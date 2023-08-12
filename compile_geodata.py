# ------------
# program to clean and compile geodata
# TIGER shapefiles used from census.gov - state_raw and zip_raw in data/shapefiles
# cleaned poverty and population data used from census.gov - data/census_data.csv
# geodata exported to state_data and zip_data in data/shapefiles
# ------------

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import zipcodes

# --DOCTORS GEODATA

print('PROCESSING DOCTOR DATA')

# import doctor geodata
doctor_data = pd.read_csv('C:\\Users\\vikra\\NYU_2023\\data\\geo_doctors.csv')
df_doc = pd.DataFrame(doctor_data)

df_doc = df_doc[df_doc['Latitude'] != 'skip']

geometry = [Point(xy) for xy in zip(df_doc.Longitude, df_doc.Latitude)]
geo_doc = df_doc.drop(['Longitude', 'Latitude'], axis=1)
geodata_doc = gpd.GeoDataFrame(geo_doc, crs="EPSG:4326", geometry=geometry)
geodata_doc.to_file('data/shapefiles/doc_data/doc.shp')

# create zip and state df
doc_zip = df_doc['Zipcode'].value_counts()
doc_zip = pd.DataFrame(doc_zip)
doc_zip.reset_index(inplace=True)
doc_zip.rename(columns={'count': 'doc'}, inplace=True)

doc_state = df_doc['State'].value_counts()
doc_state = pd.DataFrame(doc_state)
doc_state.reset_index(inplace=True)
doc_state.rename(columns={'count': 'doc'}, inplace=True)

# add well-rated
df_subset = df_doc[df_doc['Number of Ratings'] > 5]
df_subset = df_subset[df_subset['Rating'] > 3]
subset = df_subset['Zipcode'].value_counts()
df_subset = pd.DataFrame(subset)
df_subset.reset_index(inplace=True)
df_subset.rename(columns={'count': 'rated'}, inplace=True)
doc_zip = doc_zip.merge(df_subset, how='left', left_on='Zipcode', right_on='Zipcode')

df_subset = df_doc[df_doc['Number of Ratings'] > 5]
df_subset = df_subset[df_subset['Rating'] > 3]
subset = df_subset['State'].value_counts()
df_subset = pd.DataFrame(subset)
df_subset.reset_index(inplace=True)
df_subset.rename(columns={'count': 'rated'}, inplace=True)
doc_state = doc_state.merge(df_subset, how='left', left_on='State', right_on='State')

# add accepts-medicaid
df_subset = df_doc[df_doc['Accepts Medicaid'] == True]
subset = df_subset['Zipcode'].value_counts()
df_subset = pd.DataFrame(subset)
df_subset.reset_index(inplace=True)
df_subset.rename(columns={'count': 'accepts'}, inplace=True)
doc_zip = doc_zip.merge(df_subset, how='left', left_on='Zipcode', right_on='Zipcode')

df_subset = df_doc[df_doc['Accepts Medicaid'] == True]
subset = df_subset['State'].value_counts()
df_subset = pd.DataFrame(subset)
df_subset.reset_index(inplace=True)
df_subset.rename(columns={'count': 'accepts'}, inplace=True)
doc_state = doc_state.merge(df_subset, how='left', left_on='State', right_on='State')

# add both
df_subset = df_doc[df_doc['Accepts Medicaid'] == True]
df_subset = df_subset[df_subset['Number of Ratings'] > 5]
df_subset = df_subset[df_subset['Rating'] > 3]
subset = df_subset['Zipcode'].value_counts()
df_subset = pd.DataFrame(subset)
df_subset.reset_index(inplace=True)
df_subset.rename(columns={'count': 'both'}, inplace=True)
doc_zip = doc_zip.merge(df_subset, how='left', left_on='Zipcode', right_on='Zipcode')

df_subset = df_doc[df_doc['Accepts Medicaid'] == True]
df_subset = df_subset[df_subset['Number of Ratings'] > 5]
df_subset = df_subset[df_subset['Rating'] > 3]
subset = df_subset['State'].value_counts()
df_subset = pd.DataFrame(subset)
df_subset.reset_index(inplace=True)
df_subset.rename(columns={'count': 'both'}, inplace=True)
doc_state = doc_state.merge(df_subset, how='left', left_on='State', right_on='State')

# drop null values
doc_zip.fillna(0, inplace=True)
doc_state.fillna(0, inplace=True)

# ---ZIP GEODATA---

print('PROCESSING ZCTA DATA')

# import zip geodata
geodata_zip = gpd.read_file("C:\\Users\\vikra\\NYU_2023\\data\\shapefiles\\zip_raw\\tl_2022_us_zcta520.shp")
geodata_zip.to_crs("EPSG:4326", inplace=True)

# add states to zip geodata
states = []
for zip in geodata_zip['ZCTA5CE20']:
    state = zipcodes.matching(zip)[0]['state']
    states.append(state)
geodata_zip['STATE'] = states

# remove states without data
geodata_zip = geodata_zip[geodata_zip['STATE'] != 'VI']
geodata_zip = geodata_zip[geodata_zip['STATE'] != 'MP']
geodata_zip = geodata_zip[geodata_zip['STATE'] != 'GU']
geodata_zip = geodata_zip[geodata_zip['STATE'] != 'AS']

# import census zip data
census_zip = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\census_zip.csv")
df_zip = pd.DataFrame(census_zip)

# merge and clean zip geodata
geodata_zip['ZCTA'] = geodata_zip['ZCTA5CE20'].astype('int')
geodata_zip = geodata_zip.merge(df_zip,  how="left", left_on=['ZCTA'], right_on=['zip'])
geodata_zip.drop(['ZCTA5CE20', 'GEOID20', 'CLASSFP20', 'MTFCC20', 'FUNCSTAT20', 'zip'], inplace=True, axis=1)

geodata_zip = geodata_zip.merge(doc_zip, how="left", left_on=['ZCTA'], right_on=['Zipcode'])
geodata_zip.drop(['Zipcode'], inplace=True, axis=1)

# save cleaned zip geodata
geodata_zip.fillna(0, inplace=True)
geodata_zip.to_file('data/shapefiles/zip_data/zip.shp')

# ---STATE GEODATA---

print('PROCESSING STATE DATA')

# import zip geodata
geodata_state = gpd.read_file("C:\\Users\\vikra\\NYU_2023\\data\\shapefiles\\state_raw\\tl_2022_us_state.shp")
geodata_state.to_crs("EPSG:4326", inplace=True)

# import census state data
census_state = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\census_state.csv")
df_state = pd.DataFrame(census_state)

# merge and clean state geodata
geodata_state = geodata_state.merge(df_state,  how="right", left_on=['STUSPS'], right_on=['state'])
geodata_state.drop(['REGION', 'DIVISION', 'STATEFP', 'STATENS', 'GEOID', 'NAME', 'LSAD', 'MTFCC', 'FUNCSTAT', 'STUSPS'], inplace=True, axis=1)

geodata_state = geodata_state.merge(doc_state, how="left", left_on=['state'], right_on=['State'])
geodata_state.drop(['State'], inplace=True, axis=1)

# save cleaned state geodata
geodata_state.fillna(0, inplace=True)
geodata_state.to_file('data/shapefiles/state_data/state.shp')
