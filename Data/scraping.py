import tweepy
import pandas as pd
import sys

#enter authorization info

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

query = sys.argv[1]

tweets = tweepy.Cursor(api.search, q= query, lang = "en", since = "2020-09-20", tweet_mode = "extended").items(10000)

tweets_info = [[tweet.id, tweet.full_text, tweet.retweet_count, tweet.favorite_count, tweet.user.location, tweet.created_at] for tweet in tweets]
search_results = pd.DataFrame(tweets_info, columns = ["id", "tweet", "retweets", "favorites", "location", "datetime"])

print("number of tweets collected:", len(search_results))
print(search_results.head())

#if file exists remove duplicates and print all results to the file
try:
    prev_result = pd.read_csv(sys.argv[2])
    all_results = pd.concat([prev_result, search_results])
    all_results.drop_duplicates(subset = ["id"], inplace = True)
    print("total tweets:", len(all_results))
    cont = input("Press q to quit or write search results to another file. Press any other key to rewrite given file with all results: ")
    if cont == "q":
        sys.exit()

    all_results.to_csv(sys.argv[2], index = False)
    print("File present")

except SystemExit:
    new_file = input("Enter new file name or q to quit: ")
    if new_file == "q":
        sys.exit()
    else:
        search_results.to_csv(new_file, index = False)

#if file does not exist save to new file
except:
    search_results.to_csv(sys.argv[2], index=False)
    print("Created new file")



