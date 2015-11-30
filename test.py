import os
import unittest

import lib.util as util
import lib.sql as sql
import lib.db as db

class AmnezicTestCase( unittest.TestCase ):

    def setUp( self ):
        print 'setup'
        self.db = sql.Database.singleton()
        self.db.connect()

    def tearDown( self ):
        print 'teardown'
        self.db.disconnect()

    # ##################################################
    # util 

    def test_empty_object( self ):
        obj = util.Object()
        assert len( obj.__dict__ ) == 0
        obj = util.Object( None )
        assert len( obj.__dict__ ) == 0
    
    def test_object( self ):
        obj1 = util.Object( name="toto", age=12, keys=[1,"key",dict(key="value")], values=dict(key="value", sub=dict(key="value")) )
        obj2 = util.Object( str( obj1 ) )
        obj3 = util.Object( str( obj2 ) )
        for obj in [ obj1, obj2, obj3 ]:
            assert obj.name == "toto"
            assert obj.age == 12
            assert len( obj.keys ) == 3
            assert obj.keys[0] == 1
            assert obj.keys[1] == "key"
            assert obj.keys[2].key == "value"
            assert obj.values.key == "value"
            assert obj.values.sub.key == "value"
            try:
                assert str( obj ) == '{"age":12,"keys":[1,"key",{"key":"value"}],"name":"toto","values":{"key":"value","sub":{"key":"value"}}}'
            except:
                print str( obj )
                raise
    
    # ##################################################
    # login

    def login( self, username=None, password=None ):
        return self.app.post( '/login', data=dict( username=username or 'test', password=password or 'test' ), follow_redirects=True)

    def logout( self ):
        return self.app.get('/logout', follow_redirects=True)
            
    def _test_login( self ):
        rv = self.login()
        assert amnezic.SUCCESS_LOGIN in rv.data
        rv = self.logout()
        assert amnezic.SUCCESS_LOGOUT in rv.data
        rv = self.login( username='invalid' )
        assert amnezic.ERROR_INVALID_LOGIN in rv.data
        rv = self.login( password='invalid' )
        assert amnezic.ERROR_INVALID_LOGIN in rv.data
                
    # ##################################################
    # track

    def _test_no_track( self ):       
        rv = self.app.get( '/track' )
        assert amnezic.SUCCESS_TRACK_LIST_EMPTY in rv.data

    def _test_create_track( self ):       
        self.login( 'admin', 'default' )
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data
        
if __name__ == '__main__':
    unittest.main()