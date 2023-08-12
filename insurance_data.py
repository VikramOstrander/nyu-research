# ------------
# program to clean DAC_NationalDownloadableFile.csv sourced from cms.gov
# data on doctors enrolled in medicaid programs
# formatted data exported to cms_data.csv
# ------------

import pandas as pd
import concurrent.futures

# initial cleanup of data
data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\DAC_NationalDownloadableFile.csv", encoding='latin-1')
df = pd.DataFrame(data)

df.drop_duplicates(subset='NPI', inplace=True, ignore_index=True)
df.drop(df.iloc[:, 27:], inplace=True, axis=1)
df.drop(df.iloc[:, 5:25], inplace=True, axis=1)
df.drop(df.iloc[:, 0:3], inplace=True, axis=1)

df.to_csv("cms_data.csv", encoding='utf-8', index=False)

# formatting for analysis
df.drop(df.columns[[4, 5]], inplace=True, axis=1)

last = df["lst_nm"].to_list()
first = df["frst_nm"].to_list()
zip_full = df["zip"].to_list()
full = ['0'] * len(zip_full)
zipcode = ['0'] * len(zip_full)


def cleanup(i):
    full[i] = str(first[i]).lower() + ' ' + str(last[i]).lower()
    zipcode[i] = str(zip_full[i])[:5]


params = list(range(0, len(zip_full)))
with concurrent.futures.ThreadPoolExecutor(max_workers=70) as executor:
    executor.map(cleanup, params)
df['Name'] = full
df['Zipcode'] = zipcode

df.drop(df.columns[[0, 1, 2, 3]], inplace=True, axis=1)
df.to_csv("cms_data.csv", encoding='utf-8', index=False)
