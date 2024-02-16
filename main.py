import tkinter as tk
import pandas
import random

#background color
BACKGROUND_COLOR = "#B1DDC6"

#current word on flash card
current_words={}


#Reading the translations from csv files

try:
    data=pandas.read_csv("./data/to_learn.csv")
except FileNotFoundError as e:
    print(e)
    data=pandas.read_csv("./data/french_words.csv")
    list_of_translations=data.to_dict(orient="records")
else:
    list_of_translations=data.to_dict(orient="records")


#new card
def new_card():
    global current_words,flip_timer
    window.after_cancel(flip_timer)
    current_words=random.choice(list_of_translations)
    global english_word
    global french_word
    french_word=current_words["French"]
    english_word=current_words["English"]
    canvas.itemconfig(image,image=front_image)
    canvas.itemconfig(language,text="French")
    canvas.itemconfig(word,text=french_word)
    flip_timer=window.after(3000,func=flip)


#right_click
def right_click():
    data=pandas.read_csv("./data/french_words.csv")
    list_of_translations=data.to_dict(orient="records")
    list_of_translations.remove(current_words)
    dataframe=pandas.DataFrame(list_of_translations)
    dataframe.to_csv("./data/to_learn.csv",index=False)
    new_card()


#flip card
def flip():
    global back_image
    canvas.itemconfig(image,image=back_image)
    canvas.itemconfig(language,text="English")
    canvas.itemconfig(word,text=english_word)


#UI
    
#window configuration
window=tk.Tk()
window.title("Flashcards")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip)

#images to be used
back_image=tk.PhotoImage(file="./images/card_back.png")
front_image=tk.PhotoImage(file="./images/card_front.png")

#canvas
canvas=tk.Canvas(height=526,width=800,highlightthickness=0,bg=BACKGROUND_COLOR)

#flashcard
image=canvas.create_image(410,270,image=front_image)
canvas.grid(column=0,row=0,columnspan=2)
language=canvas.create_text(410,150,text="Language",font=("Ariel",40,"italic"))
word=canvas.create_text(410,270,text="Word",font=("Ariel",60,"bold"))

#wrong button
wrong_image=tk.PhotoImage(file="./images/wrong.png")
wrong_button=tk.Button(image=wrong_image,highlightthickness=0,borderwidth=0,command=new_card)
wrong_button.grid(row=1,column=0)

#right button
right_image=tk.PhotoImage(file="./images/right.png")
right_button=tk.Button(image=right_image,highlightthickness=0,borderwidth=0,command=right_click)
right_button.grid(row=1,column=1)

new_card()
window.mainloop()