from .connect import Connect
from pymongo import MongoClient

import pandas as pd
import numpy as np

from scipy import spatial

class CFLearning():
    """
    Collaborative Filtering Learning class
    """
    def __init__(self):
        client = Connect.get_connection()
        self.users = self.all_users(client)
        self.items = self.all_items(client)
        self.matrix = self.produce_matrix(client, self.users, self.items)

    def all_users(self, client):
        """
        client: the mongodb client
        return the list of all users of the database
        """
        result = []
        db = client.grand_paris_estates_users
        cursor = db.inventory.find({})
        for inventory in cursor:
            result.append(inventory["user"])
        return result

    def all_items(self, client):
        """
        client: the mongodb client
        return the list of all items of the database
        """
        result = []
        db = client.grand_paris_estates_unified
        cursor = db.inventory.find({})
        for inventory in cursor:
            result.append(str(inventory["_id"]))
        return result

    def produce_matrix(self, client, users, items):
        """
        client: the mongodb client
        users: the list of all the users of the database
        items: the list of all the items of the database
        create the score matrix based on a user item approche
        """
        result = pd.DataFrame(data=np.zeros((len(users), len(items))), index=users, columns=items)
        db = client.grand_paris_estates_users
        cursor = db.inventory.find({})
        for user in cursor:
            if "action" in user and "previews_history" in user["action"]:
                for preview in user["action"]["previews_history"]:
                    result.at[user["user"], preview] += 1
            if "action" in user and "views_history" in user["action"]:
                for view in user["action"]["views_history"]:
                    result.at[user["user"], view] += 2
        return result

    def user_similarity(self, user, thereshold=0.8, movie_dimension=5, result_dimension=3):
        """
        user: string -> The user which we will be searching other simular users
        thereshold: born to accept users on the list
        dimension: Maximum number of movies to calculate the distance
        return a list of users with a similarity score of thereshold or plus
        """
        result = {}
        row = self.matrix.loc[user].nlargest(movie_dimension)
        sub_matrix = self.matrix.drop(user)[row.index]
        sub_matrix = sub_matrix.sub(sub_matrix.mean(axis=1), axis=0)
        for index, row_bis in sub_matrix.iterrows():
            result[index] = spatial.distance.cosine(row.tolist(), row_bis.tolist())
        return pd.Series(data=result, index=list(result)).nlargest(result_dimension).index.tolist()
