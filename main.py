import tkinter as tk
import time 
from tkinter import StringVar, messagebox, filedialog
#import winsound
import pygame
import os
from plyer import notification

#git add .
#git commit -m "name"
#git push

root = tk.Tk()
root.title("Timer")
root.geometry("800x800")

pygame.mixer.init()

#Fdisplay clock
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

timeinput_frame = tk.LabelFrame(root)
timeinput_frame.pack(pady=10)

#input
hoursentry = tk.Entry(timeinput_frame, width=2, textvariable=hours, font=("arial", 18))
hoursentry.pack(side=tk.LEFT)
separatorlabel = tk.Label(timeinput_frame, text=":")
separatorlabel.pack(side=tk.LEFT)
minsentry = tk.Entry(timeinput_frame, width=2, textvariable=mins, font=("arial", 18))
minsentry.pack(side=tk.LEFT)
separatorlabel2= tk.Label(timeinput_frame, text=":")
separatorlabel2.pack(side=tk.LEFT)
secsentry = tk.Entry(timeinput_frame, width=2, textvariable=secs, font=("arial", 18))
secsentry.pack(side=tk.LEFT)

#Frame for preset buttons
preset_frame = tk.Frame(root)
preset_frame.pack(pady=10)

def set_preset_time(h, m, s):
    hours.set(f"{h:02}")
    mins.set(f"{m:02}")
    secs.set(f"{s:02}")

#Create preset buttons
preset_5min = tk.Button(preset_frame, text="5 min")
preset_5min.config(command=lambda: set_preset_time(0, 5, 0))
preset_5min.pack(side=tk.LEFT, padx=5)

preset_10min = tk.Button(preset_frame, text="10 min")
preset_10min.config(command=lambda: set_preset_time(0, 10, 0))
preset_10min.pack(side=tk.LEFT, padx=5)

preset_25min = tk.Button(preset_frame, text="25 min")
preset_25min.config(command=lambda: set_preset_time(0, 25, 0))
preset_25min.pack(side=tk.LEFT, padx=5)

preset_1hour = tk.Button(preset_frame, text="1 hour")
preset_1hour.config(command=lambda: set_preset_time(1, 0, 0))
preset_1hour.pack(side=tk.LEFT, padx=5)

purpose_label = tk.Label(root, text="Purpose")
purpose_label.pack()
purpose_entry= tk.Entry(root, textvariable=purpose, font=("arial", 14))
purpose_entry.pack()

timers_frame = tk.Frame(root)
timers_frame.pack(pady=20)

#checking input validation
def inputvalidation():
    try:

        if  int(secs.get()) < 0 or int(secs.get()) > 59:
            messagebox.showerror("invalid input", "It must be between 0 to 59")
            return False
        if int(mins.get()) < 0 or int(mins.get()) > 59:
            messagebox.showerror("invalid input", "It must be between 0 to 59")
            return False
        if int(hours.get()) < 0 or int(hours.get()) > 99:
            messagebox.showerror("invalid input", "It must be between 0 to 99")
            return False
        if hours.get() == "00" and mins.get() == "00" and secs.get() == "00":
           messagebox.showerror("Invalid Time", "Time must be greater than 00:00:00.")
           return  False
     
        return True
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for hours, minutes, and seconds.")
        return False

#timer function
def timer():
    if not inputvalidation():
        return
    
    totaltime = int(hours.get())*3600 + int(mins.get())*60 + int(secs.get())

    create_time = time.strftime("%Y-%m-%d %H:%M:%S")
    purpose_text = purpose.get()

    #saving func
    with open("timerhistory.txt","a") as f:
        f.write(f"{create_time} - {purpose_text} ({hours.get()}:{mins.get()}:{secs.get()})\n")
    
    ntimer = tk.Frame(timers_frame)
    ntimer.pack(pady=5)

    ntimer_label = tk.Label(ntimer, text="", font=("Arial", 18))
    ntimer_label.pack(side=tk.LEFT)

    purposetext = tk.Label(ntimer, text=f"for {purpose_text}")
    purposetext.pack(side=tk.LEFT)

    remaining_time = [totaltime]
    paused = [False]

    def countdown(timeleft):
        if timeleft >= 0:
            hourss,remainder = divmod(timeleft,3600)
            minss,secss = divmod(remainder,60)
            ntimer_label.config(text=f"{hourss:02}:{minss:02}:{secss:02}")
            if not paused[0]:
                root.after(1000, countdown, timeleft - 1)
            remaining_time[0] = timeleft
        else:
            ntimer_label.config(text="DONE!", fg="green")

            if os.path.exists(sound_path.get()):
                try:
                    pygame.mixer.music.load(sound_path.get())
                    pygame.mixer.music.play()

                except Exception as e:
                    print("Error playing sound:", e)
            else:
                print("No sound file selected or path invalid.")

            if show_notification.get():
                notification.notify(
                    title="Timer Finished",
                    message=f"Time's up for '{purpose_text}'",
                    timeout=3
                )
                messagebox.showinfo("ALERT", f"TIMES UP for '{purpose_text}'")


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

    pause_btn = tk.Button(ntimer, text="⏸ Pause", command=pause)
    pause_btn.pack(side=tk.LEFT)

    resume_btn = tk.Button(ntimer, text="▶ Resume", command=resume)
    resume_btn.pack(side=tk.LEFT)

    clear_btn = tk.Button(ntimer, text="❌ Clear", command=clear)
    clear_btn.pack(side=tk.LEFT)

    hours.set("00")
    mins.set("00")
    secs.set("00")
    purpose.set("")

    countdown(totaltime)  
      
start_btn = tk.Button(root, text="Start New Timer", command=timer)
start_btn.pack()

def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("History")
    history_window.geometry("400x400")
    history_label = tk.Label(history_window, text="History Here", font=("Arial", 16))
    history_label.pack(pady=20)
    history_text = tk.Text(history_window, wrap=tk.WORD)
    history_text.pack()

    try:
        with open("timerhistory.txt", "r") as f:
            content = f.read()
            history_text.insert(tk.END, content)
    except FileNotFoundError:
        history_text.insert(tk.END, "No history yet.")

history_button = tk.Button(root, text="History", command=open_history_window)
history_button.place(relx=0.0, rely=1.0, x=10, y=-10, anchor="sw")

sound_path = StringVar(value="") 
if os.path.exists("alarmpath.txt"):
    with open("alarmpath.txt", "r") as f:
        saved_alarm = f.read().strip()
        if os.path.exists(saved_alarm):
            sound_path.set(saved_alarm)
        else:
            messagebox.showwarning("Alarm Sound Not Found", "The previously saved alarm sound file was not found. Please select a new one.")

def choose_sound():
    file = filedialog.askopenfilename(
        title="Select Alarm Sound",
        filetypes=[("Audio Files", "*.wav *.mp3 *.ogg")]
    )
    if file:
        sound_path.set(file)
        with open("alarmpath.txt", "w") as f:
            f.write(file)

def preview_sound():
    if os.path.exists(sound_path.get()):
        try:
            pygame.mixer.music.load(sound_path.get())
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Sound Error", f"Could not play the sound.\n{e}")
    else:
        messagebox.showwarning("No Sound", "Please select a valid sound file first.")


show_notification = tk.BooleanVar(value=True)

options_frame = tk.Frame(root)
options_frame.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

select_button = tk.Button(options_frame, text="🎵 Choose Alarm Sound", command=choose_sound)
select_button.pack(side=tk.LEFT)

preview_button = tk.Button(options_frame, text="🔊 Preview", command=preview_sound)
preview_button.pack(side=tk.LEFT, padx=5)


notify_checkbox = tk.Checkbutton(options_frame, text="Notification PoPup", variable=show_notification)
notify_checkbox.pack(side=tk.LEFT, padx=10)


clock()
root.mainloop()
