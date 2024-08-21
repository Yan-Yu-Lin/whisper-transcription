import os
import shutil
from openai import OpenAI
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define folder paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_VIDEO = os.path.join(PROJECT_DIR, "Processing_Video")
PROCESSED_VIDEO = os.path.join(PROJECT_DIR, "Processed_Video")
RESULT_TEXT = os.path.join(PROJECT_DIR, "Result_Text")
RESULT_ARCHIVE = os.path.join(PROJECT_DIR, "Result_Archive")

def create_folders():
    """Create necessary folders if they don't exist."""
    for folder in [PROCESSING_VIDEO, PROCESSED_VIDEO, RESULT_TEXT, RESULT_ARCHIVE]:
        os.makedirs(folder, exist_ok=True)

def extract_audio(video_path):
    """Extract audio from video file."""
    video = VideoFileClip(video_path)
    audio_path = video_path.rsplit(".", 1)[0] + ".mp3"
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    """Transcribe audio using OpenAI Whisper API."""
    with open(audio_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text

def process_videos():
    """Process all videos in the Processing_Video folder."""
    for video_file in os.listdir(PROCESSING_VIDEO):
        if video_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(PROCESSING_VIDEO, video_file)
            
            # Extract audio
            audio_path = extract_audio(video_path)
            
            # Transcribe audio
            transcription = transcribe_audio(audio_path)
            
            # Save transcription
            text_file = os.path.join(RESULT_TEXT, f"{os.path.splitext(video_file)[0]}.txt")
            with open(text_file, "w", encoding="utf-8") as f:
                f.write(transcription)
            
            # Move video to Processed_Video folder
            shutil.move(video_path, os.path.join(PROCESSED_VIDEO, video_file))
            
            # Remove temporary audio file
            os.remove(audio_path)

def archive_previous_results():
    """Move previous results to the archive folder."""
    for file in os.listdir(RESULT_TEXT):
        shutil.move(os.path.join(RESULT_TEXT, file), os.path.join(RESULT_ARCHIVE, file))

def main():
    create_folders()
    archive_previous_results()
    process_videos()

if __name__ == "__main__":
    main()
