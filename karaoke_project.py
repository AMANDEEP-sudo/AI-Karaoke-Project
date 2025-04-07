import os
import threading
import time
import pygame
import yt_dlp
from lyricsgenius import Genius
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

# === DISPLAY LYRICS FUNCTION ===
def display_lyrics(lyrics_lines, pre_delay=3.0, line_delay=2.0):
    # Preparation countdown
    print("\n🎤 Get ready to sing! 🎤\n")
    for countdown in range(3, 0, -1):
        print(f"Starting in {countdown}...")
        time.sleep(1)
    print("Let's go!\n")
    time.sleep(pre_delay)  # Extra wait for sync

    # Display lyrics line by line
    for line in lyrics_lines:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        print(f"\033[92m{line}\033[0m")  # Green highlight
        time.sleep(line_delay)

print("Starting the karaoke session!")

# Initialize pygame mixer
pygame.mixer.init()

# Load and play audio
pygame.mixer.music.load("song.mp3")
audio = MP3("song.mp3")
duration = audio.info.length

# Start music
pygame.mixer.music.play()

# Start lyrics display thread
# Adjust `pre_delay` and `line_delay` as needed for better sync!
lyrics_thread = threading.Thread(target=display_lyrics, args=(lyrics_lines, 3.0, 2.0))
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
