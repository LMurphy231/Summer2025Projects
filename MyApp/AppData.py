import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkfont

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import pygame

import csv
import ast
import time
import random


class SettingOption:
    def __init__(self, name, line_num, value, category, category_type, type, min_value = None, max_value = None, list_values = None):
        self.line_num = line_num
        self.name = name
        self.value = value
        self.category = category
        self.category_type = category_type
        self.type = type
        self.min_value = min_value
        self.max_value = max_value
        self.list_values = list_values
        
    def __str__(self):
        return f"SettingOption(name={self.name}, line_num={self.line_num}, value={self.value}, category={self.category}, category_type={self.category_type}, type={self.type}, min_value={self.min_value}, max_value={self.max_value}, list_values={self.list_values})"

# region   AppData
class AppData:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.current_dimensions = [500, 700]
        self.previous_tab = []
        self.is_paused = False
        self.InGame = False
        self.user_input = None
        self.grid_row = 15
        self.grid_col = 3
        self.current_game = False

        #sound
        pygame.mixer.init()
        self.mixer =  pygame.mixer
        
        #text settings
        #default sizes
        self.default_title_size = 25
        self.default_button_size = 15
        self.default_setting_size = 12

        #default fonts
        self.dynamic_title_font = tkfont.Font(family = "Cambria", size = self.default_title_size, weight = "bold")
        self.dynamic_button_font = tkfont.Font(family = "Cambria", size = self.default_button_size, weight = "bold")
        self.dynamic_setting_font = tkfont.Font(family = "Cambria", size = self.default_setting_size, weight = "bold")

        #Variable List
        self.setting_fieldname = ['name', 'value', 'category', 'type', 'min_value', 'max_value', 'list_values']
        self.game_names = ['Word Connections']

        #In Game Setting Variables
        self.settings = {}
        self.NumOfPlayers = 1
        self.NumOfWords = 3
        self.Resolution = "500x700"
        
        #Widget Variables
        self.submit_button = StringVar()
        self.user_var = StringVar()
        self.grid_always_on = IntVar()

        # Initial Functions
        self.create_widgets()
        self.get_settings()
        self.display("Menu", Clear=False)
        self.change_grid_dimensions(self.grid_col, self.grid_row)
    
        # Key Binds
        self.root.bind("<Escape>", self.pause_game)
        self.root.bind("<Return>", self.trigger_submit)
        self.root.bind("<Button-1>", lambda event: self.play_sound("MyApp/Sounds/click.wav"))
        #self.root.bind("<Configure>", self.resize_fonts)
        

# region Widget Functions
        #Create Widgets
    def create_widgets(self):

        #Generic Buttons
        self.settings_button = tb.Button(self.root, text = "Settings", bootstyle="info-outline", command = lambda: self.display("Settings"))
        self.quit_button = tb.Button(self.root, text = "Quit", bootstyle="warning-outline", command = self.quit_app)
        self.back_button = tb.Button(self.root, text = "Back", bootstyle="danger-outline", command =  self.go_back_button)
        self.home_button = tb.Button(self.root, text = "Main menu", command = lambda: self.display("Menu"))
        self.sub_btn = tb.Button(self.root,text = 'Submit', command = self.trigger_submit)

        #Menu display
        self.title_label = tb.Label(self.root, text="My Games",font=self.dynamic_title_font)
        self.game_select_button = tb.Button(self.root, text = "Game Select", bootstyle="Primary-outline", command = lambda: self.display("Game Select"))

        #Pause Menu
        self.pause_label = tb.Label(self.root, text="Game Paused", font=self.dynamic_title_font)
        self.resume_button = tb.Button(self.root, text = "Resume", command = self.go_back_button)

        #Game Select display
        self.game_title = tb.Label(self.root, text="Choose Game", font=self.dynamic_title_font)
        self.choice_word_connections = tb.Button(self.root, text = "Word Connections", command = lambda: self.launch_game("Word Connections"))

        #Game Select display
        self.game_setup_title_label = tb.Label(self.root, text=" Game Setup", font=self.dynamic_title_font)

        #Settings display
        self.setttings_frame = tb.Frame(self.root, borderwidth=2, relief="ridge", padding=10)
        self.settings_categories = tb.Notebook(self.setttings_frame)
        self.settings_categories.grid()

        self.setting_tab_general = tb.Frame(self.settings_categories)
        self.setting_tab_word_connections = tb.Frame(self.settings_categories)

        self.settings_categories.add(self.setting_tab_general, text = "General")
        self.settings_categories.add(self.setting_tab_word_connections, text = "Word Connections")
        
        self.settings_label = tb.Label(self.root, text="Settings", font=self.dynamic_title_font)
        self.grid_always_on_button = tb.Checkbutton(self.root, text = "Grid always on", variable = self.grid_always_on , command = self.show_grid())

        #Word Connections display
        self.word_connections_title = tb.Label(self.root, text="Word Connections", font=self.dynamic_title_font)

    def go_back_button(self):
        if len(self.previous_tab) > 1:
            self.previous_tab.pop()
            self.display(self.previous_tab.pop())
            
    def pause_game(self,event = None):
        if len(self.previous_tab) > 1:
            if self.previous_tab[-1] == self.previous_tab[-2]:
                self.previous_tab.pop()
            if not self.current_game or not getattr(self.current_game, "InGame", False):
                self.go_back_button()
            else:
                if self.is_paused:
                    if self.previous_tab[-1] == "Pause":
                        self.is_paused = False
                    self.go_back_button()
                else:
                    self.is_paused = True
                    self.display("Pause")

    def quit_app(self):
        print("Exiting Program")
        try:
            self.current_game.InGame = False
            self.current_game.submit_button.set(1) 
        except:
            pass
        self.root.unbind_all("<Key>")
        self.root.quit()
        self.root.destroy()

    def trigger_submit(self, event = None):
        self.submit_button.set(True)

    def print_previous_tabs(self):
        print(self.previous_tab)

# endregion 

# region Settings Functions   
    #Load/Update Settings
    def get_settings(self, FileName = 'MyApp/Settings.csv'):
        try:
            with open(FileName, "r", newline = '') as csvfile:
                SettingsInfo = csv.DictReader(csvfile, fieldnames=self.setting_fieldname)
                #print(SettingsInfo.fieldnames)

                for line_num, row in enumerate(SettingsInfo):
                    parsed_value = self.safe_literal(row['value'])
                    parsed_list = self.safe_literal(row['list_values'])
                    min_val = self.safe_float(row.get('min_value', None))
                    max_val = self.safe_float(row.get('max_value', None))
                    #print("list = " + str(parsed_list))
                    category = self.setting_tab_general
                    match row['category']:
                        case "General":
                            category = self.setting_tab_general

                        case "Word Connections":
                            category = self.setting_tab_word_connections


                    match line_num:
                        case 0:
                            self.NumOfWords = parsed_value
                            #print("Number of Words = " + str(NumOfWords))
                        case 1:
                            self.NumOfPlayers = parsed_value
                            #print("Number of players = " + str(NumOfPlayers))
                    
                    Setting = SettingOption(
                        line_num=line_num,
                        name=row['name'],
                        value=parsed_value,
                        category=row['category'],
                        category_type = category,
                        type=row['type'].strip(),
                        min_value=min_val,
                        max_value=max_val,
                        list_values=parsed_list
                    )

                    #self.SettingsList.append(row)
                    #Save read information
                    self.settings[row['name']] = Setting
                    #self.save_setting(row['name'], parsed_value)
            
        
        except FileNotFoundError:
            print("Settings file not found")

    def modify_file(self, file_name, row_id, col_id, new_value):
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

    def save_setting(self, setting_name, value):
        self.settings[setting_name].value = value
        self.modify_file('MyApp/Settings.csv', self.settings[setting_name].line_num, 1, int(float(value)))

    def update_setting(self, value, setting_name, label = None):
        
        self.settings[setting_name].value = int(float(value))
        if label:
            label.config(text=f"{int(float(value))}")
        self.modify_file('MyApp/Settings.csv', self.settings[setting_name].line_num, 1, int(float(value)))
    
    #Safe reading
    def safe_literal(self, value):
        try:
            return ast.literal_eval(value)
        except:
            return value
        
    def safe_float(self, value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

        
# endregion

# region Display Functions  
    # Show initial menu
    def display(self, State, Clear = True):
            if Clear:
                self.clear_window()
                
            match State:
                case "Menu":
                    self.previous_tab.clear()
                    self.is_paused = False
                    self.current_game = None
                    self.previous_tab.append("Menu")
                    #self.show_grid(self.grid_size, self.grid_size)
                    #self.my_frame.grid(row = 0, column = 0, padx = 0, pady = 50, columnspan=1, sticky="nsew")
                    self.title_label.grid(row = 0, column = 1, ipadx = 0, ipady = 0, columnspan=1, sticky="")
                    self.game_select_button.grid(row = 2, column = 1, padx = 5, pady = 5, columnspan=1, sticky="ew")
                    self.settings_button.grid(row = 3,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="ew")
                    self.quit_button.grid(row = 4,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="ew")

                case "Pause":
                    self.previous_tab.append("Pause")
                    self.pause_label.grid(row = 0,  column = 0, padx = 0, pady = 0, columnspan=3, sticky="ns")
                    self.resume_button.grid(row = 3,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.settings_button.grid(row = 4,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.home_button.grid(row = 5,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.quit_button.grid(row = 6,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")

                case "Settings":
                    self.previous_tab.append("Settings")
                    self.settings_label.grid(row = 0,  column = 1, padx = 5, pady = 5)
                    self.get_settings()
                    self.display_settings()
                    

                case "Word Connections":
                    self.previous_tab.append("Word Connections")
                    self.current_game.update_word_connection_display()

                case "Game Select":
                    self.previous_tab.append("Game Select")
                    self.game_title.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan=3, sticky="ns")
                    self.choice_word_connections.grid(row = 1, column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.back_button.grid(row = 2, column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")

    def change_resolution(self, event):
        
        self.settings['Resolution'].value = event.widget.get()

        #convert string to in for both dimensions
        change_number = False
        number_string = "" 
        for i in self.settings['Resolution'].value:
            
            if  self.safe_float(i) == None:
                change_number = True
                self.current_dimensions[0] = int(self.safe_float(number_string))
                number_string = ""
            elif change_number == False:
                number_string = number_string + i
                #print(number_string)
            else: 
                number_string = number_string + i
                #print(number_string)
        self.current_dimensions[1] = int(self.safe_float(number_string))
            
        root.geometry(event.widget.get()) # width x height
        self.resize_fonts(self.current_dimensions[0])

        self.change_grid_dimensions()

    def change_grid_dimensions(self, col = None, row = None, minsize = 50):
            if col == None:
                col = self.grid_col
            self.grid_col = col

            if row == None:
                row = self.grid_row 
            self.grid_row = row
            
    
            self.root.grid_columnconfigure(0, weight=1, minsize=self.current_dimensions[0]/self.grid_col)
            self.root.grid_rowconfigure(0, weight=0, minsize=10)

            for i in range(1,self.grid_col):
                self.root.grid_columnconfigure(i, weight=1, minsize=self.current_dimensions[0]/self.grid_col)

            for i in range(1,self.grid_row):
                self.root.grid_rowconfigure(i, weight=0, minsize=minsize)
            #self.show_grid(self.grid_row, self.grid_col)

    def resize_fonts(self, width):
        title_width_scale = max(self.default_title_size, int(width/ 30))
        button_width_scale = max(self.default_button_size, int(width/ 30))
        setting_width_scale = max(self.default_setting_size, int(width/ 80))

        #print(width_scale)
        self.dynamic_title_font.configure(size = title_width_scale)
        self.dynamic_button_font.configure(size = button_width_scale)
        self.dynamic_setting_font.configure(size = setting_width_scale)

    def display_settings(self):
        last_row = 0
        for i, (CurrentSetting, item) in enumerate(self.settings.items()):
            
            label = Label(item.category_type, text = item.name, font = self.dynamic_setting_font)
            label.grid(row = i + 1, column = 0, padx = 5, pady = 5)
            last_row =  i + 1

            match item.type:
                case "Slider":
                    
                    variable_label = Label(item.category_type, text = item.value, font = self.dynamic_setting_font)
                    variable_label.grid(row = i + 1, column = 2, padx = 5, pady = 5)

                    slider = Scale(item.category_type, orient = "horizontal", from_ = item.min_value, to = item.max_value) 
                    slider.set(item.value)
                    slider.grid(row = i + 1, column = 1, padx = 5, pady = 5)
                    slider.config(command = lambda value, index = CurrentSetting, lbl = variable_label: self.update_setting(value, index, lbl))
                    if item.name == "Master Volume":
                        slider.bind("<ButtonRelease-1>", self.change_volume)

                    
                    
                case "Combobox":
                    selected_option = tk.StringVar()
                    Combo = Combobox(item.category_type, textvariable = selected_option, values = item.list_values) 
                    Combo.set(item.value)
                    Combo.grid(row = i + 1, column = 1, padx = 5, pady = 5)

                    #bind combo box
                    if item.name == "Resolution":
                        Combo.bind("<<ComboboxSelected>>", self.change_resolution)

        self.setttings_frame.grid(column=0, row = 1, columnspan=self.grid_col, rowspan = last_row+1, sticky = "nsew")                
        self.grid_always_on_button.grid(row = last_row + 1,  column = 1, padx = 5, pady = 5)
        self.back_button.grid(row = last_row + 2,  column = 1, padx = 5, pady = 5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()
        self.show_grid()

    def show_grid(self):
        if self.grid_always_on.get() == 1:
            for row in range(self.grid_row):
                self.root.grid_rowconfigure(row, weight=0)
                for col in range(self.grid_col):
                    self.root.grid_columnconfigure(col, weight=0)
                    cell = tk.Frame(self.root, bg="lightgrey", borderwidth=1, relief="solid")
                    cell.grid(row=row, column=col, sticky="nsew")
                    cell.lower()

# endregion                   

# region Start App/Game Functions

    def launch_game(self, app_name):
        self.clear_window()
        self.previous_tab.append(app_name)

        match app_name:
            case "Word Connections":
                from Apps.Word_Connections.word_connections_data import wc
                from Apps.Word_Connections.word_connections import WordConnectionsGame
               
                self.current_game = WordConnectionsGame(self.root, self.settings, wc)
                self.current_game.word_connections_game()
                try: 
                    crash = Label(self.root)
                except tk.TclError:
                    return
                
                self.home_button.grid(row = 2, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
                self.game_select_button.grid(row = 3, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
                self.quit_button.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")


                
# endregion

# region Sound Functions
    def play_sound(self, file_location):
        try:
            self.sound = self.mixer.Sound(file_location) # Load a sound file
            self.sound.set_volume(self.settings["Master Volume"].value/100)
            self.sound.play() # Play the sound
        except FileNotFoundError:
            print("Sound file not found!")

    def change_volume(self, event):
        self.settings["Master Volume"].value = event.widget.get()
        self.update_setting(self.settings["Master Volume"].value, "Master Volume")

# endregion 

# endregion

if __name__ == "__main__":
    root = tb.Window(themename="solar")
    app = AppData(root)
    root.mainloop()