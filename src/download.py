import logging
import os
import yt_dlp

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("logs/app.log"),
                        logging.StreamHandler()
                    ])

def download_video(url: str, output_path: str = "downloads") -> tuple[str | None, str | None]:
    """
    Downloads a YouTube video and its English subtitles using yt-dlp.

    Args:
        url: The YouTube URL to download.
        output_path: The directory to save the downloaded files.

    Returns:
        A tuple containing the path to the video file and the subtitle file,
        or (None, None) if the download fails.
    """
    video_path = None
    subtitle_path = None

    def hook(d):
        nonlocal subtitle_path
        if d['status'] == 'finished':
            # The hook is great for subtitles, but less reliable for the final
            # video path when merging is involved. We'll capture subtitles here
            # and determine the video path after the download completes.
            if d['info_dict'].get('ext') == 'vtt':
                subtitle_path = d['filename']
                logging.info(f"Subtitle file available at: {subtitle_path}")

    ydl_opts = {
        'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/mp4',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'subtitlesformat': 'vtt',
        'progress_hooks': [hook],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.info(f"Starting download for URL: {url}")
            # We need to extract info before downloading to get the expected title
            info = ydl.extract_info(url, download=False)
            # Construct the expected final path for the merged mp4
            video_path = ydl.prepare_filename(info).replace(info['ext'], ydl_opts['merge_output_format'])

            ydl.download([url])

        # The hook should have set the subtitle path. We can add a fallback just in case.
        if subtitle_path and not os.path.exists(subtitle_path):
            base_name = os.path.splitext(video_path)[0]
            expected_sub_path = f"{base_name}.en.vtt"
            if os.path.exists(expected_sub_path):
                subtitle_path = expected_sub_path
                logging.info(f"Used fallback to find subtitle path: {subtitle_path}")
            else:
                subtitle_path = None # Could not find it

        logging.info(f"Download finished. Video: {video_path}, Subtitles: {subtitle_path}")
        return video_path, subtitle_path

    except Exception as e:
        logging.error(f"Failed to download video from {url}: {e}")
        return None, None
