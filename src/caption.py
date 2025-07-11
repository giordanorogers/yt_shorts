import logging
from moviepy.editor import VideoFileClip, CompositeVideoClip, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
import webvtt
from io import StringIO

logger = logging.getLogger(__name__)

def burn_captions_with_moviepy(video_path: str, vtt_content: str, output_path: str) -> str | None:
    """
    Burns VTT captions into a video file using MoviePy's SubtitlesClip.
    This version includes robust VTT parsing to avoid errors with malformed files.
    """
    try:
        logger.info(f"Starting to burn captions into {video_path} with MoviePy's SubtitlesClip...")

        video_clip = VideoFileClip(video_path)

        # Manually parse the VTT content for robustness
        vtt_file = StringIO(vtt_content)
        captions = webvtt.read_buffer(vtt_file)
        
        subtitles_data = []
        for caption in captions:
            start = caption.start_in_seconds
            end = caption.end_in_seconds
            text = caption.text.replace('\\n', '\n').strip()
            # The parser might create empty text captions, which we can ignore
            if text:
                subtitles_data.append(((start, end), text))

        # Define a generator for the TextClips
        generator = lambda txt: TextClip(
            txt,
            font='Arial-Bold',
            fontsize=48,
            color='white',
            bg_color='black',
            method='caption',
            size=(video_clip.w * 0.8, None),
        )

        # Create the subtitles clip from the parsed data
        subtitles = SubtitlesClip(subtitles_data, generator)

        # Overlay the subtitles on the video
        final_clip = CompositeVideoClip([video_clip, subtitles.set_position(('center', 'bottom'))])
        
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", logger="bar")
        
        video_clip.close()
        final_clip.close()

        logger.info(f"Successfully burned captions into {output_path}")
        return output_path

    except Exception as e:
        logger.error(f"Failed to burn captions with MoviePy: {e}", exc_info=True)
        return None
