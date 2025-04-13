import tkinter as tk
import time 
#git add .
#git commit -m "name"
#git push

root = tk.Tk()

root.title("Timer")
root.geometry("800x800")

def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    label_time.config(text=hour + ":" + minute + ":" + second)
    label_time.after(1000, clock)

label_time = tk.Label(root, text="time", font=("Arial", 50))
label_time.pack()

clock()
root.mainloop()
