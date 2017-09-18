import flickrapi
import json
from pprint import pprint
import os
import random

class flickrClient(object):
    """Generic Flickr Class for handling flickr API calls."""

    def __init__(self):
        '''Class constructor or initialization method.'''
        #keys and tokens from the Flickr Dev Console
        api_key = os.environ['FLICKR_API_KEY']
        api_secret = os.environ['FLICKR_API_SECRET']

        """Now for all of the talking to Flickr code..."""
        self.api = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
        self.extras = 'url_l'
        # Below is the first attempt to clean up API call in terms of photo size.
        #'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'

    def get_photos(self, text):
        results = self.api.photos.search(text=text, extras=self.extras)
        photos = results['photos']['photo']

        photo_url = []

        while photo_url == []:
            photo = random.choice(photos)
            if "url_l" not in photo:
                print 'NEXT'
            else:
                photo_url.append(photo['url_l'])
                clean_url = str(photo_url).strip('[]u').strip("'")
                print clean_url
                break

        return clean_url