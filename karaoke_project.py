from gtts import gTTS
from lyricsgenius import Genius
from playsound import playsound
import yt_dlp
import os
import threading
import time

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

# === PLAY BOTH AUDIO FILES TOGETHER ===
def play_audio(file_path):
    playsound(file_path)

def display_lyrics(lyrics_lines):
    time.sleep(1)  # Small pause before starting lyrics
    for line in lyrics_lines:
        print(line.strip())
        time.sleep(2)  # Approximate timing between lines (adjust if needed)

print("Playing the karaoke duet!")

karaoke_thread = threading.Thread(target=play_audio, args=("song.mp3",))
partner_thread = threading.Thread(target=play_audio, args=("partner.mp3",))
lyrics_thread = threading.Thread(target=display_lyrics, args=(lyrics_lines,))

karaoke_thread.start()
partner_thread.start()
lyrics_thread.start()

karaoke_thread.join()
partner_thread.join()
lyrics_thread.join()

# === CLEANUP ===
os.remove("song.mp3")
os.remove("partner.mp3")
print("Done!")

# === Exit ===
input("Press Enter to exit...")
