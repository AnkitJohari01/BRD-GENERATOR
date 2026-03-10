# import whisper
# import tempfile
# import os

# # Load model once
# model = whisper.load_model("base")

# def transcribe_audio(file):

#     # get file extension (.mp4, .mp3, .wav etc)
#     file_extension = os.path.splitext(file.name)[1]

#     # create temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio:
#         temp_audio.write(file.read())   # FIX: Streamlit uses file.read()
#         temp_path = temp_audio.name

#     # run whisper
#     result = model.transcribe(temp_path)

#     return result["text"]


















import whisper
import tempfile
import os
import subprocess

# Load whisper model once
model = whisper.load_model("base")


def extract_audio_from_video(video_path, audio_path):
    """
    Extract audio from video using ffmpeg
    """
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-vn",
        "-acodec",
        "mp3",
        audio_path,
        "-y"
    ]

    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def transcribe_audio(file):

    file_ext = os.path.splitext(file.name)[1].lower()

    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        temp_file.write(file.read())
        input_path = temp_file.name

    audio_path = input_path

    # If video → extract audio
    if file_ext in [".mp4", ".mov", ".mkv"]:
        audio_path = input_path + ".mp3"
        extract_audio_from_video(input_path, audio_path)

    # Whisper transcription
    result = model.transcribe(audio_path)

    # Cleanup
    try:
        os.remove(input_path)
    except:
        pass

    if audio_path != input_path:
        try:
            os.remove(audio_path)
        except:
            pass

    return result["text"]
