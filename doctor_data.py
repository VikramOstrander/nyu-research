# ------------
# program for combining doctors.csv and cms_data.csv
# combined data exported to doctor_data.csv
# ------------

import pandas as pd
import bisect
import re
import concurrent.futures
import time
import datetime


import requests
from bs4 import BeautifulSoup



# -----VALUES TO EDIT-----
START = 0
END = 3006892
BATCH = 1000
THREADS = 6
# ------------------------



# importing and cleaning data
doctor_data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\doctors.csv", index_col=None)
df_doctor = pd.DataFrame(doctor_data)
df_doctor.drop_duplicates(subset=['Name', 'Location'], keep="first", inplace=True)

insurance_data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\cms_data.csv", index_col=None)
df_insurance = pd.DataFrame(insurance_data)

# sorting insurance data
df_insurance.sort_values(by='Zipcode', inplace=True)
insurance_zip = df_insurance['Zipcode'].tolist()
insurance_names = df_insurance['Name'].tolist()

# check if doctor has medicaid
accepts = list(range(len(df_doctor)))


def process(i):
    doctor_name = df_doctor['Name'].tolist()[i].lower()
    doctor_zip = int(df_doctor['Zipcode'].tolist()[i])

    parsed_name = doctor_name[doctor_name.find('.')+1:doctor_name.find(',')].split()
    doctor_first = parsed_name[0].lower()[0]
    doctor_last = re.sub(r"[^a-z]+", "", parsed_name[1].lower())

    accepts[i] = False

    start_index = bisect.bisect_left(insurance_zip, doctor_zip)
    end_index = bisect.bisect_right(insurance_zip, doctor_zip)

    if start_index == len(insurance_zip) or insurance_zip[start_index] != doctor_zip or insurance_zip[end_index-1] != doctor_zip:
        return()
    
    for j in range(start_index, end_index):
        
        insurance_name = insurance_names[j]
        insurance_first = insurance_name[0]
        insurance_last = insurance_name[insurance_name.find(' ')+1:]
        insurance_last = re.sub(r"[^a-z]+", "", insurance_last)

        if insurance_first == doctor_first and insurance_last == doctor_last:
            accepts[i] = True
            index_list[i] = j
            return()


if END > len(df_doctor):
    END = len(df_doctor)

index_list = list(range(len(df_doctor)))

start_time = time.time()
for i in range(START, END, BATCH):
    end = min(i+BATCH, END)
    t = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(process, index_list[i:end])
    t = time.time()-t
    cur_time = str(datetime.timedelta(seconds=round(time.time()-start_time)))

    df_new = df_doctor.iloc[i:end]
    df_new.insert(7, 'Accepts Medicaid', accepts[i:end])
    df_new.to_csv('data/doctor_data.csv', mode='a', index=False, encoding='utf-8')

    print(f"processed {end-START} doctors in {cur_time}\tcurrent rate: {t/BATCH}")
