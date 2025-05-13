import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Create the main Tkinter window
root = tk.Tk()
root.title("Study Buddy Music Player")
root.geometry("400x250")

# Functions for music player
def load_music():
    # Open file dialog to select a music file (MP3)
    filepath = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if filepath:
        pygame.mixer.music.load(filepath)
        play_button["state"] = "normal"
        stop_button["state"] = "normal"
        pause_button["state"] = "normal"

def play_music():
    pygame.mixer.music.play()

def stop_music():
    pygame.mixer.music.stop()

def pause_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        pause_button.config(text="Resume")
    else:
        pygame.mixer.music.unpause()
        pause_button.config(text="Pause")

def change_volume(val):
    try:
        volume = float(val) / 100  # Convert val to float and scale it from 0 to 1
        pygame.mixer.music.set_volume(volume)
        volume_label.config(text=f"Volume: {int(volume * 100)}%")  # Update the volume label text as an integer percentage
    except ValueError:
        pass  # In case of any non-numeric value, do nothing


# Create the frame for the controls
frame = tk.Frame(root)
frame.pack(pady=20)

# Load resized icons (manually resized images)
play_icon = tk.PhotoImage(file=r"C:\Users\Harsimran\Projects\Mini_IT_Project-1-08\ButtonPics\play.png")  # Replace with your resized file path
pause_icon = tk.PhotoImage(file=r"C:\Users\Harsimran\Projects\Mini_IT_Project-1-08\ButtonPics\pause.png")  # Replace with your resized file path
stop_icon = tk.PhotoImage(file=r"C:\Users\Harsimran\Projects\Mini_IT_Project-1-08\ButtonPics\stop.png")  # Replace with your resized file path

# Create buttons with resized images
load_button = tk.Button(frame, text="Load Music", command=load_music)
load_button.grid(row=0, column=0, padx=10)

play_button = tk.Button(frame, text="Play", image=play_icon, state="disabled", command=play_music)
play_button.grid(row=0, column=1, padx=10)

pause_button = tk.Button(frame, text="Pause", image=pause_icon, state="disabled", command=pause_music)
pause_button.grid(row=0, column=2, padx=10)

stop_button = tk.Button(frame, text="Stop", image=stop_icon, state="disabled", command=stop_music)
stop_button.grid(row=0, column=3, padx=10)

# Volume control
volume_label = tk.Label(root, text="Volume: 50%")
volume_label.pack(pady=5)

volume_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=change_volume)
volume_slider.set(50)  # Default volume to 50%
volume_slider.pack(pady=10)

# Run the app
root.mainloop()
