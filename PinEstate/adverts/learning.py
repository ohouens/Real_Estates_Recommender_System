from .connect import Connect
from pymongo import MongoClient

import pandas as pd
import numpy as np

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
        result = []
        db = client.grand_paris_estates_users
        cursor = db.inventory.find({})
        for inventory in cursor:
            result.append(inventory["user"])
        return result

    def all_items(self, client):
        result = []
        db = client.grand_paris_estates_unified
        cursor = db.inventory.find({})
        for inventory in cursor:
            result.append(str(inventory["_id"]))
        return result

    def produce_matrix(self, client, users, items):
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
