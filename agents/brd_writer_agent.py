
# from langchain_openai import ChatOpenAI
# from config import OPENAI_API_KEY, MODEL_NAME

# llm = ChatOpenAI(
#     openai_api_key=OPENAI_API_KEY,
#     model_name=MODEL_NAME
# )

# def generate_brd(validated_data):

#     prompt = f"""
#     Generate a professional Business Requirement Document (BRD).

#     Sections:

#     1. Executive Summary
#     2. Project Overview
#     3. Business Objectives
#     4. Scope of the Project
#        - In Scope
#        - Out of Scope
#     5. Stakeholders
#     6. Functional Requirements
#     7. Non-Functional Requirements
#     8. Data Requirements
#     9. Assumptions
#     10. Constraints
#     11. Dependencies
#     12. Risks and Mitigation
#     13. Success Criteria
#     14. Future Enhancements

#     Use structured headings and bullet points.

#     Data:
#     {validated_data}
#     """

#     response = llm.invoke(prompt)

#     return response.content







from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, MODEL_NAME

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME
)

def generate_brd(validated_data):

    prompt = f"""
    Generate a professional Business Requirement Document (BRD).

    Sections:

    1. Executive Summary
    2. Project Overview
    3. Business Objectives
    4. Scope of the Project
       - In Scope
       - Out of Scope
    5. Stakeholders
    6. Functional Requirements
    7. Non-Functional Requirements
    8. Data Requirements
    9. Assumptions
    10. Constraints
    11. Dependencies
    12. Risks and Mitigation
    13. Success Criteria
    14. Future Enhancements

    Use structured headings and bullet points.

    Data:
    {validated_data}
    """

    response = llm.invoke(prompt)

    return response.content
