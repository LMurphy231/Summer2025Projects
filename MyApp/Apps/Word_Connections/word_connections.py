import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.font as tkfont
import time

import random

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
      
class WordConnectionsGame:
    def __init__(self, root, settings, wc):
        self.root = root
        self.settings = settings

        self.player = []
        self.InGame = False
        self.game_over = False
        self.root_destroyed = False
        self.wc = wc
        self.default_title_size = 25
        self.dynamic_title_font = tkfont.Font(family = "Cambria", size = self.default_title_size, weight = "bold")
        self.current_player = 0
        self.submit_button = StringVar()
        self.guess_var = StringVar()
        self.create_widgets()
        
        #keybinds
        self.root.bind("<Return>", self.trigger_submit)        

# region Game Setup
    def GetWordList(self):
        
        WordList = []
        WordList.append(self.wc[random.randint(0,len(self.wc)-1)].name)
        
        CurrentIdList = []
        CurrentIdList.append(self.FindNameIndex(WordList[0]))
        for i in range(1,self.settings['WordCount'].value):
            ChooseWord = True #If Word still needs to be chosen
            while ChooseWord:
                NewId = random.randint(0,len(self.wc[CurrentIdList[i-1]].connection)-1) #randomly choose after word
                NextWord = self.wc[CurrentIdList[i-1]].connection[NewId]
                if NextWord != "":  #if choosen word is not empty save it
                    CurrentIdList.append(self.FindNameIndex(NextWord))
                    WordList.append(self.wc[CurrentIdList[i]].name)
                    ChooseWord = False

        return WordList, CurrentIdList
            
    def GetCharList(self, List):
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

    def SetupPlayers(self):
        #Limit number of players
        for i in range(self.settings['PlayerCount'].value):
            #print("Setting up player " + str(i))
            WordList, IndexList = self.GetWordList()
            WordCharList, HiddenCharList = self.GetCharList(WordList)
            self.player.append(PlayerStats(WordList, IndexList, 1, WordCharList, HiddenCharList, 1, False))
            #PrintPlayerStats(i)
        return


# endregion

# region Turn Functions
    def FindNameIndex(self, name):
        for index, obj in enumerate(self.wc):
            if name in obj.name:
                return index
        return -1

    def ChooseNextWord(self, CurrentIndex):
        NewId = random.randint(0,len(self.wc[CurrentIndex].connection))
        NextWord = self.wc[CurrentIndex].connection[NewId]
        #print("Next word is " + NextWord)
        return self.FindNameIndex(NextWord)

    def UpdateCharList(self, index):
        CurrentWord = self.player[self.current_player ].WordList[self.player[self.current_player ].CurrentIndex]
        Word = CurrentWord
        for i in range(1,len(Word)):
            if self.player[self.current_player ].HiddenCharList[index][i]== '_':
                self.player[self.current_player ].HiddenCharList[index][i] = Word[i]
                return

    def GetUserGuess(self):
        if self.player[self.current_player ].CurrentIndex >= self.settings['WordCount'].value: #prevents out of index
            return True
        self.submit_button.set(0)  # reset button
        self.root.wait_variable(self.submit_button)
        #self.wait_for_user_input()
            
        return self.CheckUserGuess(self.guess_var.get())

    def CheckUserGuess(self, UserInput):
        self.guess_var.set("")
        if UserInput.lower() == self.player[self.current_player ].WordList[self.player[self.current_player ].CurrentIndex].lower(): #User correct
            #print("That is correct!!")
            return True
        else:
            #print("Sorry that is incorrect ") #User incorrect
            return False
        
    def PrintList(self, List):
        for i in range(len(List)):
            print(List[i])

    def PrintPlayerStats(self):
        print("Player " + str(self.current_player  + 1) + " Stats: ")
        print()
        
        #Print word list
        print("Word List: ")
        self.PrintList(self.player[self.current_player ].WordList)
        print()

        #Print Char List
        print("Char List: ")
        self.PrintList(self.player[self.current_player ].CharList)

        #Print hidden char list
        print("Hidden Char List: ")
        print()
        for i in range(self.settings['WordCount'].value):
            print(''.join(self.player[self.current_player ].HiddenCharList[i]))
        print()
        print(self.player[self.current_player ].HasWon)

    #Player Turn
    def Turn(self):
        try: 
            crash = Label(self.root)
        except tk.TclError:
            self.InGame = False
            return
        
        self.update_word_connection_display()
        
        #Get User guess and check if it is correct
        if self.GetUserGuess():
            self.player[self.current_player ].HiddenCharList[self.player[self.current_player ].CurrentIndex] = self.player[self.current_player ].CharList[self.player[self.current_player ].CurrentIndex]
            self.player[self.current_player ].CurrentChar = 1 #Reset current char to first letter
            self.player[self.current_player ].CurrentIndex += 1 #Incriminte word counter by 1

            #If player exceeds number of words announce they have finished
            if self.player[self.current_player ].CurrentIndex >= self.settings['WordCount'].value:
                #print("Player " + str(self.current_player  + 1) + " has finished their list!")
                self.player[self.current_player ].HasWon = True
                return False
            
            return True


        else: 
            if self.player[self.current_player ].CurrentIndex >= self.settings['WordCount'].value:
                return False
            #print()
            self.UpdateCharList(self.player[self.current_player ].CurrentIndex)
            return False
        
    def setup_word_connections(self):
        self.SetupPlayers()
        self.GetWordList()

    def word_connections_game(self):
        self.setup_word_connections()
        self.game_over = False
        self.InGame = True
        while self.InGame:
            for i in range(self.settings['PlayerCount'].value):
                self.current_player = i
                while True:
                    if not self.Turn():
                        break

            if self.CheckPlayerVictories() == 2:
                #print("Reseting Players")
                InGame = True
                self.ResetPlayers()
            elif self.CheckPlayerVictories() == 1:
                InGame = False
                break

        self.AnnounceWinner()
    #("GAME OVER!!")
# endregion 

# region Display Functions

    def create_widgets(self):

        #Generic Buttons
        self.sub_btn = tb.Button(self.root,text = 'Submit', command = self.trigger_submit)
        self.guess_entry = Entry(self.root,textvariable = self.guess_var, font=('calibre',10,'normal'))
        #Word Connections display
        self.word_connections_title = tb.Label(self.root, text="Word Connections", font=self.dynamic_title_font)
    
    def trigger_submit(self, event = None):
        self.submit_button.set(True)
    
    def update_word_connection_display(self):
        try:
            self.clear_window()
            #print("updating game screen")
            self.word_connections_title.grid(row = 0, column = 0, padx = 0, pady = 0, columnspan=3, sticky="ns")
            current_player_title = Label(self.root, text = "Player " + str(self.current_player  + 1) + " is up!", font = "Arial 15 bold")
            current_player_title.grid(row = 1, column = 0, padx = 0, pady = 5, columnspan=3, sticky="n")

            displayed_words = []

            for i in range(0,self.settings['WordCount'].value):
                label = Label(self.root, text = self.player[self.current_player ].HiddenCharList[i], font = "Arial 12 bold")
                label.grid(row = i + 2, column = 1, padx = 5, pady = 0)
                displayed_words.append(label)

            
            
            self.guess_entry.grid(row = self.settings['WordCount'].value+2, column = 1, padx=(10, 2), pady=10, sticky="ew")
            self.sub_btn.grid(row = self.settings['WordCount'].value+2, column = 2, padx=(10, 2), pady=10, sticky="w")
            self.guess_entry.focus_set()
        except tk.TclError:
            print("ERROR")
            pass
        
    def clear_window(self):
        #self.create_widgets()
        try:
            if not self.root_destroyed:
                for widget in self.root.winfo_children():
                    widget.grid_forget()
        except tk.TclError:
            print("crashed at clear window")
            self.InGame = False
            pass
        

# endregion

# region End Game Functions
    def ResetPlayers(self):
        #print("More than one player has won at the same time, resetting players until a single player has won")
        
        
        for i in range(self.settings['PlayerCount'].value):
            WordList, IndexList = self.GetWordList()
            WordCharList, HiddenCharList = self.GetCharList(WordList)
            self.player[i] = PlayerStats(WordList, IndexList, 1, WordCharList, HiddenCharList, 1, False)
            #PrintPlayerStats(i)
        return    
    
    def CheckPlayerVictories(self):
        counter = 0
        for i in range(self.settings['PlayerCount'].value):
            if self.player[i].HasWon:
                counter += 1
                #print(str(counter))

        if counter == 1: #one player has won
            return 1
        elif counter == 0: #No one has won
            return 0
        return 2 #more than one player has won

    def AnnounceWinner(self):
        if self.settings['PlayerCount'].value > 0:
            for i in range(self.settings['PlayerCount'].value):
                if self.player[i].HasWon:
                    self.clear_window()
                    #self.update_word_connection_display()
                    self.victory_screen(i)
                    return
        #else:
            #print("You Win!!!!")
    def victory_screen(self, winning_player):
        self.clear_window()
        #print("updating to victory screen")
        word_connections_victory_title = Label(self.root, text = "Player " + str((winning_player + 1)) + " has won!!!", font = "Cambria 25 bold")
        word_connections_victory_title.grid(row = 0, column = 0, padx = 125, pady = 25, columnspan=3, sticky="ns")
        self.player = {}
        self.game_over = True
        
# endregion