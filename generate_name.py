import os
import random
import tweepy
import datetime
from textgenrnn import textgenrnn

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line.rstrip("\n\r")


def indefinite_article(ch):
    if ch.lower() in ["a", "e", "i", "o"]:
        return "an"
    else:
        return "a"


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


textgen = textgenrnn()

# textgen.train_from_file('data/bands.txt', num_epochs=1)
# textgen.save('metal_bands.hdf5')

textgen = textgenrnn('weights/bands.hdf5')
band_name = textgen.generate(1, return_as_list=True, temperature=0.8)[0]

user = api.me()


f = open("data/hashtags.txt")
genre = random_line(f)
f.close()

tweet = "{}, {} {} band".format(
    band_name,
    indefinite_article(genre[1]),
    genre
)

print("{} - Posting to {}: \"{}\"".format(
    datetime.datetime.now(),
    user.name,
    tweet)
)

api.update_status(tweet)
