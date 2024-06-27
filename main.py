import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Load the data
df = pd.read_csv("tmdb-movies.csv")

# Data Cleaning
to_drop = ["id", "imdb_id", "cast", "homepage", "tagline", "keywords", "overview"]
df.drop(to_drop, inplace=True, axis=1)
df.drop_duplicates(inplace=True)
df["release_date"] = pd.to_datetime(df["release_date"])
df = df.replace(0, np.nan)
df = df.dropna()

# Research Question 1: Is the film industry making profit over years?
df.insert(1, "profit", df["revenue"] - df["budget"])
avg_profit_year = df.groupby("release_year")["profit"].mean()

# Plotting Average Profit Over Years
plt.figure(figsize=(10, 6))
avg_profit_year.plot(kind='line', color='black', title='Average Profit VS Years')
plt.xlabel('Year')
plt.ylabel('Profit')
plt.savefig('analysis/profit_over_years.png')
plt.show()

# Research Question 2: How long is the average movie?
runtime_stats = df["runtime"].describe()
plt.figure(figsize=(10, 5))
plt.xlabel('Runtime')
plt.ylabel('Number Of Movies')
plt.title('Runtime of all the movies')
plt.hist(df['runtime'], bins=20)
plt.savefig('analysis/runtime_distribution.png')
plt.show()

# Research Question 3: Which genre has the highest number of movies?
def separate_count(column):
    split_data = pd.Series(df[column].str.cat(sep='|').split('|'))
    count_data = split_data.value_counts(ascending=False)
    return count_data

genre_counts = separate_count("genres")
plt.figure(figsize=(9, 9))
genre_counts.plot(kind="pie", autopct="%1.1f%%")
plt.title('Percentage Of Genres')
plt.ylabel('')
plt.savefig('analysis/genre_distribution.png')
plt.show()

# Conclusions
print("Conclusions:")
print(f"The average runtime is {runtime_stats['mean']:.2f} min.")
print(f"The genre with the highest number of movies is {genre_counts.idxmax()} with {genre_counts.max()} movies.")
