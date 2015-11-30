
# ##################################################
# import

import json

# ##################################################
# throw

def throw( message ):
    raise Exception( message )

# ##################################################
# object

class Object( object ):

    # ##################################################
    # constructor
    
    def __init__( self, *args, **kwargs ):
        self.update( *args, **kwargs )
                
    # ##################################################
    # as object

    def __setattr__( self, name, value ):
        self.__dict__[ name ] = value
    
    def __getattr__( self, name ):
        return None    
        
    # ##################################################
    # as dict
    
    def _sanitize( self, value ):
        if value is None:
            return None
        if hasattr( value, '__dict__' ):
            value = value.__dict__        
        if isinstance( value, list ):
            return [ self._sanitize( v ) for v in value ]
        if isinstance( value, tuple ):
            return ( self._sanitize( v ) for v in value )            
        if isinstance( value, dict ):
            value = Object( **value )
        return value

    def update( self, *args, **kwargs ):
        for arg in args:
            if arg is not None:
                for ( key, value ) in json.loads( str( arg ) ).iteritems():
                    self.__dict__[ key ] = self._sanitize( value )
        for ( key, value ) in kwargs.iteritems():
            self.__dict__[ key ] = self._sanitize( value )
    
    def keys( self ):
        return sorted( self.__dict__.keys() )
        
    def __setitem__( self, key, value ):
        self.__dict__[ key ] = value

    def __getitem__( self, key ):
        return self.__dict__[ key ] if self.__dict__.has_key( key ) else None    
 
    # ##################################################
    # output

    @property
    def indented_json( self ):
        return json.dumps( self, default=lambda o: o.__dict__, sort_keys=True, indent=4, separators=( ',', ': ' ) )
    
    @property
    def json( self ):
        return json.dumps( self, default=lambda o: o.__dict__, sort_keys=True, separators=(',',':') )
        
    def __str__( self ):
        return self.json
   