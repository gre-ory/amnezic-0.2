import unittest
import lib.util as util
import lib.sql as sql
import lib.db as db
import lib.track as track
import lib.plugin.deezer as deezer


class AmnezicTestCase(unittest.TestCase):
    def setUp(self):
        self.db = sql.Database.singleton()
        self.db.connect()
        self.db.execute_file(db.SCHEMA)
        track.source = deezer.source

    def tearDown(self):
        self.db.disconnect()

    # ##################################################
    # util 

    def test_000_empty_object(self):
        print ' ---------- test_000_empty_object'
        obj = util.Object()
        assert len(obj.__dict__) == 0
        obj = util.Object(None)
        assert len(obj.__dict__) == 0

    def test_001_object(self):
        print ' ---------- test_001_object '
        obj1 = util.Object(name="toto", age=12, keys=[1, "key", dict(key="value")],
                           values=dict(key="value", sub=dict(key="value")))
        obj2 = util.Object(str(obj1))
        obj3 = util.Object(str(obj2))
        for obj in [obj1, obj2, obj3]:
            assert obj.name == "toto"
            assert obj.age == 12
            assert len(obj.keys) == 3
            assert obj.keys[0] == 1
            assert obj.keys[1] == "key"
            assert obj.keys[2].key == "value"
            assert obj.values.key == "value"
            assert obj.values.sub.key == "value"
            try:
                assert str(obj) == '{"age":12,"keys":[1,"key",{"key":"value"}],\
"name":"toto","values":{"key":"value","sub":{"key":"value"}}}'
            except:
                print str(obj)
                raise

    # ##################################################
    # sql

    def test_010_sql(self):
        print ' ---------- test_010_sql '
        table = sql.Table('tmp', 'oid', 'json')
        sql.Sql('drop table if exists %s' % table.name).execute()
        sql.Sql('create table %s ( oid text primary key, json text )' % table.name).execute()
        items = table.select().fetch_all()
        assert len(items) == 0
        item = table.select().fetch_one()
        assert item is None
        table.insert(oid=99, json='{name:"toto",age:42}').execute()
        item = table.select().where(oid=99).fetch_one()
        assert item['oid'] == '99'
        assert item['json'] == '{name:"toto",age:42}'
        sql.Sql('drop table if exists %s' % table.name).execute()

    def test_011_json_sql(self):
        print ' ---------- test_011_json_sql '
        table = sql.Table('tmp', 'oid', 'json')
        sql.Sql('drop table if exists %s' % table.name).execute()
        sql.Sql('create table %s ( oid text primary key, json text )' % table.name).execute()
        items = sql.retrieve_all(table)
        assert len(items) == 0
        item = sql.search(table, oid=99)
        assert item is None
        item = util.Object(oid=99, name='toto', age=42)
        item = sql.insert(table, item)
        assert item is not None
        assert item.oid == 99
        assert item.name == 'toto'
        assert item.age == 42
        assert item.home is None
        item.name = 'tata'
        item.home = 'nice'
        item = sql.update(table, item)
        assert item is not None
        assert item.oid == 99
        assert item.name == 'tata'
        assert item.age == 42
        assert item.home == 'nice'
        item = sql.delete(table, oid=item.oid)
        assert item is not None
        assert item.oid == 99
        assert item.name == 'tata'
        assert item.age == 42
        assert item.home == 'nice'
        item = sql.search(table, oid=99)
        assert item is None
        sql.Sql('drop table if exists %s' % table.name).execute()

    # ##################################################
    # track

    def test_100_flow_track(self):
        print ' ---------- test_100_create_track '
        query = 'toto'
        items = track.retrieve_all()
        assert len(items) == 0
        items = track.search(query=query)
        assert len(items) != 0
        oid = 549979
        item = track.search(oid=oid)
        assert item.oid == oid
        item = track.create(oid=oid)
        assert item.oid == oid
        items = track.retrieve_all()
        assert len(items) == 1
        item = track.retrieve(oid=oid)
        assert item.oid == oid
        item = track.update(oid=oid)
        assert item.oid == oid
        assert item.title == 'Hold the Line'
        assert item.album == 'Les Indispensables'
        assert item.artist == 'Toto'
        assert item.genre == 'Pop'
        assert item.mp3 is not None
        assert item.picture is not None
        item = track.delete(oid=oid)
        assert item.oid == oid
        items = track.retrieve_all()
        assert len(items) == 0

    # ##################################################
    # login

    def login(self, username=None, password=None):
        return self.app.post('/login', data=dict(username=username or 'test', password=password or 'test'),
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def _test_login(self):
        rv = self.login()
        assert amnezic.SUCCESS_LOGIN in rv.data
        rv = self.logout()
        assert amnezic.SUCCESS_LOGOUT in rv.data
        rv = self.login(username='invalid')
        assert amnezic.ERROR_INVALID_LOGIN in rv.data
        rv = self.login(password='invalid')
        assert amnezic.ERROR_INVALID_LOGIN in rv.data


if __name__ == '__main__':
    unittest.main()
