import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Use TkAgg backend for interactive plotting 
matplotlib.use('TkAgg')

# =========================
# Load data
# =========================

# restaurants = pd.read_csv('data.csv')  # Example alt dataset (unused)
restaurants = pd.read_csv('restaurants.csv')
reviews = pd.read_csv('reviews.csv')

# =========================
# Clean and enrich review data
# =========================

# Convert review dates to datetime and extract year
reviews['date'] = pd.to_datetime(reviews['date'])
reviews['year'] = reviews['date'].dt.year

# Total count of rows in `reviews['stars']`, repeated in every row
reviews['count'] = reviews['stars'].count()

# Merge reviews with restaurant metadata
reviews_full = reviews.merge(
    restaurants,
    on='business_id',
    how='left'
)

# =========================
# Aggregate by state and year
# =========================

state_year = (
    reviews_full
    .groupby(['state', 'year'])
    .agg(
        avg_stars=('stars', 'mean'),
        count=('stars', 'size')
    )
    .reset_index()
)

# =========================
# Filter out sandwich chains of interest
# =========================

# Subway reviews
subway = reviews_full[
    reviews_full['name'].str.contains('Subway', case=False, na=False)
]
subway.shape
subway['stars'].describe()
# print(subway.shape)
# print(subway['stars'].describe())

# Bonus section: local vs global Subway
subway_local_mean = 3.2
print("subway_local_mean:", subway_local_mean)

subway_global = subway['stars']
subway_global_mean = round(subway_global.mean(), 3)
print("subway_global_mean:", subway_global_mean)

# Jersey Mike's reviews
jersey_mikes = reviews_full[
    reviews_full['name'].str.contains("Jersey Mike's", case=False, na=False)
]
jersey_mikes.shape
jersey_mikes['stars'].describe()
# print(jersey_mikes.shape)
# print(jersey_mikes['stars'].describe())

# Wawa reviews
wawa = reviews_full[
    reviews_full['name'].str.contains('Wawa', case=False, na=False)
]
wawa.shape
wawa['stars'].describe()
# print(wawa.shape)
# print(wawa['stars'].describe())

# Combine all three sandwich brands
sandwich_places = pd.concat([subway, jersey_mikes, wawa])

# =========================
# Classify restaurant chain types
# =========================

# Count how many distinct cities each brand appears in
city_counts = (
    restaurants
    .groupby('name')['city']
    .nunique()
    .sort_values(ascending=False)
)
# print(city_counts)

# Map each brand to a chain type based on city count
type_map = city_counts.copy()
type_map = np.where(
    city_counts >= 50, 'national',
    np.where(city_counts == 1, 'local', 'other')
)

# Attach chain type to restaurants
restaurants['chain_type'] = restaurants['name'].map(
    dict(zip(city_counts.index, type_map))
)

# Merge chain_type back into full reviews
reviews_full = reviews_full.merge(
    restaurants[['business_id', 'chain_type']],
    on='business_id',
    how='left'
)

# =========================
# Restrict to reviews from 2018 to 2021
# =========================

reviews_full['year'] = pd.to_datetime(reviews_full['date']).dt.year
reviews_18_21 = reviews_full[reviews_full['year'].between(2018, 2021)]

# =========================
# Plots
# =========================

# 1. Average rating by year
plt.figure('Question 1A')
sns.lineplot(x='year', y='avg_stars', data=state_year)
plt.xlabel('Year')
plt.ylabel('Average star rating')
plt.title('Average Yelp rating by year')
plt.ylim(0, 5)

# 2. Number of reviews by state and year
plt.figure('Question 1B')
sns.barplot(x='state', y='count', data=state_year)
plt.title('Number of Yelp reviews by state and year')

# 3. Boxplot of star ratings for Subway vs competitors
plt.figure('Question 2')
sns.boxplot(x='name', y='stars', data=sandwich_places)
plt.title('Subway Vs Competitors')

# 4. Boxplot by chain size (local vs national vs other)
plt.figure('Question 3')
sns.boxplot(x='chain_type', y='stars', data=reviews_full)
plt.title('Rating by Size')

# 5. Distribution of ratings from 2018 to 2021
plt.figure('Question 4')
sns.countplot(
    x='stars',
    data=reviews_18_21,
    order=sorted(reviews_18_21['stars'].unique())
)
plt.xlabel('Star Rating')
plt.ylabel('Number of Reviews')
plt.title('Ratings from 2018 to 2021')
plt.tight_layout()

# =========================
# Bonus visualization 1
# Histogram of all Subway ratings
# with local and global means highlighted
# =========================

plt.figure('Bonus Visualization #1', figsize=(6, 4))

plt.hist(
    subway['stars'],
    bins=10,
    edgecolor='black',
    alpha=0.7
)

plt.axvline(
    subway_local_mean,
    color='red',
    linewidth=2,
    label='Local Subway (3.2)'
)

plt.axvline(
    subway_global_mean,
    color='green',
    linewidth=2,
    label=f'Global Mean ({subway_global_mean})'
)

plt.xlabel('Star Rating')
plt.ylabel('Frequency')
plt.title('Distribution of Global Subway Ratings\nwith Local Store Highlighted')
plt.legend()
plt.tight_layout()

# =========================
# Bonus visualization 2
# Subway vs competitors histogram
# =========================

competitors = pd.concat([jersey_mikes, wawa], ignore_index=True)

plt.figure('Bonus Visualization #2', figsize=(8, 5))

# Subway histogram
plt.hist(
    subway['stars'],
    bins=[1, 2, 3, 4, 5, 6],
    alpha=0.6,
    label='Subway',
    edgecolor='black'
)

# Competitors histogram
plt.hist(
    competitors['stars'],
    bins=[1, 2, 3, 4, 5, 6],
    alpha=0.55,
    label="Jersey Mike's + Wawa",
    edgecolor='black'
)

plt.xlabel('Star Rating')
plt.ylabel('Number of Reviews')
plt.title('Distribution of Ratings: Subway vs Competitors')
plt.xticks([1, 2, 3, 4, 5])
plt.legend()
plt.tight_layout()

# =========================
# Bonus visualization 3
# Distribution of average rating per Subway store
# =========================

subway_store_avg = (
    subway
    .groupby('business_id')['stars']
    .mean()
    .reset_index(name='avg_stars')
)

plt.figure('Bonus Visualization #3', figsize=(6, 4))
plt.hist(subway_store_avg['avg_stars'], bins=10, edgecolor='black')
plt.xlabel('Average Store Rating')
plt.ylabel('Number of Subway Locations')
plt.title('Distribution of Average Ratings Across Subway Stores')
plt.xlim(1, 5)
plt.tight_layout()

# Render all figures
plt.show()
