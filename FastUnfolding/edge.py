__author__ = 'fy'
from vertex import Vertex


class Edge:
    def __init__(self, from_vertex, to_vertex, weight):
        self.from_ = from_vertex
        self.to_ = to_vertex
        self.weight = weight

    @staticmethod
    def get_from_db(from_vertex, to_vertex, db):
        pass

    def set_weight(self, weight):
        self.weight = weight

    def update_weight(self, db):
        result = db.find_one_and_update({"from_value": self.from_.value, "to_value": self.to_.value},
                                        {"$set", {"weight": self.weight}})
        if result is not None:
            return True
        result = db.find_one_and_update({"from_value": self.to_.value, "to_value": self.from_.value},
                                        {"$set", {"weight": self.weight}})
        if result is not None:
            return True
        return False