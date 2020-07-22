import pandas as pd
from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from collections import defaultdict
import json

ratings = pd.read_csv('ratings_small.csv')
# A reader is still needed but only the rating_scale param is requiered.
reader = Reader(rating_scale=(1, 5))

# The columns must correspond to user id, item id and ratings (in that order).
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)


def get_top_n(predictions, n=10):
  '''Return the top-N recommendation for each user from a set of predictions.

  Args:
      predictions(list of Prediction objects): The list of predictions, as
          returned by the test method of an algorithm.
      n(int): The number of recommendation to output for each user. Default
          is 10.

  Returns:
  A dict where keys are user (raw) ids and values are lists of tuples:
      [(raw item id, rating estimation), ...] of size n.
  '''

  # First map the predictions to each user.
  top_n = defaultdict(list)
  for uid, iid, true_r, est, _ in predictions:
    top_n[uid].append((iid, est))

  # Then sort the predictions for each user and retrieve the k highest ones.
  for uid, user_ratings in top_n.items():
    user_ratings.sort(key=lambda x: x[1], reverse=True)
    top_n[uid] = user_ratings[:n]

  return top_n


# We'll use the KNN algorithm.
algo = KNNBasic()
trainset = data.build_full_trainset()
algo.fit(trainset)
# Than predict ratings for all pairs (u, i) that are NOT in the training set.
testset = trainset.build_anti_testset()
predictions = algo.test(testset)
top_n = get_top_n(predictions, n=10)

with open('topN.json', 'w') as outfile:
    json.dump(top_n, outfile)