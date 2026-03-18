import time
import customtkinter as customtk
import threading
import pygetwindow as gw
import numpy as np
import sounddevice as sd
import pyautogui as auto
import random

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
        
        # Window List
        self.active_tab:list[str] = [w for w in gw.getAllTitles() if "Edge" in w]

        # Placeholder String
        self.string_search:list[str] = [
    "trigger", "action", "event", "workflow", "process", "task", "job", "script", "bot", "agent",
    "pipeline", "schedule", "cron", "queue", "worker", "function", "handler", "listener", "webhook", "api",
    "endpoint", "request", "response", "payload", "input", "output", "parameter", "variable", "condition", "logic",
    "rule", "filter", "router", "branch", "loop", "iterate", "retry", "timeout", "delay", "interval",
    "polling", "sync", "async", "callback", "promise", "thread", "daemon", "service", "microservice", "container",
    "virtualenv", "dependency", "package", "module", "library", "framework", "integration", "deployment", "build", "release",
    "version", "commit", "repository", "triggered", "monitor", "logging", "alert", "notification", "observer", "scheduler",
    "executor", "orchestrator", "controller", "manager", "configuration", "environment", "variable", "secret", "token", "credential",
    "authentication", "authorization", "encryption", "validation", "parser", "serializer", "transform", "mapping", "adapter", "connector",
    "bridge", "middleware", "gateway", "proxy", "cache", "database", "storage", "backup", "restore", "scaling"
]

        # X and Y Speed and Dimension
        self.x_speed:int = 3
        self.y_speed:int = 3

        # Phase
        self.phase:str= 'green'
        self.search_phase:bool = False

        #Yellow Animation and Auto-Search Animation
        self.green_anim_string:str = '|/-\\'
        self.index_string:int = 0
        self.dot_anim:str = '...'
        self.dot_anim_index:int = 0

        # Known Tab
        self.known_tab:set[str]= set()

        # Timer
        self.timer_search:int = 5
        self.timer:int = 5

        # Window
        self.window:customtk.CTk = root
        self.window.geometry('400x200')
        self.window.attributes('-topmost', True)
        self.window.resizable(False, False)
        self.window.title('Auto-Bingo')

        # String Variable
        self.text_variable:customtk.StringVar = customtk.StringVar(
                value="Microsoft Edge Not Detected"
                )
        self.text_variable_autosearch:customtk.StringVar = customtk.StringVar(
                value='Auto-Searching: Off'
                )

        # Label
        self.label:customtk.CTkLabel = customtk.CTkLabel(
                master = self.window,
                textvariable= self.text_variable,
                font=("Terminess Nerd Font Mono", 21, "bold"),
                text_color='black'
                )

        self.search_label:customtk.CTkLabel = customtk.CTkLabel(
                master=self.window,
                textvariable=self.text_variable_autosearch,
                font=("Terminess Nerd Font Mono", 15, 'bold'),
                text_color='black'
                )

        #Button
        self.autosearch_button:customtk.CTkButton = customtk.CTkButton(
                master=self.window,
                text='Start Search',
                command=self.thread_mode_search,
                font=("Terminess Nerd Font Mono",15, 'bold'),
                fg_color='#327ba8'
                )

        self.thread_mode_monitor_tab()
        self.pack_widget()

    def self_search(self):
        if not self.active_tab:
            self.text_variable_autosearch.set('Microsoft Edge not Detected!')
            time.sleep(2)
            self.text_variable_autosearch.set('Auto-Searching: Off')
            return
        else:
            list_of_keyword = self.string_search.copy()
            self.search_phase = True
            self.autosearch_button.configure(state='disabled', fg_color='grey')
            self.timer_search = 5
            while self.timer_search > 0:
                self.text_variable_autosearch.set(f'Auto-Searching in: {self.timer_search} Seconds')
                time.sleep(1)
                self.timer_search -= 1
            self.auto_search_anim()
            for i in range(1,31):
                random_keyword = random.choice(list_of_keyword)
                print(list_of_keyword)
                auto.click()
                time.sleep(random.randint(500, 700)/1000)
                auto.hotkey('ctrl', 'a')
                time.sleep(random.randint(500, 700)/1000)
                auto.hotkey('backspace')
                time.sleep(random.randint(500, 700)/1000)
                auto.typewrite(random_keyword, interval=random.randint(500,700)/1000)
                time.sleep(random.randint(500, 700)/1000)
                auto.hotkey('enter')
                time.sleep(random.randint(500, 950)/100)
                list_of_keyword.remove(random_keyword)
            self.search_phase = False
            self.text_variable_autosearch.set("Auto-Searching Finished")
            time.sleep(2)
            self.text_variable_autosearch.set('Auto Search: Off')
            self.autosearch_button.configure(state='enabled', fg_color='#327ba8')

    def monitor_edge_tabs(self):
        while True:
            self.active_tab:list[str] = [w for w in gw.getAllTitles() if "Edge" in w]
            for window in self.active_tab:
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

    def thread_mode_search(self):
        threading.Thread(
                target=self.self_search,
                daemon=True).start()

    def thread_mode_monitor_tab(self)->None:
        threading.Thread(
                target=self.monitor_edge_tabs,
                daemon=True
                ).start()

    def thread_mode_warning(self):
        threading.Thread(
                target=self.red_warning_mode,
                daemon=True).start()

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

    def auto_search_anim(self):
        if not self.search_phase:
            return
        else:
            self.text_variable_autosearch.set('Auto-Searching on Progress' + self.dot_anim[0:self.dot_anim_index])
            self.dot_anim_index += 1
            if self.dot_anim_index > 3:
                self.dot_anim_index = 0
            self.window.after(100, self.auto_search_anim)

    def pack_widget(self)->None:
        self.label.pack(
                pady=30
                )

        self.autosearch_button.pack(
                pady=10
                )

        self.search_label.pack(
                pady=5
                )

    def run_app(self)->None:
        self.window.mainloop()

if __name__ == "__main__":
    edge = EdgeDetector(customtk.CTk())
    edge.run_app()
    print('Process exited with code 0')
