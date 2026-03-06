import pytesseract
from PIL import Image
import io


def read_image(file):

    image = Image.open(io.BytesIO(file.file.read()))

    text = pytesseract.image_to_string(image)

    return text