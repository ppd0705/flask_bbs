from models import Mongod


class Board(Mongod):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names += [
            ('title', str, ''),
        ]
        return names
