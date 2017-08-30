import giphypop
# import os

# class giphyClient(object):
#     """Class for calling giphy api and then methods for doing
#     cool stuff with it."""

#     def __init__(self):
#         """Class constructor OR initialization method."""
#         #didn't make this key secret because it is a public API key used
#         #for the purposed of developing applications.
#         # api_key = dc6zaTOxFJmz

# g = giphypop.Giphy()

def get_giphy(text):

    img = giphypop.translate(text)
    return img.media_url





