from models import Mongod
from models.reply import Reply


class Topic(Mongod):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names += [
            ('title', str, ''),
            ('content', str, ''),
            ('board_id', int, 0),
            ('user_id', int, 0),
            ('views', int, 0),
        ]
        return names

    @classmethod
    def get(cls, id):
        t = cls.find(id)
        t.views += 1
        t.save()
        return t

    def user(self):
        from models.user import User
        u = User.find(self.user_id)
        return u

    def replies(self):
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def last_reply(self):
        rs = self.replies()
        if rs:
            r = rs[-1]
        else:
            r = None
        return r

    def reply_count(self):
        count = len(self.replies())
        return count
