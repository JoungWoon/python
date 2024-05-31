from tkinter import Tk, Button, messagebox

def btn_click():
    messagebox.showinfo("Message", "Button Clicked!")

window = Tk()
window.title("My First Tkinter App")
window.geometry("300x200")

button = Button(window, text="Click Me", command=btn_click)
button.pack()

window.mainloop()