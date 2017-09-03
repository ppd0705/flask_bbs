from models import Mongod
from models.topic import Topic

import hashlib


class User(Mongod):
    @classmethod
    def valid_names(cls):
        names = super().valid_names()
        names += [
            ('username', str, ''),
            ('password', str, ''),
            ('signature', str, '这家伙很懒，什么个性签名都没有留下。'),
            ('user_image', str, '/user/avatar/default.png'),
        ]
        return names

    def topics(self):
        ms = Topic.find_all(user_id=self.id)
        return ms

    def replies(self):
        from models.reply import Reply
        ms = Reply.find_all(user_id=self.id)
        return ms

    def unique_replies(self):
        from models.reply import Reply
        ms = Reply.find_all_unique('topic_id', user_id=self.id)
        return ms

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        """$!@><?>HUI&DWQa`"""
        salted = password + salt
        hash = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash

    def validate_change_pwd(self, old_pwd, new_pwd):
        if self.password == self.salted_password(old_pwd) and len(new_pwd) > 2:
            self.password = self.salted_password(new_pwd)
            self.save()
            return True
        else:
            return False

    def validate_change_name(self, name, signature):
        if len(signature) > 0:
            self.signature = signature
            self.save()
        if self.username != name and self.find_by(username=name) is None and len(name) > 2:
            self.username = name
            self.save()
            return True
        else:
            return False

    @classmethod
    def validate_login(self, form):
        username = form.get('username', '')
        pwd = form.get('password', '')
        u = User.find_by(username=username)
        if u is not None and u.password == self.salted_password(pwd):
            return u
        else:
            return None

    @classmethod
    def validate_register(self, form):
        username = form.get('username', '')
        pwd = form.get('password', '')
        u = User.find_by(username=username)
        valid = u is None and len(username) > 2 and len(pwd) > 2
        if valid:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return True
        else:
            return False
