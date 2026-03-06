import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import OPENAI_API_KEY, MODEL_NAME
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, MODEL_NAME

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name=MODEL_NAME
)

def validate_requirements(extracted):

    prompt = f"""
    Review the extracted requirements.

    Tasks:
    - Remove duplicate information
    - Improve clarity
    - Identify missing requirements
    - Ensure professional business language

    Data:
    {extracted}
    """

    response = llm.invoke(prompt)

    return response.content
