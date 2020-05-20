import tweepy
import config
from helpers import formatWord, isCommonWord
import tkinter as tk
from tkinter import font

from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

# TKINTER settings
HEIGHT = 600
WIDTH = 900
COLOR = "#00acee"

# font settings
FONT = "Comic Sans MS"
tiny = (FONT, 10)
small = (FONT, 14)
medium = (FONT, 18)
large = (FONT, 22)
xLarge = (FONT, 26)
titleFont = (FONT, 26, "bold italic")
accountTitle = (FONT, 18, "bold")


def clearField(field):
    field.delete('1.0', tk.END)


def getTweets(account, api):
    try:
        return api.user_timeline(screen_name=account, count=3000, include_rts=False, tweet_mode="extended")
    except:
        return False


def changeProfileImage(url):
    u = urlopen(url)
    raw_data = u.read()
    u.close()
    im = Image.open(BytesIO(raw_data))
    photo = ImageTk.PhotoImage(im)
    profileImageLabel.configure(image=photo)
    profileImageLabel.image = photo
    profileImageLabel.place(width=48, height=48)


def outputWords(account, api, outputField):
    outputField.tag_config("tiny", font=tiny)
    outputField.tag_config("small", font=small)
    outputField.tag_config("medium", font=medium)
    outputField.tag_config("large", font=large)
    outputField.tag_config("xLarge", font=xLarge)
    outputField.tag_config("accountTitle", font=accountTitle)
    outputField.config(cursor="arrow")
    outputField.configure(state='normal')

    # clear previous output
    clearField(outputField)

    tweets = getTweets(account, api)

    if tweets:
        changeProfileImage(tweets[0].user.profile_image_url_https)
        words = {}
        # example:
        # words = {
        #     "fake": 10,
        #     "news": 9,
        #     "covid19": 20
        # }

        # add words to words dict
        for tweet in tweets:
            for word in tweet.full_text.split():
                # remove some symbols, uncapitalize
                formattedWord = formatWord(word)

                # skip common words like "the", "and" etc...
                if isCommonWord(formattedWord):
                    continue

                # count words
                if formattedWord in words:
                    words[formattedWord] = words[formattedWord] + 1
                # add new word to dict
                else:
                    words[formattedWord] = 1

        # output user data
        outputField.insert(
            tk.INSERT, tweets[0].user.name + " @" + tweets[0].user.screen_name + "\n", "accountTitle")

        # output words
        for x, y in words.items():
            # show only words that appear atleast 5 times
            if y >= 5:
                if y > 8 and y <= 12:
                    outputField.insert(tk.INSERT, x.upper() + "   ", "small")
                elif y > 12 and y <= 16:
                    outputField.insert(tk.INSERT, x.upper() + "   ", "medium")
                elif y > 16 and y <= 20:
                    outputField.insert(tk.INSERT, x.upper() + "   ", "large")
                elif y > 20:
                    outputField.insert(tk.INSERT, x.upper() + "   ", "xLarge")
                else:
                    outputField.insert(tk.INSERT, x.upper() + "   ", "tiny")
    else:
        # hide image
        profileImageLabel.place(width=0, height=0)

        outputField.insert(
            tk.INSERT, "ERROR - account doesn't exist", "medium")

    outputField.configure(state='disabled')


# Authenticate to Twitter
auth = tweepy.OAuthHandler(config.api["key"], config.api["secret"])
auth.set_access_token(config.access["key"], config.access["secret"])
api = tweepy.API(auth)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


# TKINTER UI
root = tk.Tk()
root.title("TWITTER ACCOUNT WORD STATS")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# image
backgroundImage = tk.PhotoImage(file="background.png")
backgroundLabel = tk.Label(root, image=backgroundImage)
backgroundLabel.image = backgroundImage
backgroundLabel.place(relwidth=1, relheight=1)

# title
title = tk.Label(root, text="TWITTER ACCOUNT WORD STATS",
                 fg="#fff",
                 bg=COLOR,
                 font=titleFont)
title.place(relx=0.5, rely=0.04, anchor="n")

frame = tk.Frame(root, bg=COLOR, bd=5)
frame.place(relx=0.5, rely=0.15, relwidth=0.75, relheight=0.1, anchor="n")

# "@" symbol
entryVar = tk.StringVar(value="@")
entry = tk.Entry(frame, textvariable=entryVar, font=medium)
entry.place(relwidth=0.05, relheight=1)
entry.configure(state='disabled')

# input field
input = tk.Entry(frame, font=medium)
input.place(relx=0.05, relwidth=0.6, relheight=1)

# submit btn
button = tk.Button(frame, text="SUBMIT", font=small,
                   command=lambda: outputWords(input.get(), api, text))
button.place(relx=0.7, relwidth=0.3, relheight=1)

# profile image
profileImageLabel = tk.Label(root)
profileImageLabel.place(rely=0.3, relx=0.095, width=0,
                        height=0, anchor="n")

lowerFrame = tk.Frame(root, bg=COLOR, bd=10)
lowerFrame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor="n")

# output field
text = tk.Text(lowerFrame, wrap=tk.WORD)
text.place(relwidth=1, relheight=1)
text.configure(state='disabled')

root.mainloop()
