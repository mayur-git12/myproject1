import tkinter
from tkinter import * 
from textblob import TextBlob

root = Tk()
root.tittle("speeling checker")
root.geometry("700x400")
root.config(background="#dae6f6")

def check_spelling():
    WORD=enter_text.get()
    a=TextBlob(WORD)
    RIGHT=str(a.correct())

cs=Label(root,text="correct text is: ",font=("poppins",20),bg="#dae6f6",fg="#364971")
cs.place(x=100,y=250)
spell.config(text=RIGHT)


heading = Label(root,text="spelling checker",font=("truechat MS",30,"bold"),bg="blue",gf="white")
heading.pack(pady =(50,0))

enter_text=Entry(root,justify="center",width=30,font=( "popins",25),bg="white",border=2)
enter_text.pack(pady=10) 
enter_text.focous()

Button=Button(root,text="check",font=("arial",20,"bold"),fg="white",bg="red")
Button.pack()

spell=Label(root,font=("poppins",20),bg="#dae6f6",fg="#364971")
spell.palace(x=350,y=250)

root.mainloop()