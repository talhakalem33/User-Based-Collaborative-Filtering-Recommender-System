import pandas as pd

ITEM_RATINGS_PATH = Path
ITEM_NAMES_PATH = Path

N_NEIGHBORS = 10

N_RECOMMENDATIONS = 5

def read_ratings(path_to_ratings):

    data = []
    with open(path_to_ratings) as f:
        for line in f:
            # user id | item id | rating | timestamp
            pieces = line.split()
            user_id = int(pieces[0])
            item_id = int(pieces[1])
            rating = float(pieces[2])
            data.append((user_id, item_id, rating))
        
    return data

def read_names(path_to_names):

    data = {}
    with open(path_to_names) as f:
        for line in f:
            pieces = line.split('|')
            item_id = int(pieces[0])
            title = pieces[1]
            data[item_id] = title
        
    return data

ratings = read_ratings(ITEM_RATINGS_PATH)
ratings = pd.DataFrame(data=ratings, columns=['user', 'item', 'rating']).sample(100, random_state=42)
ratings = ratings.astype(int)

sample = ratings.sample(random_state=31)
user_id = sample.user.values[0]

ratings_raw = ratings.copy()
ratings = ratings.pivot(index='user', columns='item', values='rating')

def pearson_similarity(v1, v2):
    
    pearson = v1.corr(v2)
    
    return pearson

def compute_similarities(user_id, ratings_matrix):

    ratings_user = ratings_matrix.loc[user_id,:]
    
    similarities = ratings_matrix.apply(lambda row: pearson_similarity(ratings_user, row), axis=1)

    similarities = similarities.to_frame(name='similarity')

    similarities = similarities.sort_values(by='similarity', ascending=False)
    
    similarities = similarities.drop(user_id)
    
    return similarities

def predict_rating(item_id, ratings, similarities, N=10):
    
    users_ratings = ratings.loc[:, item_id]
    
    most_similar_users_who_rated_item = similarities.loc[~users_ratings.isnull()]
    
    N_most_similar_users = most_similar_users_who_rated_item.head(N)
    
    ratings_for_item = ratings.loc[N_most_similar_users.index, item_id]
    
    return ratings_for_item.mean()

movie_names = read_names(ITEM_NAMES_PATH)

def recommend(userid, n_neighbors=10, n_recomm=5):
    
    all_items = ratings.loc[userid,:]
    unrated_items = all_items.loc[all_items.isnull()]
    
    unrated_items = unrated_items.index.to_series(name='item_ids').reset_index(drop=True)
    print('User {} has {} unrated items.'.format(userid, len(unrated_items)))
    
    similarities = compute_similarities(userid, ratings)
        
    predictions = unrated_items.apply(lambda d: predict_rating(d, ratings, similarities, N=n_neighbors))
    
    predictions = predictions.sort_values(ascending=False)
    
    recommends = predictions.head(n_recomm)
    
    recommends = recommends.to_frame(name='predicted_rating')
    recommends = recommends.rename_axis('item_id')
    recommends = recommends.reset_index()
    
    recommends['name'] = recommends.item_id.apply(lambda d: movie_names[d])
    
    return recommends

