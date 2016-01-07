import unittest
import lib.util
import lib.sql
import lib.db

import lib.track
import lib.theme

import lib.plugin
import lib.plugin.deezer


class AmnezicTestCase(unittest.TestCase):
    def setUp(self):
        self.db = lib.sql.Database.singleton()
        self.db.connect()
        self.db.execute_file(lib.db.SCHEMA)
        lib.plugin.source = lib.plugin.deezer.source

    def tearDown(self):
        self.db.disconnect()

    # ##################################################
    # util 

    def test_000_empty_object(self):
        print ' ---------- test_000_empty_object'
        obj = lib.util.Object()
        assert len(obj.__dict__) == 0
        obj = lib.util.Object(None)
        assert len(obj.__dict__) == 0

    def test_001_object(self):
        print ' ---------- test_001_object '
        obj1 = lib.util.Object(name="toto", age=12, keys=[1, "key", dict(key="value")],
                           values=dict(key="value", sub=dict(key="value")))
        obj2 = lib.util.Object(str(obj1))
        obj3 = lib.util.Object(str(obj2))
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
        table = lib.sql.Table('tmp', 'oid', 'json')
        lib.sql.Sql('drop table if exists %s' % table.name).execute()
        lib.sql.Sql('create table %s ( oid text primary key, json text )' % table.name).execute()
        tracks = table.select().fetch_all()
        assert len(tracks) == 0
        track = table.select().fetch_one()
        assert track is None
        table.insert(oid=99, json='{name:"toto",age:42}').execute()
        track = table.select().where(oid=99).fetch_one()
        assert track['oid'] == '99'
        assert track['json'] == '{name:"toto",age:42}'
        lib.sql.Sql('drop table if exists %s' % table.name).execute()

    def test_011_json_sql(self):
        print ' ---------- test_011_json_sql '
        table = lib.sql.Table('tmp', 'oid', 'json')
        lib.sql.Sql('drop table if exists %s' % table.name).execute()
        lib.sql.Sql('create table %s ( oid text primary key, json text )' % table.name).execute()
        tracks = lib.sql.retrieve_all(table)
        assert len(tracks) == 0
        track = lib.sql.search(table, oid=99)
        assert track is None
        track = lib.util.Object(oid=99, name='toto', age=42)
        track = lib.sql.insert(table, track)
        assert track is not None
        assert track.oid == 99
        assert track.name == 'toto'
        assert track.age == 42
        assert track.home is None
        track.name = 'tata'
        track.home = 'nice'
        track = lib.sql.update(table, track)
        assert track is not None
        assert track.oid == 99
        assert track.name == 'tata'
        assert track.age == 42
        assert track.home == 'nice'
        track = lib.sql.delete(table, oid=track.oid)
        assert track is not None
        assert track.oid == 99
        assert track.name == 'tata'
        assert track.age == 42
        assert track.home == 'nice'
        track = lib.sql.search(table, oid=99)
        assert track is None
        lib.sql.Sql('drop table if exists %s' % table.name).execute()

    # ##################################################
    # track

    def test_100_no_track(self):
        print ' ---------- test_100_no_track '
        tracks = lib.track.retrieve_all()
        assert len(tracks) == 0

    def test_101_search_track(self):
        print ' ---------- test_101_search_track '
        tracks = lib.track.search('toto')
        assert len(tracks) != 0
        track = tracks[0]
        assert track.oid is not None
        assert track.title is not None
        assert track.mp3 is not None
        assert track.artist is not None
        assert track.artist.name is not None
        assert track.artist.picture is not None
        assert track.album is not None
        assert track.album.name is not None
        assert track.album.picture is not None
        assert track.genres is None

    def test_102_search_track_by_oid(self):
        print ' ---------- test_102_search_track_by_oid '
        track = lib.track.search_by_oid(549979)
        assert track.oid == 549979
        assert track.title == 'Hold the Line'
        assert track.mp3 is not None
        assert track.album is not None
        assert track.album.name == 'Les Indispensables'
        assert track.album.picture is not None
        assert track.artist is not None
        assert track.artist.name == 'Toto'
        assert track.artist.picture is not None
        assert len(track.genres) != 0
        genre = track.genres[0]
        assert genre.name == 'Pop'
        assert genre.picture is not None

    def test_103_create_track(self):
        print ' ---------- test_103_create_track '
        track = lib.track.create(549979)
        assert track.oid == 549979
        tracks = lib.track.retrieve_all()
        assert len(tracks) == 1
        track = lib.track.retrieve(549979)
        assert track.oid == 549979
        track = lib.track.update(549979)
        assert track.oid == 549979
        assert track.title == 'Hold the Line'
        assert track.mp3 is not None
        assert track.album is not None
        assert track.album.name == 'Les Indispensables'
        assert track.album.picture is not None
        assert track.artist is not None
        assert track.artist.name == 'Toto'
        assert track.artist.picture is not None
        assert len(track.genres) != 0
        genre = track.genres[0]
        assert genre.name == 'Pop'
        assert genre.picture is not None
        track = lib.track.delete(549979)
        assert track.oid == 549979
        tracks = lib.track.retrieve_all()
        assert len(tracks) == 0


    # ##################################################
    # theme

    def _test_110_flow_theme(self):
        print ' ---------- test_110_flow_theme '
        tracks = lib.theme.retrieve_all()
        assert len(tracks) == 0
        track_oid = 549979
        track = lib.track.create(track_oid)
        assert sorted(track.themes) == ['artist::215', 'genre::132', 'year::2006']
        tracks = lib.theme.retrieve_all()
        assert len(tracks) == 3

        track = lib.theme.retrieve('artist::215')
        assert track.oid == 'artist::215'
        assert track.name == ''
        assert track.tracks == [549979]

        track = lib.theme.delete(oid)
        assert track.oid == oid
        tracks = lib.theme.retrieve_all()
        assert len(tracks) == 0

    # ##################################################
    # login

    def login(self, username=None, password=None):
        return self.app.post('/login', data=dict(username=username or 'test', password=password or 'test'),
                             follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def _test_login(self):
        rv = self.login()
        assert lib.amnezic.SUCCESS_LOGIN in rv.data
        rv = self.logout()
        assert lib.amnezic.SUCCESS_LOGOUT in rv.data
        rv = self.login(username='invalid')
        assert lib.amnezic.ERROR_INVALID_LOGIN in rv.data
        rv = self.login(password='invalid')
        assert lib.amnezic.ERROR_INVALID_LOGIN in rv.data

    # ##################################################
    # app

    def _test_200_flow_track(self):
        print ' ---------- test_200_flow_track '
        query = 'toto'
        tracks = lib.track.retrieve_all()
        assert len(tracks) == 0
        tracks = lib.track.search(query=query)
        assert len(tracks) != 0
        oid = 549979
        track = lib.track.search(oid=oid)
        assert track.oid == oid
        track = lib.track.create(oid=oid)
        assert track.oid == oid
        tracks = lib.track.retrieve_all()
        assert len(tracks) == 1
        track = lib.track.retrieve(oid=oid)
        assert track.oid == oid
        track = lib.track.update(oid=oid)
        assert track.oid == oid
        assert track.title == 'Hold the Line'
        assert track.album == 'Les Indispensables'
        assert track.artist == 'Toto'
        assert track.genre == 'Pop'
        assert track.mp3 is not None
        assert track.picture is not None
        assert track.year == 2006
        track = lib.track.delete(oid=oid)
        assert track.oid == oid
        tracks = lib.track.retrieve_all()
        assert len(tracks) == 0

if __name__ == '__main__':
    unittest.main()
