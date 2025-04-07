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
    lyrics_lines = lyrics.split('\n')
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

# === SYNC LYRICS WITH AUDIO ===
def display_lyrics(lyrics_lines, duration):
    total_lines = len(lyrics_lines)
    interval = duration / total_lines

    # Add some space before lyrics for visual clarity
    print("\n🎤 Get ready to sing! 🎤")
    time.sleep(1)
    for countdown in range(3, 0, -1):
        print(f"Starting in {countdown}...")
        time.sleep(1)
    print("Let's go!\n")
    time.sleep(0.5)  # Tiny pause after countdown

    for line in lyrics_lines:
        print(f"\033[92m{line.strip()}\033[0m")  # Green text for highlight
        time.sleep(interval)

print("Starting the karaoke session!")

# Initialize pygame mixer
pygame.mixer.init()

# Load audio
pygame.mixer.music.load("song.mp3")

# Get audio duration
audio = MP3("song.mp3")
duration = audio.info.length

# Play music
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
