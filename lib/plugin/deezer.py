
# ##################################################
# import

import urllib2

import lib.util as util

import lib.plugin.source as source

# ##################################################
# Deezer

class Deezer( source.Source ):

    # ##################################################
    # constructor
    
    def __init__( self ):
        source.Source.__init__( self )
        self._host = 'https://api.deezer.com'

    # ##################################################
    # helper
    
    def _adi( self, deezer_track, full_mode=False ):
        obj = util.Object()
        obj.source = 'deezer'
        obj.oid = deezer_track.id
        obj.title = deezer_track.title
        obj.available = 'FR' in ( deezer_track.available_countries or [] )
        obj.mp3 = deezer_track.preview
        obj.artist = deezer_track.artist.name
        
        if full_mode:
            deezer_album = self._album( deezer_track.album.id )
            deezer_album is not None or util.throw( 'album %s not found!' % deezer_track.album.id )
            obj.album = deezer_album.title
            obj.picture = deezer_album.cover
    
            deezer_genre = self._genre( deezer_album.genre_id )        
            deezer_genre is not None or util.throw( 'album %s not found!' % deezer_album.genre_id )
            obj.genre = deezer_genre.name
        
        else:
            obj.album = deezer_track.album.title
            obj.picture = deezer_track.album.cover
        
        return obj    
    
    def _fetch( self, request_url ):
        response = None
        try:
            print request_url        
            response = urllib2.urlopen( request_url )
            response_str = response.read().decode( 'utf-8' )
            response_object = util.Object( response_str )
            return response_object
        finally:
            if response is not None:
                response.close()

    def _search_url( self, query ):
        return '%s/search?q=%s' % ( self._host, query )

    def _get_url( self, *args ):
        return '%s/%s' % ( self._host, '/'.join( [ str( arg ) for arg in args ] ) )

    def _get( self, *args ):
        return self._fetch( self._get_url( *args ) )

    def _artist( self, oid ):
        return self._get( 'artist', oid )
    
    def _album( self, oid ):
        return self._get( 'album', oid )
        
    def _genre( self, oid ):
        return self._get( 'genre', oid )    
        
    # ##################################################
    # interface

    def search( self, query ):
        return [ self._adi( track, full_mode=False ) for track in self._fetch( self._search_url( query ) ).data ]
    
    def track( self, oid ):
        return self._adi( self._get( 'track', oid ), full_mode=True )

# ##################################################
# interface

source = Deezer()
    