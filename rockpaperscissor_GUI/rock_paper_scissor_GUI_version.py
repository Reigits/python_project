from random import choice as ch
from tkinter import *

class rockpaperscissor:
    def __init__(self):

        #Game Variable
        self.player_action:str= 'nothing'
        self.bot_action:str= 'nothing'
        self.botaction()
        self.player_wins:int= 0
        self.bot_wins:int= 0

        #The Main Window
        self.window:Tk = Tk()
        self.window.geometry('350x380')
        self.window.resizable(False,False)
        self.window.attributes('-topmost', True)

        #Frame
        self.button_frame:Frame = Frame(self.window)
        self.frame_for_image_frame:Frame = Frame(self.window)

        #Pictures
        self.images_for_game()


        #Game Dictionary
        self.dict_game:dict[str, str]= {'rock':'scissor', 'paper':'rock', 'scissor':'paper'}
        self.dict_image_player:dict[str, PhotoImage] = {'rock':self.image_player_rock, 'paper':self.image_player_paper, 'scissor': self.image_player_scissor}
        self.dict_image_bot:dict[str, PhotoImage]= {'rock':self.image_bot_rock, 'paper':self.image_bot_paper, 'scissor': self.image_bot_scissor}        

        #Buttons and Labels
        self.labels_and_buttons()

        #Initialize Window
        self.window.mainloop()

    def images_for_game(self):
        self.image_player_rock:PhotoImage= PhotoImage(file="2Rock-paper-scissors_(rock).png")
        self.image_player_paper:PhotoImage= PhotoImage(file="2Rock-paper-scissors_(paper).png") 
        self.image_player_scissor:PhotoImage = PhotoImage(file="2Rock-paper-scissors_(scissors).png")
        self.image_bot_rock:PhotoImage = PhotoImage(file="mirrored2Rock-paper-scissors_(rock).png")
        self.image_bot_paper:PhotoImage = PhotoImage(file="mirrored2Rock-paper-scissors_(paper).png")
        self.image_bot_scissor:PhotoImage = PhotoImage(file="mirrored2Rock-paper-scissors_(scissors).png")
        self.blank_image:PhotoImage = PhotoImage(width=155, height=155)

    def labels_and_buttons(self):

        #Labels, Buttons and Grids
        self.window.title("Rock Paper Scissor")
        main_label = Label(text='Choose your power!', pady= 20, font=('Arial', 20))
        rock_button = Button(master= self.button_frame, text='Rock', command=lambda:self.checkbattle('rock'))
        paper_button = Button(master= self.button_frame, text='Paper', command=lambda:self.checkbattle('paper'))
        scissor_button = Button(master= self.button_frame, text='Scissor', command=lambda:self.checkbattle('scissor'))
        self.player_win_label:Label = Label(text=f'Player Wins = {self.player_wins}')
        self.bot_win_label:Label= Label(text=f'Bot Wins = {self.bot_wins}')
        self.win_lose_label_var:StringVar= StringVar()
        self.win_lose_label:Label= Label(textvariable=self.win_lose_label_var)
        player_action_label = Label(master=self.frame_for_image_frame, text='Player Action:')
        bot_action_label = Label(master=self.frame_for_image_frame, text='Bot Action:')
        rock_button.grid(row = 1, column = 1, padx = 10)
        paper_button.grid(row = 1, column = 3, padx = 10)
        scissor_button.grid(row =1 , column = 5, padx = 10)
        self.show_image_player:Label= Label(master=self.frame_for_image_frame, image=self.blank_image)
        self.show_image_bot:Label= Label(master=self.frame_for_image_frame, image=self.blank_image)

        #Packing All Widgets
        main_label.pack()
        self.player_win_label.pack()
        self.bot_win_label.pack(pady = 10)
        self.button_frame.pack()
        self.win_lose_label.pack(pady= 15)
        self.frame_for_image_frame.pack(fill='x')
        player_action_label.grid(row = 0,column = 1)
        bot_action_label.grid(row = 0, column = 2)
        self.show_image_player.grid(row = 1,column = 1)
        self.show_image_bot.grid(row = 1,column = 2, padx = 32)

    def checkbattle(self, choice:str): #To Calculate the Battle
        
        #Game Logic
        self.player_action = choice
        if self.player_action == self.bot_action:
            self.win_lose_label_var.set('Tie!')
        elif self.dict_game[self.player_action] == self.bot_action:
            self.player_wins += 1
            self.win_lose_label_var.set('You Win!')
            self.player_win_label.config(text=f'Player Wins = {self.player_wins}')
        else:
            self.win_lose_label_var.set('You Lose!')
            self.bot_wins += 1
            self.bot_win_label.config(text=f'Bot Wins = {self.bot_wins}')
        
        #Show Images of The Action
        self.show_image_player.config(image=self.dict_image_player[choice])
        self.show_image_bot.config(image=self.dict_image_bot[self.bot_action])
        self.show_image_player.grid(row = 1, column=1)
        self.show_image_bot.grid(row = 1, column=2)
        self.botaction()
        self.window.after(1000, self.hide_images)

    def botaction(self): #Determine the Bot Action
        self.bot_action = ch(['rock', 'paper', 'scissor'])

    def hide_images(self): #Hide Images After 1 Second
        self.show_image_player.config(image=self.blank_image)
        self.show_image_bot.config(image=self.blank_image)

gametime= rockpaperscissor()
