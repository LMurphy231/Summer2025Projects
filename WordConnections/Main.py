import numpy as np
from word_connections_data import wc

NumOfPlayers = 1
NumOfWords = 2


    

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
    NewId = np.random.randint(0,len(wc[CurrentIndex].connection))
    NextWord = wc[CurrentIndex].connection[NewId]
    print("Next word is " + NextWord)
    return FindNameIndex(NextWord)



def GetWordList():
    
    WordList = []
    WordList.append(wc[np.random.randint(0,len(wc))].name)
    CurrentIdList = []
    CurrentIdList.append(FindNameIndex(WordList[0]))
    
    for i in range(1,NumOfWords):
        ChooseWord = True #If Word still needs to be chosen
        while ChooseWord:
            NewId = np.random.randint(0,len(wc[CurrentIdList[i-1]].connection)) #randomly choose after word
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
    
    print("Curent Word To guess:")
    print(''.join(Player[PlayerNum].HiddenCharList[Player[PlayerNum].CurrentIndex]))
    
    UserInput = str(input("Enter: "))
    return CheckUserGuess(UserInput, PlayerNum)



def CheckUserGuess(UserInput, PlayerNum):
    if UserInput.lower() == Player[PlayerNum].WordList[Player[PlayerNum].CurrentIndex].lower(): #User correct
        print("That is correct!!")
        return True
    else:
        print("Sorry that is incorrect ") #User incorrect
        return False
    

    1
def SetupPlayers(NumOfPlayers):
    #Limit number of players
    

    print("Number of players: " + str(NumOfPlayers))

    for i in range(NumOfPlayers):
        #print("Setting up player " + str(i))
        WordList, IndexList = GetWordList()
        WordCharList, HiddenCharList = GetCharList(WordList)
        Player.append(PlayerStats(WordList, IndexList, 1, WordCharList, HiddenCharList, 1, False))
        #PrintPlayerStats(i)
    return

def ResetPlayers(NumOfPlayers):
    print("More than one player has won at the same time, resetting players until a single player has won")
    
    
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
    
    print("Player " + str(PlayerNum + 1) + " is up!") #Introduce player
    print()
    
    #Print current shown list
    for i in range(NumOfWords):
        print(''.join(Player[PlayerNum].HiddenCharList[i]))
    print()

    #Get User guess and check if it is correct
    if GetUserGuess(PlayerNum):
        #print("Current Index = " + str(Player[PlayerNum].CurrentIndex))
        Player[PlayerNum].HiddenCharList[Player[PlayerNum].CurrentIndex] = Player[PlayerNum].CharList[Player[PlayerNum].CurrentIndex]
        #print(''.join(Player[PlayerNum].HiddenCharList[Player[PlayerNum].CurrentIndex]))
        print()
        Player[PlayerNum].CurrentChar = 1 #Reset current char to first letter
        Player[PlayerNum].CurrentIndex += 1 #Incriminte word counter by 1

        #If player exceeds number of words announce they have finished
        if Player[PlayerNum].CurrentIndex >= NumOfWords:
            print("Player " + str(PlayerNum + 1) + " has finished their list!")
            Player[PlayerNum].HasWon = True
            return False
        
        return True


    else: 
        if Player[PlayerNum].CurrentIndex >= NumOfWords:
            return False
        print()
        UpdateCharList(Player[PlayerNum].CurrentIndex,PlayerNum)
        return False
      

def CheckPlayerVictories(NumOfPlayers):
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
        for i in range(NumOfPlayers + 1):
            if Player[i].HasWon:
                print("Player " + str(i + 1) + " has won!!!!")
                return
    else:
        print("You Win!!!!")




def main():
    while True:
        try:
            NumOfPlayers = int(input("Enter Number of Players (MAX 4): "))
            break
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4!!!")

    if NumOfPlayers > 4:
        NumOfPlayers = 4
    elif NumOfPlayers < 1:
        NumOfPlayers = 1 
       
              
    SetupPlayers(NumOfPlayers)
    GetWordList()
    InGame = True
    while InGame:
        print()
        if NumOfPlayers > 1:
            for i in range(NumOfPlayers):
                
                while True:
                    if not Turn(i):
                        break

            if CheckPlayerVictories(NumOfPlayers) == 2:
                print("Reseting Players")
                InGame = True
                ResetPlayers(NumOfPlayers)
            elif CheckPlayerVictories(NumOfPlayers) == 1:
                InGame = False
                break

        else: 
            print("SinglePlayer")
            while True:
                Turn(0)
                if  Player[0].CurrentIndex >= NumOfWords:
                    InGame = False
                    break
    AnnounceWinner()
    print("GAME OVER!!")

            

   
    
    
    
    

   
    
    
    

    
if __name__ == "__main__":
    main()  