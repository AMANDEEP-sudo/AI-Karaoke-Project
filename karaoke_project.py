from gtts import gTTS
from lyricsgenius import Genius
import yt_dlp
import os
import threading
import time
import pygame

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

# === GENERATE TTS FOR DUET PARTNER ===
print("Generating duet partner audio...")

tts_text = "Let's sing together! " + "\n".join(lyrics_lines[:4])  # First 4 lines

tts = gTTS(text=tts_text)
tts.save("partner.mp3")
print("Partner audio generated!")

# === PLAY AUDIO AND DISPLAY LYRICS ===
def display_lyrics(lyrics_lines):
    time.sleep(1)  # Small pause before starting lyrics
    for line in lyrics_lines:
        print(line.strip())
        time.sleep(2)  # Approximate timing between lines

print("Starting the karaoke session!")

# Initialize pygame mixer
pygame.mixer.init()

# Load audio
pygame.mixer.music.load("song.mp3")
partner_sound = pygame.mixer.Sound("partner.mp3")

# Play both sounds
pygame.mixer.music.play()
partner_sound.play()

# Start lyrics display in parallel
lyrics_thread = threading.Thread(target=display_lyrics, args=(lyrics_lines,))
lyrics_thread.start()

# Wait for music to finish
while pygame.mixer.music.get_busy():
    time.sleep(1)

lyrics_thread.join()

# === CLEANUP ===
pygame.mixer.quit()
os.remove("song.mp3")
os.remove("partner.mp3")
print("Done!")

# === Exit ===
input("Press Enter to exit...")
