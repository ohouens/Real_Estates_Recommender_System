from .connect import Connect
from pymongo import MongoClient
from bson.objectid import ObjectId

import pandas as pd
import numpy as np

from scipy import spatial

import random

class CFLearning():
    """
    Collaborative Filtering Learning class
    """
    def __init__(self):
        self.client = Connect.get_connection()
        self.users = self.all_users()
        self.items = self.all_items()
        self.matrix = self.produce_matrix(self.users, self.items)

    def all_users(self):
        """
        client: the mongodb client
        return the list of all users of the database
        """
        result = []
        db = self.client.grand_paris_estates_users
        cursor = db.inventory.find({})
        for inventory in cursor:
            result.append(inventory["user"])
        return result

    def all_items(self):
        """
        client: the mongodb client
        return the list of all items of the database
        """
        result = []
        db = self.client.grand_paris_estates_unified
        cursor = db.inventory.find({"image": {"$ne":float('nan')}})
        for inventory in cursor:
            result.append(str(inventory["_id"]))
        return result

    def produce_matrix(self, users, items):
        """
        client: the mongodb client
        users: the list of all the users of the database
        items: the list of all the items of the database
        create the score matrix based on a user item approche
        """
        result = pd.DataFrame(data=np.zeros((len(users), len(items))), index=users, columns=items)
        db = self.client.grand_paris_estates_users
        cursor = db.inventory.find({})
        for user in cursor:
            if "action" in user and "previews_history" in user["action"]:
                for preview in user["action"]["previews_history"]:
                    result.at[user["user"], preview] += 1
            if "action" in user and "views_history" in user["action"]:
                for view in user["action"]["views_history"]:
                    result.at[user["user"], view] += 2
        return result

    def user_similarity(self, user, movie_dimension=5, result_dimension=3):
        """
        user: string -> The user which we will be searching other simular users
        movie_dimension: Maximum number of movies to calculate the distance
        result_dimension: Maximum number of similar users
        return a list of users with a similarity score of thereshold or plus
        """
        result = {}
        row = self.matrix.loc[user].nlargest(movie_dimension)
        sub_matrix = self.matrix.drop(user)[row.index]
        sub_matrix = sub_matrix.sub(sub_matrix.mean(axis=1), axis=0)
        for index, row_bis in sub_matrix.iterrows():
            result[index] = 1 - spatial.distance.cosine(row.tolist(), row_bis.tolist())
        return pd.Series(data=result, index=list(result)).nlargest(result_dimension)

    def recommended_item(self, user, similar_users, result_dimension=20):
        """
        user: string -> The user which we will be recommended items
        similar_user: pd.Series -> users who are similar to the main users with their similarity score
        """
        result = []
        if similar_users.dropna().empty:
            #send random items
            return random.sample(self.items, result_dimension)
        else:
            #send items with best scores among the most similar users
            sub_matrix = self.matrix.loc[similar_users.index.tolist(), :]
            user_rating = sub_matrix * similar_users
            user_rating = (user_rating.sum(axis=0)/similar_users.sum()).nlargest(result_dimension)
            return user_rating.index.tolist()

    def filtering(self, user, movie_dimension, result_dimension):
        similarity = self.user_similarity(user, movie_dimension, result_dimension)
        items = self.recommended_item(user, similarity, result_dimension)
        to_check = [ObjectId(item) for item in items]
        result = []
        db = self.client.grand_paris_estates_unified
        cursor = db.inventory.find({"_id": {"$in": to_check}})
        for inventory in cursor:
            temp = inventory
            temp["id"] = str(inventory["_id"])
            result.append(temp)
        return result
