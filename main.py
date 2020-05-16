import tweepy
import config

# Authenticate to Twitter
auth = tweepy.OAuthHandler(config.api["key"], config.api["secret"])
auth.set_access_token(config.access["key"], config.access["secret"])

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


def removeSymbols(word):
    formattedWord = word
    symbolsToRemove = [",", "(", ")", "?", ".", "!",
                       ";", '"', "-", "”", "—", ":"]
    for symbol in symbolsToRemove:
        if symbol in formattedWord:
            formattedWord = formattedWord.replace(symbol, "")
    return formattedWord.lower()


def checkForCommonWords(word):
    commonWords = [
        "the",
        "be",
        "to",
        "of",
        "and",
        "a",
        "in",
        "that",
        "have",
        "it",
        "for",
        "on",
        "with",
        "he",
        "as",
        "at",
        "do",
        "this",
        "but",
        "his",
        "by",
        "from",
        "they",
        "say",
        "she",
        "or",
        "an",
        "will",
        "one",
        "all",
        "we",
        "we're",
        "where",
        "let's",
        "under",
        "would",
        "there",
        "their",
        "what",
        "so",
        "up",
        "out",
        "if",
        "about",
        "who",
        "get",
        "which",
        "go",
        "when",
        "make",
        "can",
        "just",
        "him",
        "know",
        "take",
        "into",
        "your",
        "some",
        "could",
        "them",
        "see",
        "other",
        "than",
        "then",
        "look",
        "only",
        "come",
        "its",
        "over",
        "also",
        "back",
        "after",
        "use",
        "two",
        "how",
        "work",
        "well",
        "way",
        "even",
        "want",
        "new",
        "because",
        "any",
        "these",
        "day",
        "most",
        "her",
        "is",
        "been",
        "much",
        "was",
        "off",
        "are",
        "others",
        "pm",
        "et",
        "no",
        "more",
        "were",
        "through",
        "has",
        "week",
        "may",
        "our",
        "year",
        "weeks",
        "it's",
        "had",
        "another",
        "said",
        "since",
        "says",
        "you",
        "class",
        "during",
        "not",
        "join",
        "last",
        "bcome",
        "going",
        "&amp",
        "part",
        "it's",
        "it’s"
        "that's",
        "still",
        "making",
        "make",
        "already",
        "i've",
        "keep",
        "years",
        "times",
        "too",
        "many",
        "need",
        "long",
        "they're",
        "while",
        "own",
        "should",
        "every",
        "each",
        "here",
        "here's",
        "those",
        "until",
        "ago",
        "now",
        "time",
        "don't",
        "must",
        "around",
    ]
    if "https" in word:
        return True
    for commonWord in commonWords:
        if word == commonWord:
            return True
    return False


account = "BarackObama"

tweets = api.user_timeline(
    screen_name=account, count=3000, include_rts=False, tweet_mode="extended")

words = {}
# add words to word dict
for tweet in tweets:
    for word in tweet.full_text.split():
        # remove some symbols, uncapitalize
        formattedWord = removeSymbols(word)

        # skip meaningless words
        if checkForCommonWords(formattedWord):
            continue

        if formattedWord in words:
            words[formattedWord] = words[formattedWord] + 1
        else:
            words[formattedWord] = 1

for x, y in words.items():
    if y > 5:
        print(f"{x} -> {y}")
