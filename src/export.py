import logging
import ffmpeg
import os

logger = logging.getLogger(__name__)

def format_to_vertical(video_path: str, output_path: str) -> str | None:
    """
    Formats a video to a 9:16 aspect ratio.

    It crops the video to the center and resizes it to 1080x1920.

    Args:
        video_path: The path to the input video.
        output_path: The path to save the formatted video.

    Returns:
        The path to the formatted video, or None if an error occurred.
    """

    try:
        logger.info(f"Formatting video to 9:16 aspect ratio: {video_path}")
        
        # Get video properties
        probe = ffmpeg.probe(video_path)
        video_stream = next((s for s in probe['streams'] if s['codec_type'] == 'video'), None)
        
        if not video_stream:
            logger.error("No video stream found in the input file.")
            return None
            
        width = int(video_stream['width'])
        height = int(video_stream['height'])
        
        # Calculate cropping dimensions
        target_aspect = 9.0 / 16.0
        current_aspect = float(width) / height
        
        if current_aspect > target_aspect:
            # Video is wider than target, crop width
            new_width = int(height * target_aspect)
            new_height = height
            x_offset = (width - new_width) // 2
            y_offset = 0
        else:
            # Video is taller than target, crop height
            new_width = width
            new_height = int(width / target_aspect)
            x_offset = 0
            y_offset = (height - new_height) // 2
            
        input_stream = ffmpeg.input(video_path)
        
        # Crop and resize video stream
        processed_video = (
            input_stream.video
            .filter('crop', new_width, new_height, x_offset, y_offset)
            .filter('scale', 1080, 1920)
        )
        
        # Take the audio from the input stream
        input_audio = input_stream.audio

        # Setup output stream
        stream = ffmpeg.output(processed_video, input_audio, output_path, vcodec='libx264', acodec='aac')
        ffmpeg.run(stream, overwrite_output=True, quiet=True)
        
        logger.info(f"Successfully formatted video to {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Failed to format video to vertical: {e}", exc_info=True)
        return None
