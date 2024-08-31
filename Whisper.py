import os
import shutil
from openai import OpenAI
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
from pydub import AudioSegment


# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define folder paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_MEDIA = os.path.join(PROJECT_DIR, "Processing_Media")
PROCESSED_MEDIA = os.path.join(PROJECT_DIR, "Processed_Media")
RESULT_TEXT = os.path.join(PROJECT_DIR, "Result_Text")
RESULT_ARCHIVE = os.path.join(PROJECT_DIR, "Result_Archive")
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes


def create_folders():
    """Create necessary folders if they don't exist."""
    for folder in [PROCESSING_MEDIA, PROCESSED_MEDIA, RESULT_TEXT, RESULT_ARCHIVE]:
        os.makedirs(folder, exist_ok=True)

def extract_audio(media_path):
    """Extract audio from video file or return path if already audio."""
    audio_extensions = ('.mp3', '.m4a', '.wav', '.aac', '.ogg')
    if media_path.lower().endswith(audio_extensions):
        return media_path
    video = VideoFileClip(media_path)
    audio_path = media_path.rsplit(".", 1)[0] + ".mp3"
    video.audio.write_audiofile(audio_path)
    return audio_path

def split_audio(audio_path):
    """Split audio file into chunks of 25 MB or less."""
    audio = AudioSegment.from_mp3(audio_path)
    duration = len(audio)
    chunk_duration = int((MAX_FILE_SIZE / os.path.getsize(audio_path)) * duration)
    
    chunks = []
    for i in range(0, duration, chunk_duration):
        chunk = audio[i:i+chunk_duration]
        chunk_path = f"{audio_path[:-4]}_chunk_{i//chunk_duration}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    
    return chunks

def transcribe_audio(audio_path):
    """Transcribe audio using OpenAI Whisper API, splitting if necessary."""
    if os.path.getsize(audio_path) > MAX_FILE_SIZE:
        chunks = split_audio(audio_path)
        transcriptions = []
        for chunk in chunks:
            with open(chunk, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            transcriptions.append(transcription.text)
            os.remove(chunk)  # Remove the temporary chunk file
        return " ".join(transcriptions)
    else:
        with open(audio_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text


def process_media():
    """Process all media files in the Processing_Media folder."""
    for media_file in os.listdir(PROCESSING_MEDIA):
        if media_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.mp3', '.m4a')):
            media_path = os.path.join(PROCESSING_MEDIA, media_file)
            print(f"path_way:{media_path}")
            
            # Extract audio or use MP3 directly
            audio_path = extract_audio(media_path)
            print(audio_path)
            
            # Transcribe audio
            transcription = transcribe_audio(audio_path)
            print(transcription)
            
            # Save transcription
            text_file = os.path.join(RESULT_TEXT, f"{os.path.splitext(media_file)[0]}.txt")
            with open(text_file, "w", encoding="utf-8") as f:
                f.write(transcription)
            
            # Move media to Processed_Media folder
            shutil.move(media_path, os.path.join(PROCESSED_MEDIA, media_file))
            
            # Remove temporary audio file if it was created
            if audio_path != media_path:
                os.remove(audio_path)

def archive_previous_results():
    """Move previous results to the archive folder."""
    for file in os.listdir(RESULT_TEXT):
        shutil.move(os.path.join(RESULT_TEXT, file), os.path.join(RESULT_ARCHIVE, file))

def main():
    create_folders()
    archive_previous_results()
    process_media()

if __name__ == "__main__":
    main()
