# 🎤 AI Karaoke Project

An interactive, console-based karaoke experience powered by Python. This project fetches lyrics using the Genius API and downloads karaoke tracks from YouTube using `yt-dlp`. It then displays real-time lyric highlighting in sync with the music, offering a fun and engaging solo karaoke experience.

---

## 📌 Features

- 🔍 Automatic lyrics fetching using Genius API
- 🎵 Karaoke track download from YouTube via `yt-dlp`
- ⏱️ Time-synced lyrics based on song duration
- 🎨 Real-time lyric highlighting (current line: bright green, others: yellow)
- 📼 Console clearing for a clean karaoke-style experience
- 💻 Cross-platform compatible (Windows/Linux/Mac)

---

## 🧠 AI Component

This project demonstrates a **basic level of AI integration** through:
- **Intelligent lyric parsing** using NLP-like filtering to clean up non-singing parts like `[Chorus]`, `[Verse]`, etc.
- **Synchronized timing logic**, where lyric display is mapped proportionally across the total audio duration.
- While no deep learning model is used, the real-time behavior mimics human timing and enhances interactivity using simple automation and logic.

---

## 🚀 Technologies Used

- **Python** 🐍
- [LyricsGenius](https://github.com/johnwmillr/LyricsGenius)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **mutagen** (for getting MP3 duration)
- **pygame** (for audio playback)
- Standard Libraries: `os`, `time`, `threading`

---

## 🛆 Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/YourUsername/ai-karaoke-project
   cd ai-karaoke-project
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧪 How to Run

```bash
python karaoke.py
```

1. Enter the song name.
2. Sit back as the system downloads lyrics and audio.
3. Sing along with the highlighted lyrics!

---

## ⚠️ Notes

- Internet connection required (for lyrics and YouTube download)
- Avoid using special characters in song names
- Console must support ANSI escape codes (most modern terminals do)

---

## ✅ Conclusion

This project showcases how Python can be used creatively to blend media processing, simple automation, and interactive design. It’s a great demonstration of AI principles in real-time systems.

---

## 👨‍💻 Author

**Saptaparno Chakraborty**  
BTech CSE Student | Full Stack Dev | Indie Game Dev Enthusiast
