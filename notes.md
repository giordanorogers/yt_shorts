# Proposed Next Steps

Start with a tiny, end-to-end “walking skeleton” that proves the most brittle external dependency—​YouTube downloading—​works on your machine and in CI. Concretely:

1. Project scaffold (½ day)
   • Create a clean virtual-env / Poetry project  
   • Add `requirements.txt` with yt_dlp, moviepy, ffmpeg-python, openai, streamlit, pytest, python-dotenv  
   • Commit `.gitignore`, `logging.ini`, CI stub (GitHub Actions macOS + Ubuntu matrix that just installs deps and runs `pytest -q`).

2. Slice #1 deliverable (1 day) – “Download + raw clip list printed”
   a. `download.py`  
      – Function `download_video(url: str, out_dir: Path) -> Path`  
      – Use yt_dlp to fetch the highest-quality video + English `.vtt`; save under `downloads/{video_id}/`.  
      – Log progress at INFO to `logs/app.log`.

   b. Basic transcript parsing  
      – Convert `.vtt` to a plain‐text list of `(start, end, text)` tuples.  
      – For now simply print the first *N* time-blocks to prove the pipeline can read the transcript.

   c. CLI entry point (Click or plain `argparse`)  
      `python -m yt_shorts.download "https://youtu.be/…"` → prints the first 10 caption blocks.

3. Tests (¼ day)
   • Unit test that “given a short sample video URL, `download_video` returns an MP4 and VTT under the expected folder”.  
   • Mark it `@pytest.mark.slow` and gate it behind an env var so CI can skip or run on demand.

4. CI green (¼ day)
   • Make the GitHub Action call `brew install ffmpeg` on macOS runner and `apt-get install ffmpeg` on Ubuntu, then run the test.  
   • Artifact-upload the downloaded sample video so you can inspect failures.

Why this first?  
• Validates network downloads, ffmpeg availability, file-path conventions, and logging plumbing—​all areas most likely to bite later.  
• Gives you a concrete artifact (an MP4 + captions on disk) that teammates can inspect, building confidence.  
• Sets up the structure where subsequent slices (segment selection, splicing, caption burn, UI) plug in as additional modules rather than re-architecting.

Once slice #1 is stable, move to slice #2 (“cut & caption on single segment”) with the comfort that downloads are already locked down.