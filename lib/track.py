
# ##################################################
# import

import lib.util as util
import lib.sql as sql
import lib.db as db

# ##################################################
# source

source = None

# ##################################################
# json

def search( oid=None, query=None ):
    source is not None or util.throw( 'missing track source!' )
    if oid is not None:
        return source.track( oid )
    else:
        return source.search( query )

def retrieve_all():
    return sql.retrieve_all( db.track ) 

def retrieve( oid ):
    return sql.retrieve( db.track, oid ) 

def create( oid ):
    source is not None or util.throw( 'missing track source!' )
    obj = source.track( oid )
    if obj is None:
        util.throw( 'track %s not found!' % oid )
    sql.insert( db.track, obj )
    return obj
    
def update( oid ):
    source is not None or util.throw( 'missing track source!' )
    obj = source.track( oid )
    if obj is None:
        util.throw( 'track %s not found!' % oid )
    sql.update( db.track, obj )
    return obj    

def delete( oid ):
    return sql.delete( db.track, oid )    
   