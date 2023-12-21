import tkinter as tk
from tkinter import messagebox, ttk, filedialog, StringVar
from pygame import mixer
import os
from PIL import Image, ImageTk

mixer.init()
chosen_song = ""
song_playing = False
feedback_options_window = None
play_with_phaser_window = None
return_to_menu_button = None

midi_directory = r"C:\Users\Admin\Downloads\GUI"


def play_song(file):
    try:
        mixer.music.load(file)
        mixer.music.play()
        global song_playing
        song_playing = True
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def stop_song():
    try:
        mixer.music.stop()
        global song_playing
        song_playing = False
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def hear_song():
    if chosen_song:
        if not song_playing:
            play_song(os.path.join(midi_directory, chosen_song + ".mid"))
        else:
            stop_song()
    else:
        messagebox.showinfo("Message", "Please choose a song first.")

def choose_existing_song():
    global chosen_song
    midi_files = ["Twinkle Twinkle", "Ode to Joy", "Bella Ciao", "Never Gonna Give You Up", "Mary had a Little Lamb"]
    song_window = tk.Toplevel(app)
    song_window.title("Choose Song from Existing Songs")
    style = ttk.Style()
    style.configure("TButton", padding=10, font=('Helvetica', 12))
    for midi_file in midi_files:
        song_button = ttk.Button(song_window, text=midi_file, command=lambda file=midi_file: set_chosen_song(file, song_window))
        song_button.pack(fill=tk.X, pady=5)

def import_midi_file():
    global chosen_song
    file_path = filedialog.askopenfilename(initialdir=midi_directory, filetypes=[("MIDI Files", "*.mid")])
    if file_path:
        set_chosen_song(os.path.splitext(os.path.basename(file_path))[0])

def set_chosen_song(song, window_to_close=None):
    global chosen_song
    chosen_song = song
    chosen_song_label.config(text=f"Song chosen: {chosen_song}")
    start_playing_button.pack(pady=10, fill=tk.X)
    if window_to_close:
        window_to_close.destroy()

def set_volume(value):
    try:
        volume = int(value)
        mixer.music.set_volume(volume / 100.0)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def start_playing():
    global feedback_options_window
    if chosen_song:
        if mixer.music.get_busy():
            stop_song()
        feedback_options_window = tk.Toplevel(app)
        feedback_options_window.title("Feedback Options")

        style = ttk.Style()
        style.configure("TRadiobutton", padding=10, font=('Helvetica', 12))
        feedback_option = StringVar()
        feedback_label = tk.Label(feedback_options_window, text="Select Feedback Option", font=('Helvetica', 14))
        feedback_label.pack(pady=10)
        feedback_with = ttk.Radiobutton(feedback_options_window, text="Play with Feedback", variable=feedback_option, value="with")
        feedback_with.pack()
        feedback_without = ttk.Radiobutton(feedback_options_window, text="Play without Feedback", variable=feedback_option, value="without")
        feedback_without.pack()

        start_playing_button["state"] = "disabled"

        confirm_feedback_button = ttk.Button(feedback_options_window, text="Confirm", command=lambda: play_with_feedback(feedback_option.get()))
        confirm_feedback_button.pack(pady=10)
    else:
        messagebox.showinfo("Message", "Please select a song.")

def play_with_feedback(feedback_option_value):
    global feedback_options_window, play_with_phaser_window

    feedback_options_window.destroy()
    app.withdraw()
    play_with_phaser_page(feedback_option_value)


def play_with_phaser_page(feedback_option_value):
    global play_with_phaser_window, return_to_menu_button

    play_with_phaser_window = tk.Toplevel(app)
    play_with_phaser_window.title("Play with PHASER")

    midi_file_path = os.path.join(midi_directory, chosen_song + ".mid")
    png_file_path = os.path.join(midi_directory, chosen_song + ".png")

    try:
        image = Image.open(png_file_path)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(play_with_phaser_window, image=photo)
        image_label.image = photo
        image_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

    return_to_menu_button = ttk.Button(play_with_phaser_window, text="Return to Main Menu", command=return_to_main_menu)
    return_to_menu_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

def return_to_main_menu():
    global play_with_phaser_window

    app.deiconify()
    start_playing_button["state"] = "normal"
    play_with_phaser_window.destroy()

def on_close():
    mixer.quit
    app.destroy()

app = tk.Tk()

app.title("PHASER GUI")

style = ttk.Style()
style.configure("TButton", padding=10, font=('Helvetica', 12))

app.configure(bg="#34344a")

label = tk.Label(app, text="PHASER GUI", font=('Helvetica', 16), bg="#34344a", fg="white")
label.pack()

app.protocol("WM_DELETE_WINDOW", on_close)

button_frame_1 = tk.Frame(app, bg="#34344a")
button_frame_1.pack(pady=5)

choose_song_button = ttk.Button(button_frame_1, text="Choose Song from Existing Songs", command=choose_existing_song)
choose_song_button.pack(side=tk.LEFT, padx=5)

import_midi_button = ttk.Button(button_frame_1, text="Import MIDI File (.mid)", command=import_midi_file)
import_midi_button.pack(side=tk.RIGHT, padx=5)

button_frame_2 = tk.Frame(app, bg="#34344a")
button_frame_2.pack(pady=5)

hear_song_button = ttk.Button(button_frame_2, text="Hear Song", command=hear_song)
hear_song_button.pack(side=tk.LEFT, padx=5)

stop_button = ttk.Button(button_frame_2, text="Stop", command=stop_song)
stop_button.pack(side=tk.RIGHT, padx=5)

volume_label = tk.Label(app, text="Volume", font=('Helvetica', 12), bg="#34344a", fg="white")
volume_label.pack()

volume_scale = tk.Scale(app, from_=0, to=100, orient=tk.HORIZONTAL, command=set_volume, length=200, bg="#34344a", fg="white")
volume_scale.set(70)
volume_scale.pack(pady=10)

chosen_song_label = tk.Label(app, text="", font=('Helvetica', 12), bg="#34344a", fg="white")
chosen_song_label.pack()

start_playing_button = ttk.Button(app, text="Start Playing", command=start_playing, style="TButton")
start_playing_button.pack(pady=10, fill=tk.X)

app.mainloop()
