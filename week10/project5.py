import pandas as pd 
import plotly.express as px
import numpy as np

url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/star-wars-survey/StarWars.csv"
data = pd.read_csv(url, encoding='unicode_escape')
"""
RespondentID,
Have you seen any of the 6 films in the Star Wars franchise?,
Do you consider yourself to be a fan of the Star Wars film franchise?,
Which of the following Star Wars films have you seen? 
Please select all that apply.,,,,,,
Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.,,,,,,
"Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.",,,,,,,,,,,,,,
Which character shot first?,
Are you familiar with the Expanded Universe?,
Do you consider yourself to be a fan of the Expanded Universe?��,
Do you consider yourself to be a fan of the Star Trek franchise?,
Gender,
Age,
Household Income,
Education,
Location (Census Region),
Response,
Response,
Star Wars: Episode I  The Phantom Menace,
Star Wars: Episode II  Attack of the Clones,
Star Wars: Episode III  Revenge of the Sith,
Star Wars: Episode IV  A New Hope,
Star Wars: Episode V The Empire Strikes Back,
Star Wars: Episode VI Return of the Jedi,
Star Wars: Episode I  The Phantom Menace,
Star Wars: Episode II  Attack of the Clones,
Star Wars: Episode III  Revenge of the Sith,
Star Wars: Episode IV  A New Hope,
Star Wars: Episode V The Empire Strikes Back,
Star Wars: Episode VI Return of the Jedi,
Han Solo,
Luke Skywalker,
Princess Leia Organa,
Anakin Skywalker,
Obi Wan Kenobi,
Emperor Palpatine
Darth Vader,
Lando Calrissian,
Boba Fett,
C-3P0,
R2 D2,
Jar Jar Binks,
Padme Amidala,
Yoda,
Response,
Response,
Response,
Response,
Response,
Response,
Response,
Response,
Response
"""
#print(data.head())
"""
Shorten the column names and clean them up for easier use 
with pandas. Provide a table or list that exemplifies how you 
fixed the names.
"""
print('\u00e6')
data.rename(columns = {
    'Have you seen any of the 6 films in the Star Wars franchise?': 'Seen_SW',
    'Do you consider yourself to be a fan of the Star Wars film franchise?': 'Fan_of_SW',
    'Which character shot first?':'shot_first',
    'Are you familiar with the Expanded Universe?':'familair_EU',
    'Do you consider yourself to be a fan of the Expanded Universe?\u00e6':'fan_EU',
    'Do you consider yourself to be a fan of the Star Trek franchise?':'ST_fan',
    'Household Income':'Income',
    
    #Context clues said these are the Star wars movies of the original and newest trilogies
    'Which of the following Star Wars films have you seen? Please select all that apply.':'SW1',
    'Unnamed: 4': 'SW2',
    'Unnamed: 5': 'SW3',
    'Unnamed: 6': 'SW4',
    'Unnamed: 7': 'SW5',
    'Unnamed: 8': 'SW6',

    'Please rank the Star Wars films in order of preference with 1 being your favorite film in the franchise and 6 being your least favorite film.':'SW1_ranked',
    'Unnamed: 10': 'SW2_ranked',
    'Unnamed: 11': 'SW3_ranked',
    'Unnamed: 12': 'SW4_ranked',
    'Unnamed: 13': 'SW5_ranked',
    'Unnamed: 14': 'SW6_ranked',

#Jar Jar Binks,Padme Amidala,Yoda,

    'Please state whether you view the following characters favorably, unfavorably, or are unfamiliar with him/her.': 'Han_Solo',
    'Unnamed: 16': 'Luke_Skywalker',
    'Unnamed: 17': 'Princes_Leia',
    'Unnamed: 18': 'Anakin',
    'Unnamed: 19': 'Obi Wan',
    'Unnamed: 20': 'Palpatine',
    'Unnamed: 21': 'Darth_Vadar',
    'Unnamed: 22': 'Lando_Calrissian',
    'Unnamed: 23': 'Boba_Fett',
    'Unnamed: 24': 'C-3PO',
    'Unnamed: 25': 'R2_D2',
    'Unnamed: 26': 'Jar_Jar_Binks',
    'Unnamed: 27': 'Padme_Amidala',
    'Unnamed: 28': 'Yoda'

}, inplace = True)

#data['Expanded Universe'] = data['Do you consider yourself to be a fan of the Expanded Universe?æ']
#data.drop('Do you consider yourself to be a fan of the Expanded Universe?æ',inplace=True,axis=1)
print(data.filter(["Do you consider yourself to be a fan of the Expanded Universe?æ"]))
#data['Expanded Universe'] = data[f'Do you consider yourself to be a fan of the Expanded Universe?\ae\']

print(data.info())
print(data.head())

"""
Clean and format the data so that it can be used in a machine learning model. As you format the data, 
you should complete each item listed below. In your final report provide example(s) of the reformatted 
data with a short description of the changes made.
"""
# Filter the dataset to respondents that have seen at least one film.
data_new = data.query('Seen_SW == "Yes"')
print(data_new.filter(["Seen_SW"]).head())

# Create a new column that converts the age ranges to a single number. Drop the age range categorical column.
def split_age(i):
    age_list = str(i.Age).split("-")
    if age_list[0] == "> 60":
        return 61
    elif age_list[0] == "NaN":
        return 0
    return float(age_list[0])

data_new['Age'] = data_new['Age'].fillna(0)
data_new["age_range"] = data_new.apply(split_age, axis=1)
del data['Age']

print(data_new.filter(["age_range"]))

# Create a new column that converts the education groupings to a single number. Drop the school categorical column
def split_education(i):
    i = i.Education
    if i == "High school degree":
        return 1.0
    elif i == "Some college or Associate degree":
        return 2.0
    elif i == "Bachelor degree":
        return 3.0
    elif i == "Graduate degree":
        return 4.0
data_new["education"] = data_new.apply(split_education, axis=1)
data_new['education'] = data_new['education'].fillna(0)
del data_new['Education']
print(data_new.filter(["education"]))

# Create a new column that converts the income ranges to a single number. Drop the income range categorical column.
def split_income(i):
    income_list = str(i.Income).split(" - ")
    if income_list[0] == "$0":
        return 1
    elif income_list[0] == "$25,000":
        return 2
    elif income_list[0] == "$50,000":
        return 4
    elif income_list[0] == "$100,000":
        return 8
    elif income_list[0] == "$150,000+":
        return 12
    else: # NaN
        return 0
    
data_new["Income_range"] = data_new.apply(split_income, axis=1)
del data_new['Income']
print(data_new.filter(["Income_range"]))

# Create your target (also known as “y” or “label”) column based on the new income range column.
data_new['label'] = data_new.apply(lambda _: '', axis=1)

# One-hot encode all remaining categorical columns.
print(data_new.filter(['SW1_ranked','SW2_ranked','SW3_ranked','SW4_ranked','SW5_ranked','SW6_ranked']).head())

from sklearn.preprocessing import OneHotEncoder 
category_list = [
    'SW1','SW2','SW3','SW4','SW5','SW6',#'SW1_ranked','SW2_ranked','SW3_ranked','SW4_ranked','SW5_ranked','SW6_ranked',

    'Luke_Skywalker','Princes_Leia','Anakin','Obi Wan','Palpatine','Darth_Vadar','Lando_Calrissian',
    'Boba_Fett','C-3PO','R2_D2','Jar_Jar_Binks','Padme_Amidala','Yoda',

    'Seen_SW','Fan_of_SW','shot_first','familair_EU','ST_fan',

    'Gender','Location (Census Region)',
                 ]

enc = OneHotEncoder() 
enc_data = 0
for i in category_list:
    data_new[(i)] = data_new[(i)].astype('category').cat.codes

    enc_data += pd.DataFrame(enc.fit_transform(data_new[[i]]).toarray())

data = data_new.join(enc_data) 
print(data.info()) 


"""
Validate that the data provided on GitHub lines up with the article by recreating 2 of the visuals from the article.
"""
# Which 'Star Wars' Movies Have You Seen?
movies = ['SW1','SW2','SW3','SW4','SW5','SW6']
#print(data.filter(['SW1_ranked','SW2_ranked','SW3_ranked','SW4_ranked','SW5_ranked','SW6_ranked']).head())
#print(data.filter(['SW1','SW2','SW3','SW4','SW5','SW6']).head())

movies_ranked = ['SW1_ranked','SW2_ranked','SW3_ranked','SW4_ranked','SW5_ranked','SW6_ranked']
seen_all = data.query('SW1 == 0 and SW2 == 0 and SW3 == 0 and SW4 == 0 and SW5 == 0 and SW6 == 0')
print(seen_all.filter(['SW1_ranked','SW2_ranked','SW3_ranked','SW4_ranked','SW5_ranked','SW6_ranked']).head())

def SW_Movie_Seen(i):
# Which of the following Star Wars films have you seen?
    if i.SW1_ranked == 1:
        return "SW1"
    elif i.SW2_ranked == 1:
        return "SW2"
    elif i.SW3_ranked == 1:
        return "SW3"    
    elif i.SW4_ranked == 1:
        return "SW4"    
    elif i.SW5_ranked == 1:
        return "SW5"
    elif i.SW6_ranked == 1:
        return 'SW6'

seen_all["SW_ranked"] = seen_all.apply(SW_Movie_Seen, axis=1)
#print(New_df.filter(["SW_ranked"]))

chart = px.histogram(seen_all,
    x = "SW_ranked",
    )
chart.show()