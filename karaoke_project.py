from lyricsgenius import Genius
import yt_dlp
import os
import threading
import time
import pygame
from mutagen.mp3 import MP3
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

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
    lyrics_lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
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

# === GET AUDIO LENGTH ===
audio = MP3("song.mp3")
audio_length = audio.info.length

# === HIGHLIGHT FUNCTION ===
def print_highlighted_lyrics(lyrics_lines, audio_length):
    total_lines = len(lyrics_lines)
    delay_per_line = audio_length / total_lines

    # Give user time to prepare
    print("\nGet ready to sing!\n")
    time.sleep(3)

    # Force clear before first line
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n🎤 Karaoke Mode 🎤\n")

    for idx, line in enumerate(lyrics_lines):
        if idx != 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("🎤 Karaoke Mode 🎤\n")

        for i, l in enumerate(lyrics_lines):
            if i == idx:
                print(Fore.GREEN + Style.BRIGHT + f">>> {l.upper()} <<<" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + Style.NORMAL + l)
        time.sleep(delay_per_line)

# === PLAY AUDIO AND DISPLAY LYRICS ===
print("Starting the karaoke session!")

# Initialize pygame mixer
pygame.mixer.init()

# Load and play audio
pygame.mixer.music.load("song.mp3")
pygame.mixer.music.play()

# Start lyrics display in parallel
lyrics_thread = threading.Thread(target=print_highlighted_lyrics, args=(lyrics_lines, audio_length))
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
