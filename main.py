import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 

# Data cleaning and Processing
df = pd.read_csv('mymoviedb.csv', lineterminator='\n')
print(df.head())
df.info()
print(df['Genre'].head())

dup= (df.duplicated().sum())
print(dup)

describe= df.describe()
print(describe)

#Summury
"""
>> We have a dataframe. in dataframe 9827 rows and 9 columns.
>> in our dataframe no NaN value or not any duplicate value.
>> Realse date column casted into date time and to extract only the year value.
>> overview, orignal_language and poster_url drop into dataframes.
>> genre columns in whitespace remove and need to handle. 
"""

#Covert format into datetime
df['Release_Date'] = pd.to_datetime(df['Release_Date']) 
print(df['Release_Date'].dtype)

df['Release_Date'] = df['Release_Date'].dt.year
print(df['Release_Date'].dtype)
print(df.head())

# Dropping the columns
# print(df.columns)

cols = ['Overview', 'Original_Language', 'Poster_Url']
df.drop(cols, axis=1, inplace=True)
print(df.columns)
# print(df.head())

"""
we would cut the Vote_Avarage values and make 4 categorizing:
popular, average, below_avg, not_popular to describe it more using catagorize_col()
function provide above.
"""

#Catagorizing Vote_Average column
def catagorize_col(df, col, labels):
    
    edges = [df[col].describe()['min'],
            df[col].describe()['25%'],
            df[col].describe()['50%'],
            df[col].describe()['75%'],
            df[col].describe()['max']]
    
    df[col] = pd.cut(df[col], edges, labels= labels, duplicates='drop')
    return df

labels = ['not_popular', 'below_avg', 'average', 'popular']

catagorize_col(df, 'Vote_Average', labels)
print(df['Vote_Average'].unique())
print(df.head())

values= df['Vote_Average'].value_counts()
print(values)

df.dropna(inplace=True)
print(df.isna().sum())


#we'd split genre and one genre for each rows
df['Genre'] = df['Genre'].str.split(', ')
df = df.explode('Genre').reset_index(drop=True)
print(df.head())


#Casting column into catagory
df['Genre'] = df['Genre'].astype('category')
print(df['Genre'].dtype)
df.info()  

#Data Visulization
print(df['Genre'].describe())

# # What is the most frequent gerne of movie released on netflix.
# sns.catplot(y = 'Genre', data= df, kind= 'count',
#             order= df['Genre'].value_counts().index,
#             color='#4287f5')
# plt.title('Genre column distribution')
# plt.show()


# # Which has highest votes in vote avg columns.
# sns.catplot(y= 'Vote_Average', data= df, kind='count',
#             order= df['Vote_Average'].value_counts().index,
#             color= '#4287f5')
# plt.title('Votes Distribution')
# plt.show() 


#What movies got the highest popularity ? what's its genre?
print(df[df['Popularity'] == df['Popularity'].max()])

#What movies got the highest popularity ? what's its genre?
print(df[df['Popularity'] == df['Popularity'].min()])

# #Which year has the most filmmed movies ?
# df['Release_Date'].hist()
# plt.title('Release Date columns Distribution')
# plt.show()

# SUbplotting all charts
fig, ax = plt.subplots(1, 3, figsize= (20, 6))

genre_counts = df['Genre'].value_counts()
ax[0].barh(genre_counts.index, genre_counts.values, color='skyblue')
ax[0].set_title('Most Frequent Genres on Netflix')
ax[0].set_xlabel('Genre')
ax[0].set_ylabel('Count')
ax[0].tick_params(axis='x', rotation=90)

avg_votes = df['Vote_Average'].value_counts()
ax[1].barh(avg_votes.index, avg_votes.values, color='blue')
ax[1].set_title('Top Genres by Average Vote')
ax[1].set_xlabel('Genre')
ax[1].set_ylabel('Average Vote')
ax[1].tick_params(axis='x', rotation=90)

year_counts = df['Release_Date'].value_counts().sort_index()
ax[2].bar(year_counts.index.astype(int), year_counts.values, color='salmon')
ax[2].set_title('Movies Released per Year')
ax[2].set_xlabel('Year')
ax[2].set_ylabel('Number of Movies')
ax[2].tick_params(axis='x', rotation=90)

plt.tight_layout()
# plt.savefig('Final_charts.png', dpi=300, bbox_inches='tight')
plt.show()