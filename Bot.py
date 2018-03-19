import tweepy
import random
from Secrets import *
import io

# This is a twitter bot whose purpose is to tweet messages about which starbucks drinks people are drinking.
# Everybody loves starbucks.

# AUTHOR (code): Joel Miller
# CONCEPT: Jesi Gaston

#this variable represents wether we go through names alphabetically or not (if not, we choose randomly).
alphabetically = True

# One execution of main() posts one tweet.
def main():

    # Log in to twitter
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)

    # Make the tweet
    random.seed()
    name = choose_baby_name(alphabetically)
    drink = pick_random_line("Menu.txt", False)
    tweet = construct_tweet(name, drink)

    # Post the tweet
    api.update_status(tweet)

# this function chooses a baby name, either moving alphabetically down a list of names or choosing one randomly.
# in_order should be a boolean that represents whether or not the names are being chose in order.
def choose_baby_name(in_order):

    if in_order:
        # first, we need to figure out where in the list of names we are. To help with that, the bot maintains a file
        # called log.txt which just holds the current line number. It will start at 0.
        log_file = open("log.txt", 'r+')
        line_number = int(log_file.readline().split()[0])

        # retrieve the appropriate name from the alphabetical list of names
        name_file = open("Names3.txt")
        name_lines = name_file.readlines()
        name = name_lines[line_number].split()[0]
        name_file.close()

        # write the next line number to the log file
        next_line = (line_number + 1) % (len(name_lines) - 1)
        log_file.seek(0)
        log_file.truncate()
        log_file.write(str(next_line))
        log_file.close()

    else:
        name = pick_random_name()

    return name


# This function takes in a baby name and a drink name, and constructs the actual tweet text.
# So this function takes in something like (Alex, Coffee) and outputs "Alex is having a Coffee."
def construct_tweet(name, drink):

    tweet = name
    tweet += " loves the "

    # This was from when the tweets had different syntax. I'm keeping this in just in case we decide to go back.
    #
    # # Here, we make sure that our sentence is grammatically correct.
    # if drink[0] in ['a','e','i','o','u','A','E','I','O','U']:
    #     tweet += "n "
    # else:
    #     tweet += " "

    tweet += drink + "."

    return tweet


# This function takes in a line from Names1 or Names2.txt and removes all the stuff besides the name.
# It also gives the name the appropriate casing (e.g. ALEX --> Alex)
def clean_line(line):

    capitalized_name = line.split()[0]
    normal_name = capitalized_name[0] + capitalized_name[1:].lower()
    return normal_name


# This function picks a random line out of a text file. It takes in the name/ path of the file,
# and an optional parameter to ignore the last line of the file.
def pick_random_line(file_name, include_last_line = True):

    file = io.open(file_name, mode="r", encoding="utf-8")
    line_list = file.readlines()

    # for drink names, the last line is blank, so we don't want to include it
    # (include_last_line will be passed in as false).
    if not include_last_line:
        line_list = line_list[0:len(line_list) - 1]

    file.close()

    line = random.choice(line_list)

    # here we take the last character off of the line.
    # this isn't so important for baby names, because those lines will be cleaned more later.
    # but it is important for drink names, which have a newline character at the end,
    # and don't get cleaned after being returned from this function.
    line = line[0:len(line)-1]

    return line


# this function returns a random name.
def pick_random_name():

    which_set = random.randint(1,2)
    file_name = "Names" + str(which_set) + ".txt"
    raw_line = pick_random_line(file_name)
    return clean_line(raw_line)

main()
