# Yelp restaurant reviews: Data Programming assignment

Cornell MSBA, BANA 5440 Introduction to Data Programming, Assignment 2. I wrote this by hand in Python with pandas, matplotlib and seaborn.

The script loads a restaurants table and a reviews table, joins them, and answers a set of questions about Yelp ratings with plots.

## What it does

- **Question 1A and 1B:** average star rating by year, and review counts by state and year.
- **Question 2:** Subway vs. Jersey Mike's vs. Wawa, as boxplots of star ratings.
- **Question 3:** chain size. Each brand is classed as `national` (appears in 50 or more cities), `local` (one city) or `other`, and ratings are compared across the three.
- **Question 4:** the distribution of ratings for reviews from 2018 to 2021.
- **Bonus:** three Subway visualizations: a histogram of all Subway ratings with the local store (3.2) and global mean marked, Subway against its competitors, and the distribution of average rating per Subway store.

`Assignment2-code-and-output.pdf` has the code with the figures it produced.

## Running it

```
pip install -r requirements.txt
python Assignment2.py
```

The script uses the `TkAgg` matplotlib backend, so it needs Tk available (it ships with most Python installs).

## Data

The data is not in this repository. It comes from the [Yelp Open Dataset](https://www.yelp.com/dataset), which Yelp licenses for academic use and does not allow to be redistributed, so I have left the files out. To run the script, put two CSVs next to it:

- `restaurants.csv` with the columns `business_id`, `name`, `city`, `state`, `categories`
- `reviews.csv` with the columns `review_id`, `user_id`, `business_id`, `stars`, `date`

Both are reduced extracts built from the Yelp business and review files, restaurants only.
