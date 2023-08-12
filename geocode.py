# ------------
# program to generate coordinates for all doctor locations
# geospatial data stored in geo_doctors.csv
# ------------

import pandas as pd
import numpy as np
import time
import datetime
from geopy.geocoders import ArcGIS



# -----VALUES TO EDIT-----
START = 1038100
BATCH = 100
FINISH = 1100000
# ------------------------



data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\doctor_data.csv")
df = pd.DataFrame(data)

FINISH = min(FINISH, len(df))

df = df.iloc[START:FINISH]
df['Textual Reviews'] = df['Textual Reviews'].astype('str')
df['Text Reviews'] = np.where(df['Textual Reviews'] == 'nan', False, True)
df.drop(['Textual Reviews'], axis=1, inplace=True)

TOTAL = FINISH-START
nom = ArcGIS()

locations = df['Location'].tolist()
latitude = []
longitude = []
errors = []

print("---begin geocoding---")


def geocode(begin, limit):

    t = time.time()
    for i in range(begin, limit):

        location = nom.geocode(locations[i])
        if location is None:
            print(f"error received on index {START+i}")
            latitude.append('skip')
            longitude.append('skip')
            errors.append(START+i)
        else:
            latitude.append(location.latitude)
            longitude.append(location.longitude)

    t = time.time() - t
    return t


start_time = time.time()
for i in range(0, TOTAL, BATCH):

    limit = min(i + BATCH, TOTAL)
    t = geocode(i, limit)

    df_new = df[i:limit]
    df_new['Latitude'] = latitude
    df_new['Longitude'] = longitude
    if START == i == 0:
        df_new.to_csv('data/geo_doctors.csv', mode='a', index=False, encoding='utf-8')
    else:
        df_new.to_csv('data/geo_doctors.csv', mode='a', index=False, header=False, encoding='utf-8')

    latitude = []
    longitude = []

    cur_time = str(datetime.timedelta(seconds=round(time.time()-start_time)))
    print('-'*20)
    print(f"total progress: {START+limit}/{FINISH}\ntime elapsed: {cur_time}\nprocessed {limit-i} addresses in {t:.2f} seconds")
    print(f"issues with indicies: {errors}")
    print('-'*20)
