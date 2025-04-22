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
    day = time.strftime("%a")
    date = time.strftime("%d")

    label_time.config(text=hour + ":" + minute + ":" + second)
    label_day_date.config(text=day + "," + date)
    label_time.after(1000, clock)

label_time = tk.Label(root, text="time", font=("Arial", 20))
label_time.place(relx=1.0, x=-10, y=10, anchor="ne")
label_day_date = tk.Label(root, text="", font=("Arial", 12))
label_day_date.place(relx=1.0, x=-10, y=40, anchor="ne")

#connect betwen python and tkinter
hours = StringVar(value="00")
mins = StringVar(value="00")
secs = StringVar(value="00")

purpose = StringVar(root, "")

main_label = tk.Label(root, text="Set the time")
main_label.pack()

timeinput_frame =tk.LabelFrame(root)
timeinput_frame.pack(pady=10)

#input
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
purpose_entry= tk.Entry(root, textvariable=purpose, font=("arial", 14))
purpose_entry.pack()

timers_frame = tk.Frame(root)
timers_frame.pack(pady=20)

#timer working 
def timer():
    try:
        totaltime = int(hours.get())*3600 + int(mins.get())*60 + int(secs.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return
    
    ntimer = tk.Frame(timers_frame)
    ntimer.pack(pady=5)

    ntimer_label = tk.Label(ntimer, text="", font=("Arial", 18))
    ntimer_label.pack(side=tk.LEFT)

    purposetext = tk.Label(ntimer, text=purpose.get())
    purposetext.pack(side=tk.LEFT)

    remaining_time = [totaltime]
    paused = [False]

    def countdown(timeleft):
        if timeleft >=0:
            hourss,remainder = divmod(timeleft,3600)
            minss,secss = divmod(remainder,60)
            ntimer_label.config(text=f"{hourss:02}:{minss:02}:{secss:02}")
            if not paused[0]:
                root.after(1000, countdown, timeleft - 1)
            remaining_time[0] = timeleft
        else:
            ntimer_label.config(text="DONE!", fg="green")
            messagebox.showinfo("ALERT", f"TIMES UP for '{purpose.get()}'")

    def pause():
        paused[0] = True
        pause_btn.config(state="disabled")
        resume_btn.config(state="normal")
    
    def resume():
        paused[0] = False
        countdown(remaining_time[0])
        resume_btn.config(state="disabled")
        pause_btn.config(state="normal")
    
    def clear():
        paused[0] = True
        ntimer.destroy()
        resume_btn.config(state="disabled")
        pause_btn.config(state="normal")

    pause_btn = tk.Button(ntimer, text="Pause", command=pause)
    pause_btn.pack(side=tk.LEFT)

    resume_btn = tk.Button(ntimer, text="Resume", command=resume, state="disabled")
    resume_btn.pack(side=tk.LEFT)

    clear_btn = tk.Button(ntimer, text="Clear", command=clear)
    clear_btn.pack(side=tk.LEFT)

    countdown(totaltime)    
start_btn = tk.Button(root, text="Start New Timer", command=timer)
start_btn.pack()

def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("History")
    history_window.geometry("400x400")
    history_label = tk.Label(history_window, text="History Here", font=("Arial", 16))
    history_label.pack(pady=20)

history_button = tk.Button(root, text="History", command=open_history_window)
history_button.place(relx=0.0, rely=1.0, x=10, y=-10, anchor="sw")

clock()
root.mainloop()