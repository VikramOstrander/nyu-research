# ------------
# program to generate general visualizations for doctor data
# all visualizations stored in data/visualizations directory
# ------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\doctor_data.csv", converters={'Zipcode': str})
df = pd.DataFrame(data)
print(df['Specialty'].value_counts())
df_rounded = pd.DataFrame()
df_rounded['Rating'] = df['Rating'].round()
print(df_rounded.value_counts())


# medicaid graph
# print(df['Accepts Medicaid'].value_counts())
# ax = df['Accepts Medicaid'].value_counts().plot(kind='bar', figsize=(8,8), rot=0)
# ax.bar_label(ax.containers[0])
# plt.title('Medicaid Acceptance')
# plt.xlabel('Accepts Medicaid')
# plt.ylabel('Number of Doctors')
# plt.show()

# ratings graph
# df_rounded = pd.DataFrame()
# df_rounded['Rating'] = df['Rating'].round()
# order = [5.0, 4.0, 3.0, 2.0, 1.0]
# sns.countplot(x="Rating", data = df_rounded, order=order, color='#69d')
# plt.title('Distribution of Ratings')
# plt.xlabel('Rating')
# plt.ylabel('Number of Doctors')
# plt.tight_layout()
# plt.show()
