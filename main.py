from tkinter import *
import pandas
import random

# --------------------------------Constants ------------------------------------#

YELLOW = "#f7f5dd"
FONT_NAME = "Cambria"
current_word = {}
data_dict ={}

#--------------------------Read csv---------------------------#

try:
    data = pandas.read_csv("data/words_to_learn.csv")
    # read from the words_to_learn.csv
    # If opening for first time or this csv is deleted read from the french_words.csv

except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
    # To overcome FileNotFoundError exception, using data from french_words.csv
    # reading csv file using padas.read_csv
    # converting the csv file to dictonary and keeping the orientation to "records"

else:
    # If there is words_to_learn.csv is found, use the data from that csv
    # changiing csv to dictionary and orientation as "records" and assigning to the data_dict file.
    data_dict = data.to_dict(orient="records")
    print(data_dict)




def next_card():
    # Every time user presses ✔ or ❌ button new word is chosen randomly from the csv
    # Pick a random word and assign to current word
    # changing the background image (white image)
    # changing the word in the canvas to current_word["French"] i.e the random french word
    # changing the title in canvas to say as French
    # disable the 3 second flip card timer
    # after changing to next card, it should flip card and show the english meaning

    global current_word , flipcard_timer
    window.after_cancel(flipcard_timer)
    # cancelling the 3 second flip card timer
    current_word = random.choice(data_dict)
    current_frenchword = current_word["French"]
    canvas.itemconfig(language_title,text = "French", fill = "black")
    canvas.itemconfig(language_word,text =f"{current_frenchword}", fill ="black")
    canvas.itemconfig(background_image,image = front_img)
    flipcard_timer = window.after(3000,func=flip_card)
    # once the card is changed to next card, flip to english card after 3 seconds
    
    
    
def flip_card():
    #after 3s the card should change to a english word
    # changing the background image (green image)
    # changing the french word in canvas to the english word
    # changing the french title to "English"
    current_englishword = current_word["English"]
    print(current_englishword)
    canvas.itemconfig(language_title,text ="English", fill= "white")
    canvas.itemconfig(language_word,text = f"{current_englishword}", fill ="white")
    canvas.itemconfig(background_image, image = back_img)
    
    

def known_card():
    # the user must see only unkown cards
    # remove the current card if the user presses the ✔ button
    # new csv file is created called words to learn.csv with only unkown words
    # move to next card, and chose the next card at random from the words to learn csv file
    data_dict.remove(current_word)
    print(len(data_dict))

    data = pandas.DataFrame(data_dict)
    data.to_csv("./data/words_to_learn.csv",index=0)
    # setting index = 0 because everytime close and open the program, the csv file adds index to it.
    next_card()




#--------------------------UI setup---------------------------------#
#TODO create window
window = Tk()
window.title("Flashy cards")
window.config(padx=50,pady=50,bg=YELLOW)

flipcard_timer = window.after(3000,func=flip_card)
# changes the card after every 3 seconds or 3000 milliseconds

#TODO create canvas
canvas = Canvas(width=800,height=526)
back_img = PhotoImage(file= "./images/card_back.png")
front_img = PhotoImage(file= "./images/card_front.png")
background_image = canvas.create_image(0,0,image=front_img,anchor="nw")
language_title = canvas.create_text(400,132,text="Title",font=(FONT_NAME,40,"italic"))
language_word = canvas.create_text(400,300,text="word",font=(FONT_NAME,60))
canvas.config(bg=YELLOW,highlightthickness=0)
canvas.grid(row=0,column=0,columnspan=2)

#TODO create ✔❌ buttons

wrong_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image= wrong_image,highlightthickness=0,bg=YELLOW,command=next_card)
unknown_button.grid(row=1,column=0)

correct_image = PhotoImage(file="images/right.png")
known_button = Button(image=correct_image,highlightthickness=0,bg=YELLOW,command=known_card)
known_button.grid(row=1, column=1)

next_card()



window.mainloop()
