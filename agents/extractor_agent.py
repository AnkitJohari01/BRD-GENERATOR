
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, MODEL_NAME

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name=MODEL_NAME
)

def extract_requirements(text):

    prompt = f"""
    Extract the following information from the client discussion:

    - Business objectives
    - Stakeholders
    - Functional requirements
    - Non-functional requirements
    - Assumptions
    - Constraints
    - Dependencies
    - Risks
    - Success metrics

    Discussion:
    {text}
    """

    response = llm.invoke(prompt)

    return response.content