import tkinter as tk
from tkinter import ttk, filedialog, StringVar
from tkinter import messagebox
from PIL import Image, ImageTk
import os

def play_with_phaser_page(app, midi_directory, chosen_song, start_playing_button, play_with_phaser_window):
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

    return_to_menu_button = ttk.Button(play_with_phaser_window, text="Return to Main Menu", command=lambda: return_to_main_menu(app, start_playing_button, play_with_phaser_window))
    return_to_menu_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

def return_to_main_menu(app, start_playing_button, play_with_phaser_window):
    app.deiconify()
    start_playing_button["state"] = "normal"
    play_with_phaser_window.destroy()