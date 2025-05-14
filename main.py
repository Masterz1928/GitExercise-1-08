import pygame
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import json
import os

CONFIG_FILE = "music_config.json"

def load_settings():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Config file is corrupted, using defaults.")
    return {}

def save_settings(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

# Functions for music player
def load_music():
    # Open file dialog to select a music file (MP3)
    filepath = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if filepath:
        pygame.mixer.music.load(filepath)
        play_button["state"] = "normal"
        stop_button["state"] = "normal"
        settings["last_song"] = filepath
        save_settings(settings)
        current_song.config(text="Now Playing: " + os.path.basename(filepath))


# Variable to store the current position of the song
current_position = 0

# Variable to track whether the music is playing or paused
is_playing = False

# Functions for music player
def play_pause_music():
    global is_playing, current_position
    if is_playing:
        # Pause the music
        current_position = pygame.mixer.music.get_pos()  # Save position in milliseconds
        pygame.mixer.music.pause()
        play_button.config(text="Play", image=play_icon)  # Update button text to "Play"
        is_playing = False
    else:
        # Resume or start the music
        if current_position == 0:  # If it's the first play (no previous position saved)
            pygame.mixer.music.play()
        else:  # Resume from the paused position
            pygame.mixer.music.play(start=current_position / 1000)  # Convert to seconds
        play_button.config(text="Pause", image=pause_icon)  # Update button text to "Pause"
        is_playing = True

def stop_music():
    global is_playing, current_position
    pygame.mixer.music.stop()
    current_position = 0  # Reset the position
    is_playing = False
    play_button.config(text="Play", image=play_icon)  # Reset the play button

def change_volume(val):
    try:
        volume = float(val) / 100  # Convert val to float and scale it from 0 to 1
        pygame.mixer.music.set_volume(volume)
        volume_label.config(text=f"Volume: {int(volume * 100)}%")  # Update the volume label text as an integer percentage
        settings["volume"] = volume
        save_settings(settings)
    except ValueError:
        pass  # In case of any non-numeric value, do nothing


# Create the main Tkinter window
root = tk.Tk()
root.title("Study Buddy Music Player")
root.geometry("400x250")

# Load previous settings
settings = load_settings()
last_song = settings.get("last_song", "")
last_volume = settings.get("volume", 0.5)

# Set initial volume
# Initialize pygame mixer for audio playback
pygame.mixer.init()
pygame.mixer.music.set_volume(last_volume)

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

play_button = tk.Button(frame, text="Play", image=play_icon, state="disabled", command=play_pause_music)
play_button.grid(row=0, column=1, padx=10)

stop_button = tk.Button(frame, text="Stop", image=stop_icon, state="disabled", command=stop_music)
stop_button.grid(row=0, column=2, padx=10)

filename = os.path.basename(last_song)
current_song = tk.Label(root, text=f"Playing: {filename}")
current_song.pack()

# Volume control
volume_label = tk.Label(root, text="Volume: 50%")
volume_label.pack(pady=5)

volume_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=change_volume)
volume_slider.set(last_volume * 100)
volume_label.config(text=f"Volume: {int(last_volume * 100)}%")

if last_song and os.path.exists(last_song):
    try:
        pygame.mixer.music.load(last_song)
        play_button["state"] = "normal"
        stop_button["state"] = "normal"
    except Exception as e:
        print(f"Could not load last song: {e}")

volume_slider.pack(pady=10)

# Run the app
root.mainloop()
