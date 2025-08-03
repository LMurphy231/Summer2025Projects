import tkinter as tk
from tkinter.ttk import *
from Logic import *

window = tk.Tk()
window.geometry("500x700") # width x height
window.resizable(False,False)

def remove_all_widgets(parent_widget):
    """Removes all Button widgets from the given parent_widget."""
    for widget in parent_widget.winfo_children():
        if isinstance(widget, tk.Button):
            widget.destroy()

def Display(State):
    remove_all_widgets(window)
    match State:
        case "Menu":
            print("setting up main menu")
            TitleLabel.pack(padx = 100, pady = 100)
            PlayGame.place(x = 150, y = 150, width = 200)
            Settings.place(x = 150, y = 200, width = 200)
        case "Pause":
            TitleLabel.pack(padx = 100, pady = 100)
            PlayGame.place(x = 150, y = 150, width = 200)
        case "Settings":
            TitleLabel.pack(padx = 100, pady = 100)
            PlayGame.pack(padx = 150, pady = 150)
            Settings.pack(padx = 150, pady = 200)
        case "Game":
            Settings.pack(padx = 100, pady = 100)
            print("setting up game")
        case "Player Select":
            TitleLabel.pack(padx = 100, pady = 100)
            PlayGame.place(x = 150, y = 150, width = 200)
            
#Menu Display
TitleLabel = Label(window, text="Word Connections", font=("Cambria 25 bold"))
PlayGame = Button(window, text = "Play Game", command = lambda: Display("Game"))
Settings = Button(window, text = "Settings", command = lambda: Display("Settings"))
#PlayGame = Button(window, text = "Play Game", command = lambda: Display("Game"))
#PlayGame = Button(window, text = "Play Game", command = lambda: Display("Game"))
SettingsLabel = Label(window, text="Settings", font=("Cambria 25 bold"))



    

# Set the window title
Display("Menu")
window.title("My Python Window")
window.mainloop()