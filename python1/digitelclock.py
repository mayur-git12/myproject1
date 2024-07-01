import tkinter as tk
from time import strftime

root = tk.Tk()
root.title("digitel clock")

def time():
    string = strftime('%H:%M:%S %p \n %D')
    Label.config(text=string)
    Label.after(1000,time) 

Label = tk.Label(root, font=('calibri',50,'bold'), background = "blue",foreground='white') 
Label.pack(anchor='center')

time()

root.mainloop()