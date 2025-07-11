# YT-Long-to-Shorts-Agent

> Paste a YouTube link → get five ready-to-post 60-sec vertical shorts.

This project is an automated pipeline that takes a long-form YouTube video and generates multiple short-form vertical clips, complete with burned-in captions, ready for platforms like YouTube Shorts, TikTok, and Instagram Reels.

## The Problem

Content creators and marketing teams spend hours manually finding the best moments in long videos, clipping them, adding captions, and reformatting them for vertical platforms. This process is repetitive, time-consuming, and a bottleneck for content production.

## The Solution

This tool automates the entire workflow. By simply providing a YouTube URL, users get back five engaging, 60-second video clips, perfectly formatted and captioned. The goal is to reduce the end-to-end processing time for a 60-minute video to under 15 minutes with just two clicks.

## How It Works

The process is orchestrated by a Python agent that follows these steps:

1.  **Input**: User pastes a YouTube URL into a simple Streamlit web interface.
2.  **Download**: The high-quality video and its English transcript (`.vtt`) are downloaded using `yt-dlp`.
3.  **Segment Selection**: An AI model (GPT-4o) analyzes the transcript to identify the most engaging and coherent 60-second segments.
4.  **Video Splicing**: `moviepy` cuts the video at the selected timestamps.
5.  **Caption Generation**: The corresponding transcript text is styled and hard-burned onto the video clips using `ffmpeg`.
6.  **Export**: The final clips are exported as 1080x1920 MP4 files (9:16 aspect ratio).
7.  **Delivery**: Download links for the generated shorts are presented in the UI.

## Tech Stack

*   **UI**: [Streamlit](https://streamlit.io/)
*   **AI**: [OpenAI API](https://openai.com/docs) (GPT-4o) for content analysis
*   **Video Downloading**: `yt-dlp`
*   **Video Processing**: `moviepy`, `ffmpeg-python`
*   **Testing**: `pytest`

## Getting Started

### Prerequisites

*   Python 3.8+
*   FFmpeg installed on your system and available in your PATH.
    *   **macOS**: `brew install ffmpeg`
    *   **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
*   An OpenAI API Key.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/yt-long-to-shorts-agent.git
    cd yt-long-to-shorts-agent
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-..."
    ```

### Usage

Run the Streamlit application:

```bash
streamlit run src/ui.py
```

Open your browser to the local URL provided by Streamlit, paste a YouTube video link, and click "Generate".

## Project Roadmap

This project is being built in vertical slices to deliver end-to-end functionality quickly.

| Slice | Demo Goal                               | Status      |
|-------|-----------------------------------------|-------------|
| 1     | Download + raw clip list printed        | `In Progress` |
| 2     | Full cut & caption on single segment    | `Pending`   |
| 3     | 5-clip pipeline + tests pass            | `Pending`   |
| 4     | Streamlit UI + progress + downloads     | `Pending`   |

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.

Before submitting a PR, please ensure all tests pass:
```bash
pytest
```

---
*This README was generated based on the project's [PRD.md](PRD.md) and development notes.* 