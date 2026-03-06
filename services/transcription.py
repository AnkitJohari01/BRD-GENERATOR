import whisper
import tempfile
import os

# Load model once
model = whisper.load_model("base")

def transcribe_audio(file):

    # get file extension (.mp4, .mp3, .wav etc)
    file_extension = os.path.splitext(file.name)[1]

    # create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_audio:
        temp_audio.write(file.read())   # FIX: Streamlit uses file.read()
        temp_path = temp_audio.name

    # run whisper
    result = model.transcribe(temp_path)

    return result["text"]
