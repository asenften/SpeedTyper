"""
SpeedTyper - The Game!
Written by Avery

Release Version 1.0 (12/15/2023)
SpeedTyper is a simple typing game! Test your typing speed and accuracy by copying the prompts shown at the top of the screen
"""
from tkinter import *
from breezypythongui import EasyFrame
import pickle
import random

""" MAIN MENU
The MainMenu class is what I'm using to display the starting page of SpeedTyper. It contains two buttons: 'Play' and 'Highscore'.
The 'Play' button takes the user to the main gameplay loop, and the 'High Score' Button takes the user to a page that shows their highest saved score.
"""
class MainMenu(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=350, height=200, resizable=True)
        self.setBackground("#90C775")
        self.addLabel(text='S  P  E  E  D  T  Y  P  E  R', row=0, column=0, columnspan=4, font=("Lato Bold", 22),background='#9DD980',sticky="NSEW")    #Title
        self.addButton(text='Play', row=1, column=0,columnspan=2,sticky="NSEW",command=self.game_start)                                                 #Button that starts the game
        self.addButton(text='High Score',row=1,column=3,sticky="NSEW",command=self.go_scoreboard)                                                       #Button that opens the High Score screen
        

        
    def game_start(self):
        self.destroy()              #Destroy this screen...
        GameScreen().mainloop()     #...and open the Game Screen

    def go_scoreboard(self):
        self.destroy()              #Destroy this screen...
        HighScore().mainloop()      #...and open the High Score screen

""" HIGH SCORE
The HighScore class is what I'm using to display a page showcasing the users high score. It only contains one button: 'Main Menu'
The 'Main Menu' button simply returns the user back to the Main Menu.
"""
class HighScore(EasyFrame):
    def __init__(self):                                                     
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=550, height=200, resizable=False)
        self.setBackground("#90C775")

        f = open("highscore.obj","rb")  #Opening the highscore file... 
        highscore = str(pickle.load(f)) #...and saving its information to the variable 'highscore'
        f.close

        self.addLabel(text=f'Your highest saved score is:',row=0,column=0, font=("Lato", 25),background='#76A360',sticky="NSEW")
        self.addLabel(text=f'{highscore}',row=1,column=0, font=("Lato", 15),background='#76A360',sticky="NSEW")
        self.addButton(text='Main Menu', row=2, column=0, sticky="NSEW",command=self.go_Home)
    
    def go_Home(self):
        self.destroy()          #Destroy this screen...
        MainMenu().mainloop()   #...and return to the main menu

""" GAME SCREEN
The GameScreen class is what I'm using to display the main gameplay loop. It contains several objects that come together to create
the gameloop. After pressing start on the Main Menu, the user should begin typing to prompts shown at the top of the screen. If the user
wants to quit the game early, there is a 'Quit' button at the bottom right of the screen. 
"""
class GameScreen(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=800, height=200, resizable=False)
        self.setBackground("#90C775")

        #Instance variable declarations
        self.seconds_remaining = 60                 #Variable representing how many seconds the user has before the game ends
        self.charTotal = 0                          #Accumulative variable that stores the total number of characters the user types
        self.promptsTyped = 0                       #Accumulative variable that stores the total number of prompts the user has successfully completed
        self.sentence = self.get_sentences()        #Variable that represents obtaining a sentence from sentences.txt
        self.displayText = self.addLabel(text=self.sentence, row=0, column=0, font=("Lato Bold", 15), background='#76A360', sticky="NSEW")  #variable that acts as the sentence prompt
        self.entry_box = self.addTextField(text="", row=1, column=0, columnspan=1, rowspan=2, sticky='EW')     #This is the text field the user types in
        self.message = self.addLabel(text="", row=3, column=0, columnspan=1, font=("Lato", 13), background='#90C775', sticky="EW")  #Displays a status message to the user
        self.timer_label = self.addLabel(text=f"Time Remaining:{self.seconds_remaining} ",row=5,column=0,columnspan=1,font=("Lato", 16),background='#90C775',sticky="W")    #Label for the timer created in the method 'update_timer'
        self.gohome = self.addButton(text='Quit', row=5, column=0, sticky="E",command=self.go_home)    #Button that quits the game early and returns to the Main Menu.

        #Method declarations
        self.entry_box.focus_set()  #This line focuses the entry box upon opening the GameScreen window
        self.update_timer()         #Starts the timer
    
    def go_home(self):
        self.destroy()              #Destroy this screen...
        MainMenu().mainloop()       #...and return to the main menu

    def get_sentences(self):                                        
        file = open('sentences.txt', "r", encoding="utf-8")     #Open sentences.txt in utf-8 so it doesn't encode apostrophes weirdly...
        sentences = file.read().splitlines()                    #...and split each sentence by line
        file.close
        
        randomSentence = sentences[random.randint(0, 40)]   #Select a sentence from the sentences.txt at random
        #randomSentence = sentences[32]                     #Just an innocent little debug script :) (Do NOT look at line 33 in sentences.txt)
        self.randomSentence = randomSentence                #Variable that calls for a random sentence
        
        return str(self.randomSentence)  # returns the random sentence in question
    
    def check_input(self):
        #ALL self.message references update the text of self.message.
        if len(str(self.entry_box.getText())) >= len(str(self.randomSentence)): #(Progression: 1/7) If the length of both the text box and random sentence are equal...
            if str(self.entry_box.getText()) == str(self.randomSentence):       #(Progression: 2/7)...AND the text from both are the same...
                characters = self.randomSentence.split(" ")                     #(Progression: 3/7)...take the words from the random sentence...
                for characters in self.randomSentence:
                    self.charTotal += 1                                         #(Progression: 4/7)...and add them toward the word total.                                    
                self.message = self.addLabel(text="Great job!",row=3,column=0,columnspan=1,font=("Lato", 13),background='#90C775',sticky="EW")    
                self.promptsTyped += 1
                self.get_sentences()                                            #(Progression: 5/7) Now, grab a new sentence...       
                self.thisSentence = self.randomSentence                         #(Progression: 6/7)...and update the random sentence and label
                self.displayText = self.addLabel(text=self.thisSentence, row=0, column=0, font=("Lato Bold", 15), background='#76A360', sticky="NSEW")
                self.entry_box.setText("")                                      #(Progression: (7/7) Finally, clear the user's text entry box
            else:                                                               # . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #If the length of the typed sentence is correct, but the characters are not...
                self.message = self.addLabel(text="Something wasn't quite right, try again.", row=3, column=0, columnspan=1, font=("Lato", 13), sticky="EW")    #...inform the user they made a mistake...
                self.entry_box.setText("")        
                                                                                                                              #... and clear the entry box for the user so they can restart
            #///DEBUG ZONE///
            #If the sentences aren't the same even though the length is, print the text into the console so I can see why.
            #print("Prompt:", self.sentence)
            #print("TypedS:", self.entry_box.getText())
        else:
            self.message = self.addLabel(text="Type the sentence above!",row=3,column=0,columnspan=1,font=("Lato", 13),background='#90C775',sticky="EW")  #Default message to display.

    def update_timer(self):
            mins, secs = divmod(self.seconds_remaining, 60)             #Timer code
            timer_text = '{:02d}:{:02d}'.format(mins, secs)             #Timer format
            self.timer_label["text"] = f"Time Remaining: {timer_text}"  #Update the timer_label text
            self.after(1000, self.update_timer)                         #After one second, loop this method
                    
            if self.seconds_remaining == 0:     #Every 1000 milliseconds (1 second) we check if self.seconds_remaining is 0 (or less).
                self.destroy()                  #Once it's zero, destroy the current page...
                self.results_screen()           #And open the results screen
                
            else:
                self.seconds_remaining -= 1     #If the value of self.seconds_remaining is greater than 0, reduce it's value by one
                self.check_input()              #And check if the user typed the correct sentence.
                
                #///DEBUG ZONE/// Every second I can print the status of certian values
                #print("Text len:", len(str(self.entry_box.getText())))
                #print("Sentence len:", len(self.sentence))

            return timer_text       #returns the timer
    
    """ RESULTS SCREEN
    The 'results_screen' method - and the methods below it - act as their own screen that might LOOK separate 
    from the class 'GameScreen', but it's all part of one cohesive unit. It shows the user their score after
    the timer has run out and allows them to save the score, return to the main menu, or restart the game
    from the beginning.
    """
    def results_screen(self):     
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=800, height=300, resizable=False) 
        self.setBackground("#90C775")

        f = open("highscore.obj","rb")  #Open highscore.obj in read mode
        savedScore = pickle.load(f)     #And save the contents to the variable 'savedScore'
        f.close

        self.addLabel(text="Great job! Here are your results", row=0, column=0,columnspan=2, font=("Lato Bold", 25),background='#76A360',sticky="NSEW")             #Congratulatory message
        self.addLabel(text=f"Characters per second: {int(self.charTotal)/60}", row=1, column=0, columnspan=1, font=("Lato", 15),background='#9DD980', sticky="W")   #Characters per second score
        self.addLabel(text=f"Prompts completed: {self.promptsTyped}", row=2, column=0, columnspan=1, font=("Lato", 15),background='#9DD980', sticky="W")            #Prompts completed score
        self.currentScore = self.addLabel(text=f'Current High Score:\n{savedScore}',row=2,column=1,sticky="E",font=("Lato",10),background='#90C775')                #Display of the current saved score
        self.addButton(text='Save This Score',row=1, column=1,sticky="E",command=self.save_button)  # Save button (see 'save_Button' method)
        self.addButton(text='Main Menu', row=3, column=0, sticky="NSEW", command=self.menu_button)  # Main Menu button (see 'menu_Button' method)
        self.addButton(text='Restart', row=3, column=1, sticky="NSEW", command=self.restart_button) # Restart button (see 'restart_button' method)

    def save_button(self):
        f = open("highscore.obj","wb")      #Open highscore.obj...
        thisScore = f'Characters per second: {self.charTotal/60}\nPrompts completed: {self.promptsTyped}'   
        pickle.dump(thisScore,f)            #...and write the user's score to it    
        f.close

    def menu_button(self):
        self.destroy()          #Destroy the current page...
        MainMenu().mainloop()   #...and return to the main menu

    def restart_button(self):   
        self.destroy()          #Destroy the current page...
        GameScreen().mainloop() #...and restart the game loop from the beginning

def main():                     #Open the program starting at MainMenu()
    MainMenu().mainloop()

if __name__ == "__main__":
    main()
