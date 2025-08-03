import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from Logic import *
import csv
import ast

root = tk.Tk()


root.geometry("500x700") # width x height
root.resizable(False,False)

#Settings Functions
class SettingOption:
    def __init__(self, line_num, option_name, value, category, type, min_value = None, max_value = None, list_values = None):
        self.line_num = line_num
        self.option_name = option_name
        self.value = value
        self.category =category
        self.type = type
        self.min_value = min_value
        self.max_value = max_value
        self.list_values = list_values
        
    def __str__(self):
        return f"SettingOption(line_num={self.line_num} option_name={self.option_name}, value={self.value}, category={self.category}, type={self.type}, min_value={self.min_value}, max_value={self.max_value}, list_values={self.list_values})"

SettingsList = []

def safe_literal(value):
    try:
        return ast.literal_eval(value)
    except:
        return value
    
def safe_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None
    
PlayerNum = 0
NumOfWords = 0

def get_settings(FileName = 'WordConnections/App/Settings.csv'):
    global SettingsList
    SettingsList.clear()
    with open(FileName, "r", newline = '') as csvfile:
        SettingsInfo = csv.DictReader(csvfile, fieldnames=['option_name', 'value', 'category', 'type', 'min_value', 'max_value', 'list_values'])
        #print(SettingsInfo.fieldnames)

        for line_num, row in enumerate(SettingsInfo):
            parsed_value = safe_literal(row['value'])
            parsed_list = safe_literal(row['list_values'])
            #print("list = " + str(parsed_list))
            min_val = safe_float(row.get('min_value', None))
            max_val = safe_float(row.get('max_value', None))

            match line_num:
                case 0:
                    global NumOfWords
                    NumOfWords = parsed_value
                    print("Number of Words = " + str(parsed_value))
                case 1:
                    global PlayerNum 
                    PlayerNum = parsed_value
                    print("Number of players = " + str(PlayerNum))



            
            Setting = SettingOption(
                line_num=line_num,
                option_name=row['option_name'],
                value=parsed_value,
                category=row['category'],
                type=row['type'].strip(),  # clean whitespace
                min_value=min_val,
                max_value=max_val,
                list_values=parsed_list
            )
            SettingsList.append(Setting)


    #for i in range(len(SettingsList)):
    #    print(SettingsList[i])

    return SettingsList

def modify_file(file_name, row_id, col_id, new_value):
    try:
        with open(file_name, 'r', newline = '') as infile:
            readfile = csv.reader(infile)
            data = list(readfile)

            if 0 <= row_id < len(data) and 0 <= col_id < len(data[row_id]):
                data[row_id][col_id] = new_value
            else: 
                print(f"Error: Row {row_id} or column {col_id} is out of bounds.")
                return
            
            with open(file_name, 'w', newline= '') as outfile:
                writefile = csv.writer(outfile)
                writefile.writerows(data)

    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
            



SettingsWidgets = []
def display_settings():
    SettingsWidgets.clear()
    global CurrentSetting
    for CurrentSetting, item in enumerate(SettingsList):
        label = Label(root, text = item.option_name, font = "Arial 12 bold")
        label.grid(row = CurrentSetting + 1, column = 0, padx = 5, pady = 5)
        SettingsWidgets.append(label)

        match SettingsList[CurrentSetting].type:
            case "Slider":
                
                slider = Scale(root, orient = "horizontal", from_ = item.min_value, to = item.max_value, value = item.value, 
                               command = lambda value, index = CurrentSetting: update_setting(value, index))
                slider.grid(row = CurrentSetting + 1, column = 1, padx = 5, pady = 5)

                variable_label = Label(root, text = item.value, font = "Arial 10 bold")
                variable_label.grid(row = CurrentSetting + 1, column = 2, padx = 5, pady = 5)
                
                slider.config(command = lambda value, index = CurrentSetting, lbl = variable_label: update_setting(value, index, lbl))

                SettingsWidgets.append(slider)
                SettingsWidgets.append(variable_label)
                
            case "Combobox":
                selected_option = tk.StringVar()
                Combo = Combobox(root, textvariable = selected_option, values = item.list_values) 
                Combo.set(item.value)
                Combo.grid(row = CurrentSetting + 1, column = 1, padx = 5, pady = 5)
                #bind resolution combo box
                if item.option_name == "Resolution":
                    Combo.bind("<<ComboboxSelected>>", change_resolution)
                SettingsWidgets.append(Combo)


def change_resolution(event):
    new_resolution = event.widget.get()
    root.geometry(new_resolution) # width x height
    return


def update_setting(value, i, label = None):
    SettingsList[i].value = int(float(value))
    if label:
        label.config(text=f"{int(float(value))}")
    #print(SettingsList[i].line_num)
    #print(int(float(value)))
    modify_file('WordConnections/App/Settings.csv', SettingsList[i].line_num, 1, int(float(value)))
    
    return 0

#Button Functions
def quit_app():
    print("quitting")
    root.quit()

is_paused = False
#Pause/Resume Game
def pause_game(event):
    global is_paused
    #try:
    #    print(previous_tab[len(previous_tab)-1])
    #except:
    #    return
    if is_paused & (previous_tab[len(previous_tab)-2] == "Game"):
        is_paused = False
        #print("unpausing game")
        previous_tab.clear()
        Display("Game")
    elif (previous_tab[len(previous_tab)-1] == "Game"):
        is_paused = True
        #print("Pausing game")
        Display("Pause")

    else:
        back_button()

def resume_game(event):
    Display("Game")

#Back Button Functions
previous_tab = []
def print_previous_tabs():
    for i in range(len(previous_tab)):
        print(previous_tab[i])

        
def back_button():
    if len(previous_tab) > 1:
        #next_tab = previous_tab[len(previous_tab)-2]
        #print("next tab is " + next_tab)
        previous_tab.pop()
        Display(previous_tab.pop())

#Display Setup
def clear_window():
    for widget in root.winfo_children():
        widget.grid_forget()

def Display(State, Clear = True):
    if Clear:
        clear_window()
        
    match State:
        case "Menu":
            previous_tab.append("Menu")

            TitleLabel.grid(row = 0, column = 0, padx = 125, pady = 50, columnspan=3, sticky="n")
            GameSelect.grid(row = 2, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Settings.grid(row = 3, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Back.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Quit.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")

        case "Pause":
            previous_tab.append("Pause")
            pause_label.grid(row = 0, column = 0, padx = 125, pady = 50, columnspan=3, sticky="n")
            Settings.grid(row = 3, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            resume_button.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Quit.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")

        case "Settings":
            previous_tab.append("Settings")
            SettingsLabel.grid(row = 0, column = 0, padx = 5, pady = 5)
            get_settings()
            display_settings()
            Back.grid(row = 4, column = 0, padx = 5, pady = 5)

        case "Game":
            previous_tab.append("Game")
            SetupPlayers(NumOfPlayers)
            PrintPlayerStats(0)
            
            game_title.grid(row = 0, column = 0, padx = 125, pady = 50, columnspan=3, sticky="n")
            
            Back.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Quit.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")

        case "Game Select":
            previous_tab.append("Game Select")
            TitleLabel.grid(row = 0, column = 0, padx = 125, pady = 50, columnspan=3, sticky="n")
            GameSelect.grid(row = 2, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Settings.grid(row = 3, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Back.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Quit.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
    

#Generic Buttons
Settings = Button(root, text = "Settings", command = lambda: Display("Settings"))
Quit = Button(root, text = "Quit", command = quit_app)
Back = Button(root, text = "Back", command =  back_button)

#Menu Display
TitleLabel = Label(root, text="Word Connections", font=("Cambria 25 bold"))
GameSelect = Button(root, text = "Game Select", command = lambda: Display("Game"))

#Pause Menu
pause_label = Label(root, text="Game Paused", font=("Cambria 25 bold"))
resume_button = Button(root, text = "Resume", command = lambda: Display("Game"))

#Game Display
game_title = Label(root, text="IN GAME", font=("Cambria 25 bold"))

#Game Select Display
GameSetupTitleLabel = Label(root, text=" Game Setup", font=("Cambria 25 bold"))

#Settings Display
SettingsLabel = Label(root, text="Settings", font=("Cambria 25 bold"))

#Key Binds
root.bind("<Escape>", pause_game)

    

# Set the Window title
Display("Menu", False)
root.title("My Python Window")
root.mainloop()