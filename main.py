"""
SpeedTyper - The Game!
Written by Avery

Release Version 1.0
This program is a simple typing game. It has a main menu with two buttons: Start and History. 'Start' will begin The Game, and 'History'
shows you your most recent score. Within the game, there are two parts. The typing phase, and the results phase. In the typing part, the
user should type the prompt on the screen as quickly and accurately as they can. Once the user successfully types the sentence, it will
load a new sentence and log the information needed for the results phase.
"""

from breezypythongui import EasyFrame
import random
import pickle

class MainMenu(EasyFrame):      #Start page
    def __init__(self):
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=350, height=200, resizable=False)
        self.setBackground("#90C775")
        self.addLabel(text='Press Play to Begin!', row=0, column=0, columnspan=2, font=("Lato Bold", 16),background='#9DD980',sticky="NSEW")
        self.addButton(text='Play', row=1, column=0, sticky="NSEW", command=self.game_start)
        self.addButton(text='History', row=1, column=1, sticky="NSEW",command=self.goLeaderboard)

    def game_start(self):
        self.destroy()
        GameScreen().mainloop()

    def goLeaderboard(self):
        self.destroy()
        RecentScore().mainloop()

class RecentScore(EasyFrame):       #This used to be for your highscore but I decided I didn't want to deal with that :)
    def __init__(self):
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=550, height=200, resizable=False)
        self.setBackground("#90C775")

        h = open("highscore.obj","rb")      #Open the "highscore" file
        highscore = str(pickle.load(h)) 
        h.close
        self.addLabel(text=f'Your most recent score was:',row=0,column=0, font=("Lato", 25),background='#76A360',sticky="NSEW")
        self.addLabel(text=f'{highscore}',row=1,column=0, font=("Lato", 15),background='#76A360',sticky="NSEW")
        self.addButton(text='Main menu', row=2, column=0, sticky="NSEW",command=self.goHome)
    
    def goHome(self):
        self.destroy()
        MainMenu().mainloop()

class GameScreen(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=800, height=200, resizable=False)
        self.setBackground("#90C775")

        #Instance variable declarations
        self.charTotal = 0
        self.promptsTyped = 0
        self.sentence = self.get_sentences()
        self.seconds_remaining = 60
        self.displayText = self.addLabel(text=self.sentence, row=0, column=0, font=("Lato Bold", 15), background='#76A360', sticky="NSEW")
        self.message = self.addLabel(text="", row=3, column=0, columnspan=1, font=("Lato", 13), background='#90C775', sticky="EW")  #Displays an updating message to the user
        self.entry_box = self.addTextField(text="", row=1, column=0, columnspan=1, rowspan=2, sticky='EW')
        self.timer_label = self.addLabel(text=f"Time Remaining:{self.seconds_remaining} ",row=5,column=0,columnspan=1,font=("Lato", 16),background='#90C775',sticky="W")

        #Method declarations
        self.entry_box.focus_set()  #This line focuses the entry box upon opening the GameScreen window
        self.update_timer()
        self.check_input()

    def get_sentences(self):
        file = open('sentences.txt', "r", encoding="utf-8")
        sentences = file.read().splitlines()
        file.close
        
        randomSentence = sentences[random.randint(0, 40)] # choose a sentence from the list at random
        #randomSentence = sentences[32] #Just an innocent little debug script :) (Do NOT look at line 33 in sentences.txt)
        self.randomSentence = randomSentence
        
        return str(self.randomSentence)  # returns the random sentence in question
    

    def check_input(self):
        #All self.message references are made to update the text of self.message.
        if len(str(self.entry_box.getText())) >= len(str(self.randomSentence)): #(Progression: 1/7) If the length of both the text box and random sentence are equal...
            if str(self.entry_box.getText()) == str(self.randomSentence):       #(Progression: 2/7)...AND the text from both are the same...
                characters = self.randomSentence.split(" ")                     #(Progression: 3/7)...take the words from the random sentence...
                for characters in self.randomSentence:
                    self.charTotal += 1                                         #(Progression: 4/7)...and add them toward the word total.                                    
                self.message = self.addLabel(text="Great job!",row=3,column=0,columnspan=1,font=("Lato", 13),background='#90C775',sticky="EW")    
                self.promptsTyped += 1
                self.get_sentences()                                            #(Progression: 5/7) Now, grab a new sentence...       
                self.thisSentence = self.randomSentence                         #(Progression: 6/7)...and update the random sentence and label.
                self.displayText = self.addLabel(text=self.thisSentence, row=0, column=0, font=("Lato Bold", 15), background='#76A360', sticky="NSEW")
                self.entry_box.setText("")                                      #(Progression: (7/7) Finally, clear the entry box text.
            else:
                self.message = self.addLabel(text="Something wasn't quite right, try again.", row=3, column=0, columnspan=1, font=("Lato", 13), sticky="EW")
                self.entry_box.setText("")          #Clear the entry box for the user so they can restart.
            

            #///DEBUG ZONE///
            #If the sentences aren't the same even though the length is, print the text into the console so I can see why
            #print("PS:", self.sentence)
            #print("TS:", self.entry_box.getText())
        else:
            self.message = self.addLabel(text="Type the sentence above!",row=3,column=0,columnspan=1,font=("Lato", 13),background='#90C775',sticky="EW")  #This message is what displays in most instances

    def update_timer(self):
            mins, secs = divmod(self.seconds_remaining, 60)             #Timer code
            timer_text = '{:02d}:{:02d}'.format(mins, secs)             #Timer format
            self.timer_label["text"] = f"Time Remaining: {timer_text}"  #Update the timer_label text
            self.after(1000, self.update_timer)                         #After one second, loop this method
                    
            if self.seconds_remaining == 0:     #Every 1000 milliseconds (1 second) we check if self.seconds_remaining is 0 (or less).
                self.destroy()                  #Once it's zero, destroy the current page...
                self.resultsPage()                                #And create the results page
                
            else:
                self.seconds_remaining -= 1     #If the value of self.seconds_remaining is greater than 0, reduce it's value by one
                self.check_input()              #And check if the user typed the correct sentence.
                
                #///DEBUG ZONE/// Every second I can print the status of certian values
                #print("Text len:", len(str(self.entry_box.getText())))
                #print("Sentence len:", len(self.sentence))

            return timer_text       #returns the timer

    def resultsPage(self): 
        EasyFrame.__init__(self, title="SpeedTyper - The Game!", width=800, height=300, resizable=False) 
        self.setBackground("#90C775")
        self.addLabel(text="Great job! Here are your results", row=0, column=0,columnspan=2, font=("Lato Bold", 25),background='#76A360',sticky="NSEW")
        self.addLabel(text=f"Characters per second: {int(self.charTotal)/60}", row=1, column=0, columnspan=1, font=("Lato", 15),background='#9DD980', sticky="W")
        self.addLabel(text=f"Prompts completed: {self.promptsTyped}", row=2, column=0, columnspan=1, font=("Lato", 15),background='#9DD980', sticky="W")
        self.addButton(text='Main Menu', row=3, column=0, sticky="NSEW", command=self.menu_Button)
        self.addButton(text='Restart', row=3, column=1, sticky="NSEW", command=self.restart_Button)

        f = open("highscore.obj","wb")      #Create/Open and write to a file 'highscore.obj'
        previousScore = f'Characters per second: {self.charTotal/60}\nPrompts completed: {self.promptsTyped}'
        pickle.dump(previousScore,f)        
        f.close

    def menu_Button(self):      #Return to menu button
        self.destroy()
        MainMenu().mainloop()

    def restart_Button(self):   #Restart the game button
        self.destroy()
        GameScreen().mainloop()

def main():                     #Start the program at MainMenu()
    MainMenu().mainloop()

if __name__ == "__main__":
    main()
