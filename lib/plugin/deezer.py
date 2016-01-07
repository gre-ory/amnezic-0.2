# ##################################################
# import

import urllib2

import lib.util
import lib.plugin


# ##################################################
# DeezerSource

class DeezerSource(lib.plugin.Source):

    # ##################################################
    # constructor

    def __init__(self):
        lib.plugin.Source.__init__(self)
        self._host = 'https://api.deezer.com'

    # ##################################################
    # helper

    def _fetch(self, request_url):
        response = None
        try:
            request_url = '%s/%s' % (self._host, request_url)
            print request_url
            response = urllib2.urlopen(request_url)
            response_str = response.read().decode('utf-8')
            response_object = lib.util.Object(response_str)
            return response_object
        finally:
            if response is not None:
                response.close()

    # ##################################################
    # interface

    def search(self, query):
        return [self.track(deezer_track=deezer_track) for deezer_track in self._fetch('search?q=%s' % query).data]

    def track(self, oid=None, deezer_track=None):
        oid is not None or deezer_track is not None or lib.util.throw('missing track oid!')
        deezer_track = self._fetch('track/%s' % oid) if oid is not None else deezer_track
        track = lib.util.Object()
        track.source = 'deezer'
        track.oid = deezer_track.id
        track.title = deezer_track.title
        track.available = 'FR' in (deezer_track.available_countries or [])
        track.mp3 = deezer_track.preview
        track.artist = self.artist(deezer_artist=deezer_track.artist)
        track.album = self.album(deezer_album=deezer_track.album)

        # full mode > retrieve genres
        if oid is not None:
            deezer_album = self._fetch('album/%s' % track.album.oid)
            track.genres = [self.genre(deezer_genre=deezer_genre) for deezer_genre in deezer_album.genres.data]

        return track

    def artist(self, oid=None, deezer_artist=None):
        oid is not None or deezer_artist is not None or lib.util.throw('missing artist oid!')
        deezer_artist = self._fetch('album/%s' % oid) if oid is not None else deezer_artist
        artist = lib.util.Object()
        artist.oid = deezer_artist.id
        artist.name = deezer_artist.name
        artist.picture = deezer_artist.picture
        return artist

    def album(self, oid=None, deezer_album=None):
        oid is not None or deezer_album is not None or lib.util.throw('missing album oid!')
        deezer_album = self._fetch('album/%s' % oid) if oid is not None else deezer_album
        album = lib.util.Object()
        album.oid = deezer_album.id
        album.name = deezer_album.title
        album.picture = deezer_album.cover
        return album

    def genre(self, oid=None, deezer_genre=None):
        oid is not None or deezer_genre is not None or lib.util.throw('missing genre oid!')
        deezer_genre = self._fetch('genre/%s' % oid) if oid is not None else deezer_genre
        genre = lib.util.Object()
        genre.oid = deezer_genre.id
        genre.name = deezer_genre.name
        genre.picture = deezer_genre.picture
        return genre

# ##################################################
# interface

source = DeezerSource()
