from json import *
from tkinter import *
from random import choice

class window:
    def __init__(self):
        self.window = Tk()
        self.button_frame = Frame(master=self.window)
        self.window.title('Flash Card')
        self.window.geometry('500x500')
        self.window.configure(bg='#F5F5F5')
        try:
            with open('save_file.json', 'r') as maindata:
                self.data = load(maindata)
        except FileNotFoundError:
            self.data = {}
            self.initial_request()
        if self.data:
            self.flash_card_label_list = choice(list(self.data.keys()))
        else:
            self.flash_card_label_list = 'No Cards!'

        #Widgets
        self.widgets_initialization()

        #Window Initialization
        self.window.mainloop()
    
    def widgets_initialization(self):

        #StringVars
        self.flash_card_label_var = StringVar()
        self.flash_card_answer_var = StringVar()

        #Widgets
        self.guide_label = Label(master=self.window, text='Press the cards to see the answer!')
        self.flash_card_label = Button(master=self.window, textvariable=self.flash_card_label_var, relief='ridge', borderwidth=10,command=self.flip_card, bg="#C24B3E", font=('Arial', 15), wraplength=250)
        self.load_button = Button(master=self.button_frame, text='Load New Cards', command=self.load_data_button_function)
        self.refresh_button = Button(master=self.button_frame, text='Refresh Cards', command=self.refresh_card)
        self.is_flipped = True

        #Packing Widget

        self.guide_label.pack(pady=20)
        self.flash_card_label.pack(expand=True, fill=BOTH, padx=20)
        self.button_frame.pack(pady=30)
        self.load_button.grid(row=1,column=1)
        self.refresh_button.grid(row=1,column=2, padx= 20)
        self.flash_card_label_var.set(self.flash_card_label_list)

    def initial_request(self):
        self.request_window = Toplevel(master=self.window)
        self.request_window.geometry('250x250')
        self.request_window.attributes('-topmost', True)
        card_entry_request_frame = Frame(master=self.request_window)
        answer_entry_request_frame = Frame(master=self.request_window)
        request_label = Label(master=self.request_window, text='Please put it in your\ninitial question and answer!', pady=20)
        card_entry_label = Label(master=card_entry_request_frame, text='Card:')
        answer_entry_label = Label(master=answer_entry_request_frame, text='Answer:')
        self.request_entry_card = Entry(master=card_entry_request_frame)
        self.request_entry_answer = Entry(master=answer_entry_request_frame)
        self.request_button = Button(master=self.request_window, text='Load into program!', command=self.load_file_request)

        request_label.pack()
        card_entry_request_frame.pack()
        answer_entry_request_frame.pack(pady=20)
        card_entry_label.pack()
        answer_entry_label.pack()
        self.request_entry_card.pack()
        self.request_entry_answer.pack()
        self.request_button.pack(pady=10)

    def load_data_button_function(self):

        #Label. Button Initialization
        self.load_window = Toplevel(self.window)
        self.load_window.title('Load New Cards')
        self.load_window.geometry('250x250')
        self.entry_cards_frame = Frame(master=self.load_window)
        self.entry_answers_frame = Frame(master=self.load_window)
        self.load_label = Label(master=self.load_window, text='Enter your cards and answers!')
        self.entry_cards_label = Label(master=self.entry_cards_frame, text='Card Title:')
        self.entry_cards = Entry(master=self.entry_cards_frame, text='Cards')
        self.entry_answers_label = Label(master=self.entry_answers_frame, text='Card Answer:')
        self.entry_answers = Entry(master=self.entry_answers_frame, text='Answer')
        self.load_button_therealone = Button(master=self.entry_answers_frame, text='Load into program!', command=self.load_file)
        
        #Packing Widget
        self.load_label.pack(pady=20)
        self.entry_cards_frame.pack()
        self.entry_cards_label.pack()
        self.entry_cards.pack()
        self.entry_answers_frame.pack(pady=20)
        self.entry_answers_label.pack()
        self.entry_answers.pack()
        self.load_button_therealone.pack(pady=20)
        
    def load_file(self):

        #Load Logic
        cards_key = self.entry_cards.get()
        answers_value = self.entry_answers.get()
        try:
            with open('save_file.json', 'r') as readfile:
                self.datanew = load(readfile)
        except FileNotFoundError:
            self.datanew = {}

        self.datanew[cards_key] = answers_value
        with open('save_file.json', 'w') as mainfile:
            dump(self.datanew, mainfile, indent=5)
        self.data = self.datanew

    def flip_card(self):

        #The Flip Card Logic
        if self.is_flipped:
            self.flash_card_label_var.set(self.data[self.flash_card_label_list])
            self.flash_card_label['bg'] = "#50DA57"
            self.is_flipped = False
        else:
            self.flash_card_label_var.set(self.flash_card_label_list)
            self.flash_card_label['bg'] = '#C24B3E'
            self.is_flipped = True

    def refresh_card(self):

        #Change The Card
        self.flash_card_label_list= choice(list(self.data.keys()))
        self.flash_card_label_var.set(self.flash_card_label_list)
        self.flash_card_label['bg'] = '#C24B3E'
        self.is_flipped = True

    def load_file_request(self):

        #Load Logic
        cards_key = self.request_entry_card.get()
        answers_value = self.request_entry_answer.get()
        self.data[cards_key] = answers_value
        with open('save_file.json', 'w') as mainfile:
            dump(self.data, mainfile, indent=5)
        self.flash_card_label_list = choice(list(self.data.keys()))
        self.request_window.destroy()

flash_card = window()
