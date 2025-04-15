import tkinter as tk
import time 
from tkinter import StringVar, messagebox
#git add .
#git commit -m "name"
#git push

root = tk.Tk()

root.title("Timer")
root.geometry("800x800")

#display clock
def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    label_time.config(text=hour + ":" + minute + ":" + second)
    label_time.after(1000, clock)

label_time = tk.Label(root, text="time", font=("Arial", 50))
label_time.pack()

#testing timer
hours = StringVar()
mins = StringVar()
secs = StringVar()

hours.set("00")
mins.set("00")
secs.set("00")

hoursEntry = tk.Entry(root, width=3, font=("arial, 18"), textvariable=hours)
hoursEntry.place(x=20, y=80)

minsEntry = tk.Entry(root, width=3, font=("arial, 18"), textvariable=mins)
minsEntry.place(x=70, y=80)

secsEntry = tk.Entry(root, width=3, font=("arial, 18"), textvariable=secs)
secsEntry.place(x=120, y=80)

#timer button
def set():
    try: 
        totaltime = int(hours.get())*3600 + int(mins.get())*60 + int(secs.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    countdown(totaltime)

def countdown(timeleft):
    if timeleft >= 0:
        hourss,remainder = divmod(timeleft,3600)
        minss,secss = divmod(remainder,60)
        
        hours.set("{0:2d}".format(hourss))
        mins.set("{0:2d}".format(minss))
        secs.set("{0:2d}".format(secss))

        root.after(1000, countdown, timeleft-1)
    else: 
            messagebox.showinfo("TIMES UP")

def clear():
    hours.set("00")
    mins.set("00")
    secs.set("00")
    timeleft.set("00")

timerbtn = tk.Button(root, text="set timer", command= set)
timerbtn.pack()

clearbtn = tk.Button(root, text="Clear", command=clear)
clearbtn.pack()

clock()
root.mainloop()
