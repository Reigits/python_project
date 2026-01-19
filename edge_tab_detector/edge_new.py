import time
import customtkinter as customtk
import threading
import pygetwindow as gw
import numpy as np
import sounddevice as sd

fs = 44100  # sample rate

def tone(freq:int, duration:float, volume:float=0.15):
    t = np.linspace(0, duration, int(fs * duration), False)
    return volume * np.sign(np.sin(2 * np.pi * freq * t))  # 8-bit square wave

sound = np.concatenate([
    tone(659, 0.08),   # E5
    tone(784, 0.08),   # G5
    tone(988, 0.08),   # B5
    tone(1319, 0.24),  # E6 (GO!)
])

def tone2(freq:int=260, duration:float=0.06, volume:float=0.22):
    t = np.linspace(0, duration, int(fs * duration), False)
    return volume * np.sin(2 * np.pi * freq * t)

sound2 = np.concatenate([
    tone2(),
    np.zeros(int(fs * 0.04)),   # tiny gap
    tone2(freq=320)  # slight pitch change = attention
])


print("Starting Edge Detector...")
class EdgeDetector:
    def __init__(self, root:customtk.CTk) -> None:

        # X and Y Speed and Dimension
        self.x_speed:int = 3
        self.y_speed:int = 3

        # Phase
        self.phase:str= 'green'

        #Yellow Animation
        self.green_anim_string:str = '|/-\\'
        self.index_string:int = 0

        # Known Tab
        self.known_tab:set[str]= set()

        # Timer
        self.timer:int = 5

        # Window
        self.window:customtk.CTk = root
        self.window.geometry('400x150')
        self.window.attributes('-topmost', True)
        self.window.resizable(False, False)
        self.window.title('Edge Tab Detector')

        # String Variable
        self.text_variable:customtk.StringVar = customtk.StringVar(
                value="Microsoft Edge Not Detected"
                )

        # Label
        self.label:customtk.CTkLabel = customtk.CTkLabel(
                master = self.window,
                textvariable= self.text_variable,
                font=("Terminess Nerd Font Mono", 21, "bold"),
                text_color='black'
                )
        self.thread_mode_monitor_tab() 
        self.dvd_anim()
        self.pack_widget()

    def dvd_anim(self):
        x_position:int = self.window.winfo_x()
        y_position:int = self.window.winfo_y()
        next_x:int = self.x_speed + x_position
        next_y:int = self.y_speed + y_position
        if (next_x + 416) >= 1920:
            self.x_speed = -self.x_speed
        elif next_x <= 0:
            self.x_speed = -self.x_speed
        if (next_y + 189) >= 1080:
            self.y_speed = -self.y_speed
        elif next_y <= 0:
            self.y_speed = -self.y_speed
        self.window.geometry(f'400x150+{next_x}+{next_y}')
        self.window.after(10, self.dvd_anim)

    def pack_widget(self)->None:
        self.label.place(
                relx=0.5,
                rely=0.5,
                anchor='center'
                )
    def thread_mode_monitor_tab(self)->None:
        threading.Thread(
                target=self.monitor_edge_tabs,
                daemon=True
                ).start()

    def thread_mode_warning(self):
        threading.Thread(
                target=self.red_warning_mode,
                daemon=True).start()

    def monitor_edge_tabs(self):
        while True:
            active_tab:list[str] = [w for w in gw.getAllTitles() if "Edge" in w]
            print(active_tab)
            for window in active_tab:
                if 'New tab' in window:
                    continue
                if 'Edge Tab Detector' in window:
                    continue
                if 'Untitled' in window:
                    continue
                if 'bing.com' in window:
                    continue
                if window not in self.known_tab and self.phase=='green':
                    self.phase = 'red'
                    self.thread_mode_warning()
                    self.known_tab.add(window)
            time.sleep(1)

    def red_warning_mode(self)->None: 
        self.phase = 'red'
        self.window.configure(fg_color = '#FF3131')
        while self.timer > 0: 
            sd.play(sound2, fs)
            self.text_variable.set(f'Do Not Continue!: {self.timer} Second')
            time.sleep(1)
            self.timer -= 1
        self.yellow_warning_mode()
        time.sleep(0.5)
        self.green_warning_mode()
        self.timer = 5

    def yellow_warning_mode(self):
        self.phase = 'yellow'
        self.window.configure(fg_color = '#FFD700')
        self.text_variable.set('Almost Done!')
        sd.play(sound, fs)

    def green_warning_mode(self)->None:
        self.phase = 'green'
        self.green_mode_anim()
        self.window.configure(fg_color = '#7CFC00')

    def green_mode_anim(self):
        if self.phase != 'green':
            return
        else:
            self.text_variable.set(self.green_anim_string[self.index_string]+' No New Tab Detected '+self.green_anim_string[self.index_string]) 
            self.index_string += 1
            if self.index_string > 3:
                self.index_string = 0 
            self.window.after(100, self.green_mode_anim)

    def run_app(self)->None:
        self.window.mainloop()

if __name__ == "__main__":
    edge = EdgeDetector(customtk.CTk())
    edge.run_app()
    print('Process exited with code 0')
