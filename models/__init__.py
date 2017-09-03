import time
from pymongo import MongoClient

mongod = MongoClient()


def timestamp():
    return int(time.time())


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'sep': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = mongod.db['data_id']
    new_id = doc.find_and_modify(**kwargs).get('sep')
    return new_id


class Mongod(object):
    @classmethod
    def valid_names(cls):
        names = [
            '_id',
            ('id', int, -1),
            ('deleted', bool, False),
            ('created_time', int, 0),
            ('updated_time', int, 0),
        ]
        return names

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{} = {}'.format(k, v) for k, v in self.__dict__.items())
        return '<{}: \n  {}\n>'.format(class_name, '\n'.join(properties))

    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__
        m = cls()
        names = cls.valid_names().copy()
        names.remove('_id')
        if form is None:
            form = {}

        for f in names:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError

        m.id = next_id(name)

        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        m.deleted = False
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        m = cls()
        names = cls.valid_names().copy()
        names.remove('_id')
        for f in names:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        kwargs['deleted'] = False
        ds = mongod.db[name].find(kwargs)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find_all_unique(cls, unique_key, **kwargs):
        unique_list = []
        l = []
        ds = cls._find(**kwargs)[::-1]
        for d in ds:
            unique_value = d.__dict__[unique_key]
            if unique_value not in unique_list:
                l.append(d)
                unique_list.append(unique_value)
        print('unique reply', l)
        return l

    @classmethod
    def find_one(cls, **kwargs):
        kwargs['deleted'] = False
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    def save(self):
        name = self.__class__.__name__
        mongod.db[name].save(self.__dict__)

    @classmethod
    def delete(cls, id):
        name = cls.__name__
        query = {
            'id': id,
        }
        values = {
            '$set': {
                'deleted': True
            }
        }
        mongod.db[name].update_one(query, values)

    @classmethod
    def delete_all(cls, query):
        name = cls.__name__
        query = query
        values = {
            '$set': {
                'deleted': True
            }
        }
        mongod.db[name].update(query, values)

    @classmethod
    def update(cls, id, form):
        name = cls.__name__

        query = {
            'id': id,
        }
        values = {
            '$set': form
        }
        print('values', values)
        print('before', cls.find(id))
        mongod.db[name].update_one(query, values)
        print('after', cls.find(id))

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d
