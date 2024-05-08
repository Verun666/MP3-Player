import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer

# Define a class for the MP3 player.
class Player(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack()

        # Initialize the Pygame mixer for playing audio.
        mixer.init()

        # Load playlist from file if it exists, otherwise initialize an empty list.
        if os.path.exists("songs.pickle"):
            with open("songs.pickle", "rb") as f:
                self.playlist = pickle.load(f)
        else:
            self.playlist = []

        # Initialize variables for current song index, playback state, and whether a song has been played.
        self.current = 0
        self.paused = True
        self.played = False

        # Create GUI frames and widgets.
        self.create_frames()
        self.track_widgets()
        self.control_widgets()
        self.tracklist_widgets()
        

    # Function to create GUI frames.
    def create_frames(self):
        # Frame for displaying track information.
        self.track = tk.LabelFrame(self, text="Track",
                                   font=("Comic Sans MS",14,"bold"),
                                   bg="#329dcb", fg="white",bd=5,relief=tk.GROOVE)
        self.track.configure(width=410, height=300)
        self.track.grid(row=0, column=0, padx=10)

        # Frame for displaying playlist.
        self.tracklist = tk.LabelFrame(self, text=f"Playlist - {str(len(self.playlist))}",
                                       font=("Comic Sans MS",14,"bold"),
                                       bg="#329dcb", fg="white",bd=5,relief=tk.GROOVE)
        self.tracklist.configure(width=190, height=400)
        self.tracklist.grid(row=0, column=1,rowspan=3, pady=5)

        # Frame for playback controls.
        self.controls = tk.LabelFrame(self, text="Track",
                                      font=("Comic Sans MS",14,"bold"),
                                      bg="#329dcb", fg="white",bd=2,relief=tk.GROOVE)
        self.controls.configure(width=410, height=80)
        self.controls.grid(row=2, column=0, pady=5, padx= 10)

    # Function to create track information widgets.
    def track_widgets(self):
        # Canvas for displaying album art.
        self.canvas = tk.Label(self.track, image=img)
        self.canvas.configure(width=400, height=240)
        self.canvas.grid(row=0, column=0)

        # Label for displaying song track information.
        self.songtrack = tk.Label(self.track, font=("Comic Sans MS",14,"bold"),
                                  bg= "#329dcb", fg="white")
        self.songtrack["text"] = "Veromusic MP3 Player"
        self.songtrack.configure(width=30, height=1)
        self.songtrack.grid(row=1, column=0, padx=10)

    # Function to create playback control widgets.
    def control_widgets(self):
        # Button to load songs from a directory.
        self.load_songs = tk.Button(self.controls, bg= "#329dcb", fg="white", font=("Comic Sans MS",14,"bold"))
        self.load_songs["text"] = "Load Songs"
        self.load_songs["command"]  = self.retrieve_songs
        self.load_songs.grid(row=0, column=0, padx=10)

        # Button for previous song.
        self.prev = tk.Button(self.controls, image=prev, bg="#329dcb")
        self.prev["command"]  = self.prev_song
        self.prev.grid(row=0, column=1)

        # Button for pause/resume.
        self.pause = tk.Button(self.controls, image=pause, bg="#329dcb")
        self.pause["command"]  = self.pause_song
        self.pause.grid(row=0, column=2)

        # Button for next song.
        self.next = tk.Button(self.controls, image= next, bg="#329dcb")
        self.next["command"]  = self.next_song
        self.next.grid(row=0, column=3)

        # Volume slider.
        self.volume = tk.DoubleVar(self)
        self.slider = tk.Scale(self.controls, from_=0, to=10, orient=tk.HORIZONTAL)
        self.slider["variable"] = self.volume
        self.slider.set(7)
        mixer.music.set_volume(0.7)
        self.slider["command"]  = self.change_volume
        self.slider.grid(row=0, column=4, padx=5)

    # Function to create playlist widgets.
    def tracklist_widgets(self):
        self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, rowspan=5, sticky="ns")

        self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,
                               yscrollcommand=self.scrollbar.set, selectbackground="#64d2ed")
        self.enumerate_songs()
        self.list.config(height=22)
        self.list.bind("<Double-1>", self.play_song)
        self.scrollbar.config(command=self.list.yview)
        self.list.grid(row=0, column=0, rowspan=5)

    # Function to enumerate and display songs in the playlist.
    def enumerate_songs(self):
        for index, song in enumerate(self.playlist):
            self.list.insert(index, os.path.basename(song))

    # Function to retrieve songs from a directory.
    def retrieve_songs(self):
        self.songlist = []
        directory = filedialog.askdirectory()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file)[1] == ".mp3":
                    path = (root + "/" + file).replace("\\","/")
                    self.songlist.append(path)

        with open("songs.pickle", "wb") as f:
            pickle.dump(self.songlist, f)

        self.playlist = self.songlist
        self.tracklist["text"] = f"Playlist - {str(len(self.playlist))}"
        self.list.delete(0, tk.END)
        self.enumerate_songs()

    # Function to play a song.
    def play_song(self, event=None):
        if event is not None:
            self.current = self.list.curselection()[0]
            for i in range(len(self.playlist)):
                self.list.itemconfigure(i, bg="#93e0f2")

        mixer.music.load(self.playlist[self.current])

        self.pause["image"] = play
        self.paused = False
        self.played = True
        self.songtrack["anchor"] = "w"
        self.songtrack["text"] = os.path.basename(self.playlist[self.current])
        self.list.activate(self.current)
        self.list.itemconfigure(self.current, bg="#64d2ed")
        mixer.music.play()

    # Function to pause/resume a song.
    def pause_song(self):
        if not self.paused:
            self.paused = True
            mixer.music.pause()
            self.pause["image"] = pause
        else:
            if self.played == False:
                self.play_song()
            self.paused = False
            mixer.music.unpause()
            self.pause["image"] = play

    # Function to play the previous song.
    def prev_song(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = 0
        self.list.itemconfigure(self.current + 1, bg="#64d2ed")
        self.play_song()

    # Function to play the next song.
    def next_song(self):
        if self.current < len(self.playlist) - 1:
            self.current += 1
        else:
            self.current = 0
            self.play_song()
        self.list.itemconfigure(self.current - 1, bg="#64d2ed")
        self.play_song()

    # Function to change the volume.
    def change_volume(self, event=None):
        self.v = self.volume.get()
        mixer.music.set_volume(self.v / 10)

# Create the main Tkinter window.
screen = tk.Tk()
screen.geometry('640x420')
screen.wm_title('Vero MP3 Player')

# Load images for GUI buttons.
img = PhotoImage(file="images/music.png")
next = PhotoImage(file="images/next.png")
prev = PhotoImage(file="images/previous.png")
pause = PhotoImage(file="images/pause.png")
play = PhotoImage(file="images/play.png")

# Create and run the MP3 player application.
app = Player(master=screen)
app.mainloop()
