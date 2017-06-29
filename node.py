import plyvel
import json


class Node:

    def __init__(self, db_path='./db'):
        self.db = plyvel.DB(db_path, create_if_missing=True)
        self.node_info = NodeInfo.from_json(self.db.get(b'node_info'))

