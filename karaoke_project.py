from lyricsgenius import Genius
import yt_dlp
import os
import threading
import time
import pygame
from mutagen.mp3 import MP3

# === SETUP ===
GENIUS_API_TOKEN = "Ck5Q6uo_T8LYrAKw8l8e7i1jhqLox4l-9zrb1cd4oUvuWUkP_d2fPFv_hhwjv2m-"  # <-- your token
genius = Genius(GENIUS_API_TOKEN)

# === USER INPUT ===
song_name = input("Enter the song name: ")

# === FETCH LYRICS ===
song = genius.search_song(song_name)
if song:
    print("\nLyrics found!\n")
    lyrics = song.lyrics
    lyrics_lines = [line.strip() for line in song.lyrics.split('\n') if line.strip()]
else:
    print("Lyrics not found.")
    exit()

# === DOWNLOAD AUDIO FROM YOUTUBE USING yt-dlp ===
print("Downloading audio from YouTube...")

def download_audio(search_query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': 'song.%(ext)s',
        'quiet': False,
        'default_search': 'ytsearch',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([search_query + " karaoke"])

download_audio(song_name)
print("Audio downloaded!")

# === GET SONG DURATION ===
audio = MP3("song.mp3")
duration = audio.info.length

# === DISPLAY LYRICS SYNCHRONIZED WITH HIGHLIGHT ===
def display_lyrics(lyrics_lines, duration):
    time.sleep(1)  # Small pause before starting lyrics
    time_per_line = duration / len(lyrics_lines) if lyrics_lines else 0

    for index, line in enumerate(lyrics_lines):
        # Clear screen before printing
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print all lyrics with current line highlighted
        for i, l in enumerate(lyrics_lines):
            if i == index:
                print(f"\033[93m{l}\033[0m")  # Yellow highlight
            else:
                print(l)
        
        time.sleep(time_per_line)

print("Starting the karaoke session!")

# Initialize pygame mixer
pygame.mixer.init()

# Load audio
pygame.mixer.music.load("song.mp3")

# Start music playback
pygame.mixer.music.play()

# Start lyrics display in parallel
lyrics_thread = threading.Thread(target=display_lyrics, args=(lyrics_lines, duration))
lyrics_thread.start()

# Wait for music to finish
while pygame.mixer.music.get_busy():
    time.sleep(1)

lyrics_thread.join()

# === CLEANUP ===
pygame.mixer.quit()
os.remove("song.mp3")
print("Done!")

# === Exit ===
input("Press Enter to exit...")
