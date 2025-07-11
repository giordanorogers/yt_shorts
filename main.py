import logging
import os
from src.download import download_video
from src.edit import cut_video
from src.caption import burn_captions_with_moviepy
from src.export import format_to_vertical
from src.select import select_best_segments

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main function to run the video processing pipeline.
    """
    # --- Configuration ---
    YOUTUBE_URL = "" # ENTER THE URL TO THE YOUTUBE VIDEO HERE!!!
    NUM_CLIPS = 5
    CLIP_DURATION = 60

    DOWNLOADS_DIR = "downloads"
    OUTPUT_DIR = "output"
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Pipeline ---
    
    # 1. Download Video and Subtitles
    logging.info("--- Step 1: Downloading Video ---")
    video_path, vtt_path = download_video(YOUTUBE_URL, DOWNLOADS_DIR)
    if not video_path or not vtt_path:
        logging.error("Failed to download video or subtitles. Exiting.")
        return
    logging.info(f"Video downloaded to: {video_path}")
    logging.info(f"Subtitles downloaded to: {vtt_path}")

    with open(vtt_path, 'r', encoding='utf-8') as f:
        vtt_content = f.read()

    # 2. Select Best Segments
    logging.info("\n--- Step 2: Selecting Best Segments ---")
    segments = select_best_segments(vtt_content, NUM_CLIPS, CLIP_DURATION)
    if not segments:
        logging.error("No segments were selected. Exiting.")
        return
    logging.info(f"Selected {len(segments)} segments.")

    # 3. Process Each Segment
    logging.info("\n--- Step 3: Processing Each Segment ---")
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    
    for i, segment in enumerate(segments):
        start_time = segment["start"]
        end_time = segment["end"]
        logging.info(f"\n--- Processing clip {i+1}/{len(segments)} ({start_time} - {end_time}) ---")

        # Define file paths for this segment
        raw_clip_path = os.path.join(OUTPUT_DIR, f"{base_name}_clip_{i+1}_raw.mp4")
        captioned_clip_path = os.path.join(OUTPUT_DIR, f"{base_name}_clip_{i+1}_captioned.mp4")
        final_clip_path = os.path.join(OUTPUT_DIR, f"{base_name}_clip_{i+1}_final.mp4")

        # Cut, Caption, and Format
        cut_clip = cut_video(video_path, raw_clip_path, start_time, end_time)
        if not cut_clip:
            logging.error(f"Failed to cut clip {i+1}. Skipping.")
            continue

        captioned_clip = burn_captions_with_moviepy(cut_clip, vtt_content, captioned_clip_path)
        if not captioned_clip:
            logging.error(f"Failed to burn captions for clip {i+1}. Skipping.")
            continue
        
        final_clip = format_to_vertical(captioned_clip, final_clip_path)
        if not final_clip:
            logging.error(f"Failed to format clip {i+1}. Skipping.")
            continue
            
        logging.info(f"✅ Finished processing clip {i+1}. Final video at: {final_clip}")
    
    logging.info("\n--- All Clips Processed ---")

if __name__ == "__main__":
    main()
