import logging
from moviepy.editor import VideoFileClip
import os

# Configure logging
logger = logging.getLogger(__name__)

def _time_to_seconds(time_str: str) -> float:
    """Converts a HH:MM:SS or MM:SS string to seconds."""
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return int(m) * 60 + float(s)
    else:
        raise ValueError("Invalid time format. Please use HH:MM:SS or MM:SS.")

def cut_video(input_path: str, output_path: str, start_time: str, end_time: str) -> str | None:
    """
    Cuts a video segment from a source file using moviepy.

    Args:
        input_path: Path to the source video file.
        output_path: Path to save the new video clip.
        start_time: The start time of the clip in "HH:MM:SS" or "MM:SS" format.
        end_time: The end time of the clip in "HH:MM:SS" or "MM:SS" format.

    Returns:
        The path to the created clip, or None if an error occurred.
    """
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return None

    try:
        start_seconds = _time_to_seconds(start_time)
        end_seconds = _time_to_seconds(end_time)

        logger.info(f"Cutting video from {start_time} to {end_time}...")
        
        # Create a sub-directory for clips if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with VideoFileClip(input_path) as video:
            sub_clip = video.subclip(start_seconds, end_seconds)
            sub_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger=None)
        
        logger.info(f"Successfully created clip: {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Failed to cut video: {e}")
        return None
