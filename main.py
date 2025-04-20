import tkinter as tk
from tkinter import messagebox
import time

root = tk.Tk()
root.title("Multi Timer")
root.geometry("800x800")

# Shared input fields
hours = tk.StringVar(value="00")
mins = tk.StringVar(value="00")
secs = tk.StringVar(value="00")

tk.Label(root, text="Set Time (HH:MM:SS)").pack()

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Entry(input_frame, width=3, textvariable=hours).pack(side=tk.LEFT)
tk.Label(input_frame, text=":").pack(side=tk.LEFT)
tk.Entry(input_frame, width=3, textvariable=mins).pack(side=tk.LEFT)
tk.Label(input_frame, text=":").pack(side=tk.LEFT)
tk.Entry(input_frame, width=3, textvariable=secs).pack(side=tk.LEFT)

timers_frame = tk.Frame(root)
timers_frame.pack(pady=20)

def start_new_timer():
    try:
        total = int(hours.get()) * 3600 + int(mins.get()) * 60 + int(secs.get())
        if total <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid time.")
        return

    # Create a frame for this timer
    timer_frame = tk.Frame(timers_frame)
    timer_frame.pack(pady=5)

    timer_label = tk.Label(timer_frame, text="", font=("Arial", 18))
    timer_label.pack(side=tk.LEFT)

    def countdown(timeleft):
        if timeleft >= 0:
            h, r = divmod(timeleft, 3600)
            m, s = divmod(r, 60)
            timer_label.config(text=f"{h:02}:{m:02}:{s:02}")
            root.after(1000, countdown, timeleft - 1)
        else:
            timer_label.config(text="DONE!")
            timer_label.config(fg="green")

    countdown(total)

start_btn = tk.Button(root, text="Start New Timer", command=start_new_timer)
start_btn.pack()

root.mainloop()
