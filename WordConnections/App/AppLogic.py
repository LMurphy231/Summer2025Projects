import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import csv
import ast
import random



class SettingOption:
    def __init__(self, name, line_num, value, category, type, min_value = None, max_value = None, list_values = None):
        self.line_num = line_num
        self.name = name
        self.value = value
        self.category =category
        self.type = type
        self.min_value = min_value
        self.max_value = max_value
        self.list_values = list_values
        
    def __str__(self):
        return f"SettingOption(name={self.name}, line_num={self.line_num}, value={self.value}, category={self.category}, type={self.type}, min_value={self.min_value}, max_value={self.max_value}, list_values={self.list_values})"

# region        classes
class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.default_dimensions = [500, 700]
        self.previous_tab = []
        self.is_paused = False
        self.InGame = False
        self.user_input = None
        self.grid_row = 3
        self.grid_col = 3
        self.create_widgets()
        self.display("Menu", Clear=False)
        self.change_grid_dimensions()

        # Key Binds
        self.root.bind("<Escape>", self.pause_game)
        self.root.bind("<Return>", self.trigger_submit)

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
        self.user_var = tk.StringVar()
        

# region Widget Functions
        #Create Widgets
    def create_widgets(self):

        #Generic Buttons
        self.Settings = tb.Button(self.root, text = "Settings", bootstyle="info-outline", command = lambda: self.display("Settings"))
        self.Quit = tb.Button(self.root, text = "Quit", bootstyle="warning-outline", command = self.quit_app)
        self.Back = tb.Button(self.root, text = "Back", bootstyle="danger-outline", command =  self.back_button)
        self.home_button = tb.Button(self.root, text = "Main menu", command = lambda: self.display("Menu"))
        self.sub_btn = tb.Button(self.root,text = 'Submit', command = self.trigger_submit)

        #Menu display
        self.TitleLabel = tb.Label(self.root, text="My Games", font=("Cambria 25 bold"))
        self.GameSelect = tb.Button(self.root, text = "Game Select", bootstyle="Primary-outline", command = lambda: self.display("Game Select"))

        #Pause Menu
        self.pause_label = tb.Label(self.root, text="Game Paused", font=("Cambria 25 bold"))
        self.resume_button = tb.Button(self.root, text = "Resume", command = self.resume_game)

        #Game Select display
        self.game_title = tb.Label(self.root, text="Choose Game", font=("Cambria 25 bold"))
        self.choice_word_connections = tb.Button(self.root, text = "Word Connections", command = lambda: self.display("Word Connections"))

        #Game Select display
        self.GameSetupTitleLabel = tb.Label(self.root, text=" Game Setup", font=("Cambria 25 bold"))

        #Settings display
        self.my_frame = tb.Frame(self.root, borderwidth=2, relief="ridge", padding=10)
        self.SettingsLabel = tb.Label(self.root, text="Settings", font=("Cambria 25 bold"))

        #Word Connections display
        self.word_connections_title = tb.Label(self.root, text="Word Connections", font=("Cambria 25 bold"))

    def back_button(self):
        if len(self.previous_tab) > 1:
            self.previous_tab.pop()
            self.display(self.previous_tab.pop())

    def resume_game(self):
        self.pause_game()

    def pause_game(self,event = None):

        if self.is_paused & (self.previous_tab[len(self.previous_tab)-2] in self.game_names):
            self.is_paused = False
            self.previous_tab.pop()
            self.Display(self.previous_tab.pop())
        elif (self.previous_tab[len(self.previous_tab)-1] in self.game_names):
            self.is_paused = True
            self.Display("Pause")

        else:
            self.back_button()

    def quit_app(self):
        print("Exiting Program")
        self.root.unbind_all("<Key>")
        self.InGame = False
        self.root.destroy()
        self.root.update()

    def trigger_submit(self, event = None):
        self.submit_button.set(True)


# endregion 

# region Settings Functions   
    #Load/Update Settings
    def get_settings(self, FileName = 'WordConnections/App/Settings.csv'):
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

    def save_setting(self, setting_name, value):
        self.settings[setting_name].value = value
        self.modify_file('WordConnections/App/Settings.csv', self.settings[setting_name].line_num, 1, int(float(value)))

    def update_setting(self, value, setting_name, label = None):
        self.settings[setting_name].value = int(float(value))
        if label:
            label.config(text=f"{int(float(value))}")
        self.modify_file('WordConnections/App/Settings.csv', self.settings[setting_name].line_num, 1, int(float(value)))
    
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
                    self.previous_tab.append("Menu")
                    #self.show_grid(self.grid_size, self.grid_size)
                    #self.my_frame.grid(row = 0, column = 0, padx = 0, pady = 50, columnspan=1, sticky="nsew")
                    self.TitleLabel.grid(row = 0, column = 1, ipadx = 0, ipady = 0, columnspan=1, sticky="")
                    self.GameSelect.grid(row = 1, column = 1, padx = 5, pady = 5, columnspan=1, sticky="ew")
                    self.Settings.grid(row = 2,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="ew")
                    self.Back.grid(row = 3,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="ew")
                    self.Quit.grid(row = 4,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="ew")

                case "Pause":
                    self.previous_tab.append("Pause")
                    self.pause_label.grid(row = 0,  column = 1, padx = 0, pady = 0, columnspan=1, sticky="nsew")
                    self.resume_button.grid(row = 3,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.Settings.grid(row = 4,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.home_button.grid(row = 5,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.Quit.grid(row = 6,  column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")

                case "Settings":
                    self.previous_tab.append("Settings")
                    self.SettingsLabel.grid(row = 0,  column = 1, padx = 5, pady = 5)
                    self.get_settings()
                    self.display_settings()
                    self.Back.grid(row = 4,  column = 1, padx = 5, pady = 5)

                case "Word Connections":
                    self.previous_tab.append("Word Connections")
                    self.word_connections_title.grid(row = 0,  column = 1, padx = 0, pady = 0, columnspan=1, sticky="nsew")
                    if self.InGame == False: #game has not started
                        self.setup_word_connections()

                    self.word_connections_game()
                    
                    
                    #Back.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    #Quit.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan=1, sticky="nsew")

                case "Game Select":
                    self.previous_tab.append("Game Select")
                    self.game_title.grid(row = 0, column = 1, padx = 0, pady = 0, columnspan=1, sticky="nsew")
                    self.choice_word_connections.grid(row = 1, column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")
                    self.Back.grid(row = 2, column = 1, padx = 5, pady = 5, columnspan=1, sticky="nsew")

    def change_resolution(self, event):
        
        self.settings['Resolution'].value = event.widget.get()

        #convert string to in for both dimensions
        change_number = False
        number_string = "" 
        for i in self.settings['Resolution'].value:
            
            if  self.safe_float(i) == None:
                change_number = True
                self.default_dimensions[0] = int(self.safe_float(number_string))
                number_string = ""
            elif change_number == False:
                number_string = number_string + i
                #print(number_string)
            else: 
                number_string = number_string + i
                #print(number_string)
        self.default_dimensions[1] = int(self.safe_float(number_string))
            
        root.geometry(event.widget.get()) # width x height


        self.change_grid_dimensions()

    def change_grid_dimensions(self, minsize = 20):
            self.root.grid_columnconfigure(0, weight=1, minsize=self.default_dimensions[0]/self.grid_col)
            self.root.grid_rowconfigure(0, weight=0, minsize=10)

            for i in range(1,self.grid_col):
                self.root.grid_columnconfigure(i, weight=1, minsize=self.default_dimensions[0]/self.grid_col)

            for i in range(1,self.grid_row):
                self.root.grid_rowconfigure(i, weight=0, minsize=minsize)
            #self.show_grid(self.grid_row, self.grid_col)

    def display_settings(self):
        for i, (CurrentSetting, item) in enumerate(self.settings.items()):
            
            label = Label(root, text = item.name, font = "Arial 12 bold")
            label.grid(row = i + 1, column = 0, padx = 5, pady = 5)
            

            match item.type:
                case "Slider":
                    
                    variable_label = Label(self.root, text = item.value, font = "Arial 10 bold")
                    variable_label.grid(row = i + 1, column = 2, padx = 5, pady = 5)

                    slider = Scale(self.root, orient = "horizontal", from_ = item.min_value, to = item.max_value) 
                    slider.set(item.value)
                    slider.grid(row = i + 1, column = 1, padx = 5, pady = 5)
                    slider.config(command = lambda value, index = i, lbl = variable_label: self.update_setting(value, index, lbl))

            
                    
                    slider.config(command = lambda value, index = i, lbl = variable_label: self.update_setting(value, index, lbl))
                    
                case "Combobox":
                    selected_option = tk.StringVar()
                    Combo = Combobox(self.root, textvariable = selected_option, values = item.list_values) 
                    Combo.set(item.value)
                    Combo.grid(row = i + 1, column = 1, padx = 5, pady = 5)
                    #bind resolution combo box
                    if item.name == "Resolution":
                        Combo.bind("<<ComboboxSelected>>", self.change_resolution)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.grid_forget()

    def show_grid(self, rows= 10, columns=10):
        for row in range(rows):
            self.root.grid_rowconfigure(row, weight=1)
            for col in range(columns):
                self.root.grid_columnconfigure(col, weight=1)
                cell = tk.Frame(self.root, bg="lightgrey", borderwidth=1, relief="solid")
                cell.grid(row=row, column=col, sticky="nsew")

# endregion                   


# endregion

if __name__ == "__main__":
    root = tb.Window(themename="solar")
    app = GameApp(root)
    
    root.mainloop()