import flickrapi
import json
from pprint import pprint
import os

class flickrClient(object):
    """Generic Flickr Class for handling flickr API calls."""

    def __init__(self):
        '''Class constructor or initialization method.'''
        #keys and tokens from the Flickr Dev Console
        api_key = os.environ['FLICKR_API_KEY']
        api_secret = os.environ['FLICKR_API_SECRET']
        

            #PROBABLY NEED TO PUT AUTHENTICATION STUFF HERE. NOT SURE HOW.

        """Now for all of the talking to Flickr code..."""
        self.api = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
        self.extras = 'url_l'
        #'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'

    def get_photos(self, text, per_page):
        results = self.api.photos.search(text=text, per_page=per_page, extras=self.extras)
        photos = results['photos']['photo']

        photo_url = []

        for photo in photos:
            if "url_l" in photo:
                photo_url.append(photo['url_l'])
            else:
                print "NOTHING TO SEE HERE"

        return photo_url 
    # def clean_photos(self):



    #     pprint(self.get_photos())

# code reminder for later...
# i = 0
# results = []
# while results == []:
# results = flickr.get_photos('happy', i)
# i += 1