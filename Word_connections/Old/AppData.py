import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import csv
import ast
import random
from MyApp.Apps.Word_Connections.word_connections_data import wc
import time

root = tk.Tk()


root.geometry("500x700") # width x height
root.resizable(False,False)


# region        Settings Functions
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
                    #print("Number of Words = " + str(NumOfWords))
                case 1:
                    global NumOfPlayers 
                    NumOfPlayers = parsed_value
                    #print("Number of players = " + str(NumOfPlayers))



            
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
        print("Current setting = " + str(CurrentSetting))
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

def update_setting(value, i, label = None):
    SettingsList[i].value = int(float(value))
    if label:
        label.config(text=f"{int(float(value))}")
    #print(SettingsList[i].line_num)
    #print(int(float(value)))
    modify_file('WordConnections/App/Settings.csv', SettingsList[i].line_num, 1, int(float(value)))
    
    return 0
# endregion

# region        Button Functions 
def quit_app():
    print("Exiting Program")
    root.unbind_all("<Key>")
    InGame = False
    root.destroy()
    root.update()
# endregion

is_paused = False
# region        Pause/Resume Game
game_names = ["Word Connections"]
def pause_game(event = None):
    global is_paused
    #try:
    #    print(previous_tab[len(previous_tab)-1])
    #except:
    #    return
    if is_paused & (previous_tab[len(previous_tab)-2] in game_names):
        is_paused = False
        #print("unpausing game")
        previous_tab.pop()
        Display(previous_tab.pop())
    elif (previous_tab[len(previous_tab)-1] in game_names):
        is_paused = True
        #print("Pausing game")
        Display("Pause")

    else:
        back_button()

def resume_game():
    #print(previous_tab[len(previous_tab)-1])
    pause_game()

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
# endregion 

NumOfPlayers = 0
NumOfWords = 0

# region        Word Connections
def setup_word_connections():
    get_settings()
    SetupPlayers(NumOfPlayers)
    GetWordList()

InGame = False
def word_connections_game():
    global InGame
    InGame = True
    while InGame:
        for i in range(NumOfPlayers):
            while True:
                if not Turn(i):
                    break

        if CheckPlayerVictories() == 2:
            #print("Reseting Players")
            InGame = True
            ResetPlayers()
        elif CheckPlayerVictories() == 1:
            InGame = False
            break

    AnnounceWinner()
    #("GAME OVER!!")

global submit_button
submit_button = StringVar()

def trigger_submit(event = None):
    submit_button.set(True)
    
root.bind("<Return>", trigger_submit)

def update_word_connection_display(PlayerNum):
    clear_window()
    #print("updating game screen")
    word_connections_title.grid(row = 0, column = 1, padx = 0, pady = 25, columnspan=2, sticky="n")
    current_player_title = Label(root, text = "Player " + str(PlayerNum + 1) + " is up!", font = "Arial 15 bold")
    current_player_title.grid(row = 1, column = 0, padx = 0, pady = 5, columnspan=3, sticky="n")

    displayed_words = []

    for i in range(0,NumOfWords):
        label = Label(root, text = Player[PlayerNum].HiddenCharList[i], font = "Arial 12 bold")
        label.grid(row = i + 2, column = 1, padx = 5, pady = 0)
        displayed_words.append(label)

    global guess_var
    global sub_btn
    global guess_entry

    guess_var = tk.StringVar() 
    guess_entry = Entry(root,textvariable = guess_var, font=('calibre',10,'normal'))
    
    sub_btn = Button(root,text = 'Submit', command = trigger_submit)
    guess_entry.grid(row = NumOfWords+2, column = 1, padx=(10, 2), pady=10, sticky="ew")
    sub_btn.grid(row = NumOfWords+2, column = 2, padx=(10, 2), pady=10, sticky="w")
    guess_entry.focus_set()

user_guess = ""    
def Get_UserGuess():

    global user_guess
    user_guess = guess_var.get()
    #print(user_guess)
    guess_var.set("")
    
def victory_screen(PlayerNum):
    clear_window()
    #print("updating to victory screen")
    word_connections_victory_title = Label(root, text = "Player " + str((PlayerNum + 1)) + " has won!!!", font = "Cambria 25 bold")
    word_connections_victory_title.grid(row = 0, column = 1, padx = 125, pady = 25, columnspan=3, sticky="n")
    home_button.grid(row = 2, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
    GameSelect.grid(row = 3, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
    Quit.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
    ResetPlayers(NumOfPlayers)
    InGame == False
# endregion 

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
            resume_button.grid(row = 3, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Settings.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            home_button.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Quit.grid(row = 6, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")

        case "Settings":
            previous_tab.append("Settings")
            SettingsLabel.grid(row = 0, column = 0, padx = 5, pady = 5)
            get_settings()
            display_settings()
            Back.grid(row = 4, column = 0, padx = 5, pady = 5)

        case "Word Connections":
            previous_tab.append("Word Connections")
            word_connections_title.grid(row = 0, column = 0, padx = 125, pady = 50, columnspan=3, sticky="n")
            if InGame == False: #game has not started
                setup_word_connections()

            word_connections_game()
            
            
            #Back.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            #Quit.grid(row = 5, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")

        case "Game Select":
            previous_tab.append("Game Select")
            game_title.grid(row = 0, column = 0, padx = 125, pady = 50, columnspan=3, sticky="n")
            choice_word_connections.grid(row = 2, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            Back.grid(row = 4, column = 0, padx = 5, pady = 5, columnspan=3, sticky="n")
            
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

#Generic Buttons
Settings = Button(root, text = "Settings", command = lambda: Display("Settings"))
Quit = Button(root, text = "Quit", command = quit_app)
Back = Button(root, text = "Back", command =  back_button)
home_button = Button(root, text = "Main menu", command = lambda: Display("Menu"))

#Menu Display
TitleLabel = Label(root, text="My Games", font=("Cambria 25 bold"))
GameSelect = Button(root, text = "Game Select", command = lambda: Display("Game Select"))

#Pause Menu
pause_label = Label(root, text="Game Paused", font=("Cambria 25 bold"))
resume_button = Button(root, text = "Resume", command = resume_game)

#Game Select Display
game_title = Label(root, text="Choose Game", font=("Cambria 25 bold"))
choice_word_connections = Button(root, text = "Word Connections", command = lambda: Display("Word Connections"))

#Game Select Display
GameSetupTitleLabel = Label(root, text=" Game Setup", font=("Cambria 25 bold"))

#Settings Display
SettingsLabel = Label(root, text="Settings", font=("Cambria 25 bold"))

#Word Connections Display
word_connections_title = Label(root, text="Word Connections", font=("Cambria 25 bold"))

#Key Binds
root.bind("<Escape>", pause_game)


# region Word Connection Logic

class PlayerStats:
    def __init__(self, WordList, IndexList, CurrentIndex, CharList, HiddenCharList, CurrentChar, HasWon):
        self.WordList = WordList
        self.IndexList = IndexList
        self.CurrentIndex = CurrentIndex
        self.CharList = CharList
        self.HiddenCharList = HiddenCharList
        self.CurrentChar = CurrentChar
        self.HasWon = HasWon
        
    def __str__(self):
        return f"Player(WordList={self.WordList}, IndexList={self.IndexList}, CharList={self.CharList}, CurrentIndex={self.CurrentIndex}, CurrentChar={self.CurrentChar}, HasWon={self.HasWon})"
        
Player = []






def FindNameIndex(name):
    for index, obj in enumerate(wc):
        if name in obj.name:
            return index
    return -1

def ChooseNextWord(CurrentIndex):
    NewId = random.randint(0,len(wc[CurrentIndex].connection))
    NextWord = wc[CurrentIndex].connection[NewId]
    #print("Next word is " + NextWord)
    return FindNameIndex(NextWord)



def GetWordList():
    
    WordList = []
    WordList.append(wc[random.randint(0,len(wc))].name)
    CurrentIdList = []
    CurrentIdList.append(FindNameIndex(WordList[0]))
    for i in range(1,NumOfWords):
        ChooseWord = True #If Word still needs to be chosen
        while ChooseWord:
            NewId = random.randint(0,len(wc[CurrentIdList[i-1]].connection)-1) #randomly choose after word
            NextWord = wc[CurrentIdList[i-1]].connection[NewId]
            if NextWord != "":  #if choosen word is not empty save it
                CurrentIdList.append(FindNameIndex(NextWord))
                WordList.append(wc[CurrentIdList[i]].name)
                ChooseWord = False

    return WordList, CurrentIdList
        
def GetCharList(List):
    WordCharList = []
    HiddenCharList = []
    for i in range(len(List)):
        TempList = []
        TempCharList = []

        for char in List[i]:
            TempCharList.append(char)
            TempList.append('_')

        TempList[0] = List[i][0]
        HiddenCharList.append(TempList)
        WordCharList.append(TempCharList)
        HiddenCharList[0] = WordCharList[0]
    return WordCharList, HiddenCharList

def UpdateCharList(index, PlayerNum):
    CurrentWord = Player[PlayerNum].WordList[Player[PlayerNum].CurrentIndex]
    Word = CurrentWord
    for i in range(1,len(Word)):
        if Player[PlayerNum].HiddenCharList[index][i]== '_':
            Player[PlayerNum].HiddenCharList[index][i] = Word[i]
            return
        
def GetUserGuess(PlayerNum):
    if Player[PlayerNum].CurrentIndex >= NumOfWords: #prevents out of index
        return True
    root.wait_variable(submit_button)
    Get_UserGuess()
    #print(user_guess)
    return CheckUserGuess(user_guess, PlayerNum)



def CheckUserGuess(UserInput, PlayerNum):
    if UserInput.lower() == Player[PlayerNum].WordList[Player[PlayerNum].CurrentIndex].lower(): #User correct
        #print("That is correct!!")
        return True
    else:
        #print("Sorry that is incorrect ") #User incorrect
        return False
    

    
def SetupPlayers(NumOfPlayers):
    #Limit number of players
    

    #print("Number of players: " + str(NumOfPlayers))

    for i in range(NumOfPlayers):
        #print("Setting up player " + str(i))
        WordList, IndexList = GetWordList()
        WordCharList, HiddenCharList = GetCharList(WordList)
        Player.append(PlayerStats(WordList, IndexList, 1, WordCharList, HiddenCharList, 1, False))
        #PrintPlayerStats(i)
    return

def ResetPlayers(NumOfPlayers):
    #print("More than one player has won at the same time, resetting players until a single player has won")
    
    
    for i in range(NumOfPlayers):
        WordList, IndexList = GetWordList()
        WordCharList, HiddenCharList = GetCharList(WordList)
        Player[i] = PlayerStats(WordList, IndexList, 1, WordCharList, HiddenCharList, 1, False)
        #PrintPlayerStats(i)
    return
    
    



def PrintList(List):
    for i in range(len(List)):
        print(List[i])



def PrintPlayerStats(PlayerNum):
    print("Player " + str(PlayerNum + 1) + " Stats: ")
    print()
    
    #Print word list
    print("Word List: ")
    PrintList(Player[PlayerNum].WordList)
    print()

    #Print Char List
    print("Char List: ")
    PrintList(Player[PlayerNum].CharList)

    #Print hidden char list
    print("Hidden Char List: ")
    print()
    for i in range(NumOfWords):
        print(''.join(Player[PlayerNum].HiddenCharList[i]))
    print()
    print(Player[PlayerNum].HasWon)


#Player Turn
def Turn(PlayerNum):
    #Make Sure player hasnt won
    
    #print("Player " + str(PlayerNum + 1) + " is up!") #Introduce player
    #print()
    
    #Print current shown list
    update_word_connection_display(PlayerNum)
    #for i in range(NumOfWords):
    #    print(''.join(Player[PlayerNum].HiddenCharList[i]))
    #print()

    #Get User guess and check if it is correct
    if GetUserGuess(PlayerNum):
        #print("Current Index = " + str(Player[PlayerNum].CurrentIndex))
        Player[PlayerNum].HiddenCharList[Player[PlayerNum].CurrentIndex] = Player[PlayerNum].CharList[Player[PlayerNum].CurrentIndex]
        #print(''.join(Player[PlayerNum].HiddenCharList[Player[PlayerNum].CurrentIndex]))
        #print()
        Player[PlayerNum].CurrentChar = 1 #Reset current char to first letter
        Player[PlayerNum].CurrentIndex += 1 #Incriminte word counter by 1

        #If player exceeds number of words announce they have finished
        if Player[PlayerNum].CurrentIndex >= NumOfWords:
            #print("Player " + str(PlayerNum + 1) + " has finished their list!")
            Player[PlayerNum].HasWon = True
            return False
        
        return True


    else: 
        if Player[PlayerNum].CurrentIndex >= NumOfWords:
            return False
        #print()
        UpdateCharList(Player[PlayerNum].CurrentIndex,PlayerNum)
        return False
      

def CheckPlayerVictories():
    counter = 0
    for i in range(NumOfPlayers):
        if Player[i].HasWon:
            counter += 1
            #print(str(counter))

    if counter == 1: #one player has won
        return 1
    elif counter == 0: #No one has won
        return 0
    return 2 #more than one player has won


def AnnounceWinner():
    if NumOfPlayers > 0:
        for i in range(NumOfPlayers):
            if Player[i].HasWon:
                update_word_connection_display(i)
                #print("Player " + str(i + 1) + " has won!!!!")
                victory_screen(i)
                return
    #else:
        #print("You Win!!!!")

# endregion

# Set the Window title
Display("Menu", False)
root.title("My Python Window")
root.mainloop()
input("Press Enter to close the program...")