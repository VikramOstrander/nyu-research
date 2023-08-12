# ------------
# program to extract individual textual reviews from doctor_data.csv
# data exported to reviews.csv
# ------------

import pandas as pd
import re

# import data
data = pd.read_csv("C:\\Users\\vikra\\NYU_2023\\data\\doctor_data.csv")
df = pd.DataFrame(data)

# extract ids, doctors, and textual reviews
id_list = df['ID']
doctors_list = df['Name']
reviews_list = df['Textual Reviews']

# initialize empty lists
id = []
doctors = []
reviews = []
ratings = []

# iterate through each doctor to extract individual textual reviews
for i in range(0, len(id_list)):

    # select the current doctor
    doctor_id = id_list[i]
    doctor = doctors_list[i]
    review_list = str(reviews_list[i])

    # ignore doctors with no textual reviews
    if review_list == "nan":
        continue

    # create a list of all textual reviews for the current doctor
    review_list_split = []
    match = re.search(r",\d: ", review_list)
    while match:
        review_list_split.append(review_list[0:match.start()])
        review_list = review_list[match.start()+1:]
        match = re.search(r",\d: ", review_list)
    review_list_split.append(review_list)

    # process each review for it's rating and contents
    for review in review_list_split:
        if review[0] == 'T':
            continue
        id.append(doctor_id)
        doctors.append(doctor)
        ratings.append(review[0])
        reviews.append(review[3:])

# print summary of reviews
ratings_df = pd.DataFrame({'Rating': ratings})
print(f"total: {len(ratings_df)}")
print(pd.value_counts(ratings_df['Rating']))
# NOTE:
#   out of the 3122488 total reviews: 2401965 are 5 star and 575710 are 1 star
#   this means that 4.64% of the reviews were the intermediary values 2, 3, or 4
#   use sentiment analysis to better classify the sentiment behind the text

# export data to reviews.csv
review_df = pd.DataFrame({'Doctor ID': id, 'Doctor Name': doctors, 'Rating': ratings, 'Review': reviews})
review_df.to_csv('data/reviews.csv', index=False, encoding='utf-8')
