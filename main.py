import logging
from src.download import download_video

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the video processing pipeline.
    Slice 1: Download video and print hard-coded clip list.
    """
    # 1. Download video
    # Using a video that is known to have subtitles for testing
    video_url = "https://www.youtube.com/watch?v=vRQs7qfIDaU"
    logging.info(f"Starting pipeline for video: {video_url}")

    video_path, subtitle_path = download_video(video_url)

    if not video_path or not subtitle_path:
        logging.error("Pipeline failed: Could not download video or subtitles.")
        return

    logging.info(f"Video downloaded to: {video_path}")
    logging.info(f"Subtitles downloaded to: {subtitle_path}")

    # 2. Select segments (Slice 1: hard-coded)
    logging.info("Clip selection (using hard-coded timestamps for Slice 1):")
    
    hardcoded_clips = [
        {"start_time": "00:02:30", "end_time": "00:03:30", "title": "Clip 1: The Core Idea"},
        {"start_time": "00:05:15", "end_time": "00:06:15", "title": "Clip 2: Key Insight"},
        {"start_time": "00:10:45", "end_time": "00:11:45", "title": "Clip 3: A Practical Example"},
        {"start_time": "00:15:00", "end_time": "00:16:00", "title": "Clip 4: Future Implications"},
        {"start_time": "00:20:20", "end_time": "00:21:20", "title": "Clip 5: Conclusion"}
    ]

    for clip in hardcoded_clips:
        logging.info(f"  - Found clip: {clip['title']} ({clip['start_time']} - {clip['end_time']})")
    
    logging.info("Slice 1 complete: Video downloaded and raw clip list generated.")


if __name__ == "__main__":
    main()
