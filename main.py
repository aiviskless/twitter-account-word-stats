import tweepy
import config
from helpers import formatWord, isCommonWord

import tkinter as tk
from tkinter import font
from tkinter.ttk import Progressbar

HEIGHT = 600
WIDTH = 900

COLOR = "#00acee"

# font settings
FONT = "Verdana"
tiny = (FONT, 10)
small = (FONT, 14)
medium = (FONT, 18)
large = (FONT, 22)
xLarge = (FONT, 26)
titleFont = FONT + " 26 bold italic"

# Authenticate to Twitter
auth = tweepy.OAuthHandler(config.api["key"], config.api["secret"])
auth.set_access_token(config.access["key"], config.access["secret"])
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


def clearField(field):
    field.delete('1.0', tk.END)


def getWords(account):
    text.tag_config("a", font=tiny)
    text.tag_config("b", font=small)
    text.tag_config("c", font=medium)
    text.tag_config("d", font=large)
    text.tag_config("e", font=xLarge)
    text.config(cursor="arrow")

    text.configure(state='normal')
    # clear previous output
    clearField(text)

    print("Button clicked!", account)

    tweets = []
    try:
        # get tweets
        tweets = api.user_timeline(
            screen_name=account, count=3000, include_rts=False, tweet_mode="extended")
    except:
        text.configure(state='normal')
        text.insert(tk.INSERT, "ERROR - account doesn't exist", "a")
        text.configure(state='disabled')

    if tweets:
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

        # clear previous output
        clearField(text)

        # output words
        for x, y in words.items():
            if y >= 5:
                if y > 8 and y <= 12:
                    text.insert(tk.INSERT, x.upper() + "   ", "b")
                elif y > 12 and y <= 16:
                    text.insert(tk.INSERT, x.upper() + "   ", "c")
                elif y > 16 and y <= 20:
                    text.insert(tk.INSERT, x.upper() + "   ", "d")
                elif y > 20:
                    text.insert(tk.INSERT, x.upper() + "   ", "e")
                else:
                    text.insert(tk.INSERT, x.upper() + "   ", "a")

        text.configure(state='disabled')


# TKINTER
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
                   command=lambda: getWords(input.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

lowerFrame = tk.Frame(root, bg=COLOR, bd=10)
lowerFrame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor="n")

# output field
text = tk.Text(lowerFrame, wrap=tk.WORD)
text.place(relwidth=1, relheight=1)
text.configure(state='disabled')

root.mainloop()
