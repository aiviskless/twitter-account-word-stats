import tweepy
import config
from helpers import formatWord, checkForCommonWords

import tkinter as tk
from tkinter import font

from PIL import Image, ImageTk
import urllib
import io
from io import BytesIO
import requests

# Authenticate to Twitter
auth = tweepy.OAuthHandler(config.api["key"], config.api["secret"])
auth.set_access_token(config.access["key"], config.access["secret"])

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


HEIGHT = 500
WIDTH = 900


def getWords(account):
    print("Button clicked!", account)
    string = ""

    try:
        # get tweets
        tweets = api.user_timeline(
            screen_name=account, count=3000, include_rts=False, tweet_mode="extended")
        words = {}

        cover = tweets[0].user.profile_image_url
        print(cover)
        u = urllib.urlopen(cover)
        print("1")
        raw_data = u.read()
        print("2")
        u.close()
        print("3")

        im = Image.open(BytesIO(raw_data))
        print("4")
        image = ImageTk.PhotoImage(im)
        print("5")
        label = tk.Label(image=image)
        print("6")
        label.pack()

        # add words to words dict
        for tweet in tweets:
            for word in tweet.full_text.split():
                # remove some symbols, uncapitalize
                formattedWord = formatWord(word)

                # skip meaningless words
                if checkForCommonWords(formattedWord):
                    continue

                # count words
                if formattedWord in words:
                    words[formattedWord] = words[formattedWord] + 1
                # add new word to dict
                else:
                    words[formattedWord] = 1

        text.tag_config("a", font=("Helvetica", 10))
        text.tag_config("b", font=("Helvetica", 14))
        text.tag_config("c", font=("Helvetica", 18))
        text.tag_config("d", font=("Helvetica", 22))
        text.tag_config("e", font=("Helvetica", 26))
        text.config(cursor="arrow")

        # simple print
        for x, y in words.items():
            if y > 5:
                if y > 8 and y <= 12:
                    text.insert(tk.INSERT, x + "  ", "b")
                elif y > 12 and y <= 16:
                    text.insert(tk.INSERT, x + " ", "c")
                elif y > 16 and y <= 20:
                    text.insert(tk.INSERT, x + " ", "d")
                elif y > 20:
                    text.insert(tk.INSERT, x + " ", "e")
                else:
                    text.insert(tk.INSERT, x + " ", "a")

    except:
        string = "Error"

    # output to label
    # label["text"] = string
    # text.tag_config("a", foreground="blue", underline=1)
    # text.config(cursor="arrow")
    # text.insert(tk.INSERT, string, "a")


root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# backgroundImage = tk.PhotoImage(
#     file="https://pbs.twimg.com/profile_images/508960761826131968/LnvhR8ED_normal.png")
# backgroundLabel = tk.Label(root, image=backgroundImage)
# backgroundLabel.image = backgroundImage
# backgroundLabel.place(relwidth=1, relheight=1)
url = "https://pbs.twimg.com/profile_images/508960761826131968/LnvhR8ED_normal.png"
response = requests.get(url)
im = Image.open(BytesIO(response.content))
print(im)
backgroundImage = ImageTk.PhotoImage(im)
backgroundLabel = tk.Label(image=backgroundImage)
backgroundLabel.place(relwidth=1, relheight=1, anchor="n")

frame = tk.Frame(root, bg="#80c1ff", bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="n")

entry = tk.Entry(frame, font=("Helvetica", 16))
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Submit", font=("Helvetica", 16),
                   command=lambda: getWords(entry.get()))
button.place(relx=0.7, relwidth=0.3, relheight=1)

lowerFrame = tk.Frame(root, bg="#80c1ff", bd=10)
lowerFrame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor="n")

label = tk.Label(lowerFrame, font=("Helvetica", 12),
                 anchor="nw", justify="left", bd=4)
label.place(relwidth=1, relheight=1)


text = tk.Text(label)
text.place(relwidth=1, relheight=1)
text.pack()

root.mainloop()
