import tkinter as tk
import time 
from tkinter import StringVar, messagebox
#git add .
#git commit -m "name"
#git push

root = tk.Tk()

root.title("Timer")
root.geometry("800x800")

#input
hours = StringVar(value="00")
mins = StringVar(value="00")
secs = StringVar(value="00")

purpose = StringVar(root, "")

main_label = tk.Label(root, text="Set the time")
main_label.pack()

timeinput_frame =tk.LabelFrame(root)
timeinput_frame.pack(pady=10)

hoursentry = tk.Entry(timeinput_frame, width=2, textvariable=hours, font=("arial", 18))
hoursentry.pack(side =tk.LEFT)
separatorlabel = tk.Label(timeinput_frame, text=":")
separatorlabel.pack(side =tk.LEFT)
minsentry = tk.Entry(timeinput_frame, width=2, textvariable=mins, font=("arial", 18))
minsentry.pack(side =tk.LEFT)
separatorlabel2= tk.Label(timeinput_frame, text=":")
separatorlabel2.pack(side =tk.LEFT)
secsentry = tk.Entry(timeinput_frame, width=2, textvariable=secs, font=("arial", 18))
secsentry.pack(side =tk.LEFT)

purpose_label = tk.Label(root, text="Purpose")
purpose_label.pack()
purpose_entry= tk.Entry(root, textvariable=purpose)
purpose_entry.pack()

timers_frame = tk.Frame(root)
timers_frame.pack(pady=20)

def timer():
    try:
        totaltime = int(hours.get())*3600 + int(mins.get())*60 + int(secs.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return
    
    ntimer = tk.Frame(timers_frame)
    ntimer.pack()

    ntimer_label = tk.Label(ntimer, text="", font=("Arial", 18))
    ntimer_label.pack(side=tk.LEFT)

    purposetext = tk.Label(ntimer, text=purpose.get())
    purposetext.pack(side=tk.LEFT)

    def countdown(timeleft):
        if timeleft >=0:
            hourss,remainder = divmod(timeleft,3600)
            minss,secss = divmod(remainder,60)
            ntimer_label.config(text=f"{hourss:02}:{minss:02}:{secss:02}")
            root.after(1000, countdown, timeleft - 1)
        else:
            ntimer_label.config(text="DONE!")
            ntimer_label.config(fg="green")
            messagebox.showinfo("ALERT", "TIMES UP")

    countdown(totaltime)

start_btn = tk.Button(root, text="Start New Timer", command=timer)
start_btn.pack()

root.mainloop()