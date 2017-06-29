__author__ = 'fy'


class Vertex:
    def __init__(self, value):
        self.value = value
        self.community = -1
        self.modularity = 0
        self.degree = 0

    def degree_incr(self):
        self.degree += 1

    def set_community(self, community, modularity):
        self.community = community
        self.modularity = modularity

    @staticmethod
    def get_vertex_from_db(db, value):
        return db.find_one({"value": value})

    def update_vertex(self, db):
        db.find_one_and_update({"value": self.value},
                               {"community": self.community, "modularity": self.modularity, "degree": self.degree})