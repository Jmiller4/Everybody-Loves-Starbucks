import tweepy
import random
from Secrets import *
import io

# This is a twitter bot whose purpose is to tweet messages about which starbucks drinks people are drinking.
# Everybody loves starbucks!

# AUTHOR (code): Joel Miller
# CONCEPT: Jesi Gaston

def main():

    # Twitter API stuff
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Making the tweet
    random.seed()

    name = pick_random_name()
    drink = pick_random_line("Menu.txt", False)
    tweet = construct_tweet(name, drink)

    api.update_status(tweet)


# This function takes in a baby name and a drink name, and constructs the actual tweet text.
# So this function takes in something like (Alex, Coffee) and outputs "Alex is having a Coffee."
def construct_tweet(name, drink):

    tweet = name
    tweet += " is having a"

    if drink[0] in ['a','e','i','o','u','A','E','I','O','U']:
        tweet += "n "
    else:
        tweet += " "

    tweet += drink + "."

    return tweet


# This function takes in a line from the text file, and removes all the stuff besides the name.
# It also gives the name the appropriate casing (e.g. ALEX --> Alex)
def clean_line(line):

    capitalized_name = line.split()[0]
    normal_name = capitalized_name[0]
    normal_name += capitalized_name[1:len(capitalized_name)].lower()
    return normal_name


# picks a random line out of a text file. It takes in the name/ path of the file, as well as the number of lines in the file.
def pick_random_line(file_name, include_last_line = True):

    file = io.open(file_name, mode="r", encoding="utf-8")
    line_list = file.readlines()

    # for drink names, the last line is a newline, so we don't want to include it.
    if not include_last_line:
        line_list = line_list[0:len(line_list) - 1]

    file.close()

    line = random.choice(line_list)

    # here we take the last character off of the line.
    # this isn't so important for baby names, because those lines will be cleaned more later.
    # but it is important for drink names, which have a newline at the end, and don't get cleaned
    # after being returned from this function.
    line = line[0:len(line)-1]

    return line


# this function returns a random name.
def pick_random_name():

    which_set = random.randint(1,2)
    file_name = "Names" + str(which_set) + ".txt"
    raw_line = pick_random_line(file_name)
    return clean_line(raw_line)


main()

