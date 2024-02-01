### User Based Collaborative Filtering Recommender System

<br >

## What is User Based Collaborative Filtering Recommender System?

User-based collaborative filtering makes recommendations based on user-product interactions in the past.The assumption behind the algorithm is that similar users like similar products.

<br >

## How does the User Based Collaborative Filtering Recommender System work?

1- Find similar users based on interactions with common items.
2- Identify the items rated high by similar users but have not been exposed to the active user of interest.
3- Calculate the weighted average score for each item.
4- Rank items based on the score and pick the top n items to recommend.

<br >

## Prepare for Use

Go `algorithm.py` and find

```py
ITEM_RATINGS_PATH = Path
ITEM_NAMES_PATH = Path
```

Write your files path

<br >

## How should the files be?

The order in the ITEM_RATINGS should be like this
`user id | item id | rating | ...`

The order in the ITEM_NAMES should be like this
`movie id | movie title | ...`

<br >

## How to Use

```py
from algorithm import recommend

recommend(user_id, n_recomm, n_neighbors)

```

parameters:<br >
    - user_id: int, user to generate recommendations for<br >
    - n_neighbors: int: the number of neighbors to use to generate rating predictions<br >
    - n_recomm: int, number of movies to recommend

returns:
    - pd.DataFrame with [movie_id, rating, movie name]
