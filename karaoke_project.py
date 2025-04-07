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

# === PLAY AUDIO AND DISPLAY LYRICS ===
def display_lyrics(lyrics_lines, song_duration):
    # Prepare user with countdown
    print("\nGet ready to sing!\n")
    for count in range(3, 0, -1):
        print(f"{count}...")
        time.sleep(1)
    print("🎤 Karaoke Mode 🎤\n")
    time.sleep(0.5)

    # Calculate line timing
    num_lines = len(lyrics_lines)
    line_duration = song_duration / num_lines if num_lines > 0 else 0

    for i, line in enumerate(lyrics_lines):
        # Clear screen (works on most OS)
        os.system('cls' if os.name == 'nt' else 'clear')

        # Add initial spacing for breathing room
        print("\n\n🎤 Karaoke Mode 🎤\n")

        # Display lyrics with current line highlighted
        for j, lyric_line in enumerate(lyrics_lines):
            if j == i:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + ">>> " + lyric_line.strip() + " <<<")
            else:
                print(Fore.YELLOW + lyric_line.strip())

        time.sleep(line_duration)

print("Starting the karaoke session!")

# Initialize pygame mixer
pygame.mixer.init()

# Load audio
pygame.mixer.music.load("song.mp3")

# Get audio duration
audio = MP3("song.mp3")
song_duration = audio.info.length

# Start lyrics display in parallel
lyrics_thread = threading.Thread(target=display_lyrics, args=(lyrics_lines, song_duration))
lyrics_thread.start()

# Play music
pygame.mixer.music.play()

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
