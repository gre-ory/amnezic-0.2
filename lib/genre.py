
# ##################################################
# import

import lib.util as util
import lib.sql as sql
import lib.db as db

# ##################################################
# source

source = None

# ##################################################
# actions

def retrieve_all():
    return sql.retrieve_all( db.genre )

def retrieve( oid ):
    return sql.retrieve( db.genre, oid ) 

def create( oid ):
    source is not None or util.throw( 'missing genre source!' )
    obj = source.genre( oid )
    if obj is None:
        util.throw( 'genre %s not found!' % oid )
    sql.insert( db.genre, obj )
    return obj
    
def update( oid ):
    source is not None or util.throw( 'missing genre source!' )
    obj = source.genre( oid )
    if obj is None:
        util.throw( 'genre %s not found!' % oid )
    sql.update( db.genre, obj )
    return obj    

def delete( oid ):
    return sql.delete( db.genre, oid )
        
    