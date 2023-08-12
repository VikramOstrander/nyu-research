# ------------
# program to clean ACSST5Y2021.S1701-Data.csv (zcta) and ACSST5Y2021.S1701-2023-07-06T180522.csv (state) sourced from census.gov
# data on population and poverty rate by ZCTA and State
# formatted data exported to data/census_zip.csv and data/census_state.csv
# ------------

import pandas as pd

# zipcode data
zip_data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\ACSST5Y2021.S1701-Data.csv", encoding="latin-1")
df_zip = pd.DataFrame(zip_data)

zcta = df_zip[str(df_zip.columns[1])]
zip_pop = df_zip[str(df_zip.columns[2])]
zip_pov = df_zip[str(df_zip.columns[498])]

zipcodes = []
for zip in zcta:
    zipcodes.append(zip.split(' ')[1])

df_zip = pd.DataFrame({'zip': zipcodes, 'pop': zip_pop, 'pov': zip_pov})
df_zip = df_zip[df_zip.pov != '-']
df_zip = df_zip.drop(0)
df_zip.to_csv("data/census_zip.csv", encoding='utf-8', index=False)



# state data
state_data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\ACSST5Y2021.S1701-2023-07-06T180522.csv", encoding="latin-1")
df_state = pd.DataFrame(state_data)

print(df_state.columns.values)

col0 = df_state[str(df_state.columns[0])]
col1 = df_state[str(df_state.columns[1])]

state_names = []
state_pop = []
state_pov = []

for i in range(0, len(df_state), 10):
    state_names.append(col0[i])
    state_pop.append(int(col1[i+2].replace(',', '')))
    state_pov.append(int(col1[i+5].replace(',', '')))

for i in range(0, len(state_pov)):
    state_pov[i] = (state_pov[i]/state_pop[i])*100

states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 
          'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'PR']

df_state = pd.DataFrame({'state': states, 'name': state_names, 'pop': state_pop, 'pov': state_pov})
df_state.to_csv("data/census_state.csv", encoding='utf-8', index=False)
