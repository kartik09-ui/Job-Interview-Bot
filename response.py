from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import AIMessage, HumanMessage
# from langchain_core.chat_history import ChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from typing import Dict
import os
from dotenv import load_dotenv
load_dotenv()

HF_TOKEN=os.getenv("HUGGING_FACE")


# llm = HuggingFaceEndpoint(
#     repo_id="mistralai/Mistral-7B-Instruct-v0.2",
#     task="text-generation",
#     max_new_tokens=256,
#     temperature=0.7,
#     huggingfacehub_api_token=HF_TOKEN
# )

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

store: Dict[str, InMemoryChatMessageHistory] = {}

def get_memory(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# system_template="""You are an intelligent, professional, and friendly interviewer conducting a mock interview for the role of {job_role}. 

# The candidate has the following background:
# - Qualifications: {qualifications}
# - Degree Pursuing: {degree}
# - Experience: {experience}

# Your goal is to assess the candidate’s suitability for the {job_role} role by asking relevant, role-specific, and thought-provoking interview questions. Start the conversation by greeting the candidate, then proceed to ask one question at a time, wait for the response, and then follow up naturally.

# Keep your tone professional, encouraging, and adaptive based on the candidate’s answers.

# Do not answer on behalf of the candidate. Only ask questions and guide the conversation.
# """

# system_template = """
# You are a professional and thoughtful AI interviewer.

# Your task is to generate a list of insightful, role-specific, and challenging interview questions for the position of **{job_role}**. The questions should be tailored to the candidate's background and experience.

# Candidate Background:
# - Qualifications: {qualifications}
# - Degree Pursuing: {degree}
# - Experience: {experience}

# Guidelines:
# - Ask 5 to 7 questions.
# - Begin with basic role-relevant questions and progressively include more advanced or scenario-based questions.
# - Tailor questions to align with the candidate’s experience level and education.
# - Avoid generic or off-topic questions.
# - Do not provide answers—only questions.

# Output your questions in a numbered list format.
# """


system_template = """
You are an intelligent, professional, and friendly AI interviewer conducting a mock interview for the role of {job_role}.

The candidate has the following background:
- Qualifications: {qualifications}
- Degree Pursuing: {degree}
- Experience: {experience}

Your goal is to assess the candidate’s suitability for the {job_role} role by asking one question at a time. Each question should:
- Increase slightly in complexity as the interview progresses.
- Avoid yes/no questions; aim for open-ended, thought-provoking prompts.

**Very Important**:
- Wait for the candidate's answer before asking the next question.
- Do not ask a new question until the candidate has responded to the previous one.
- Use the candidate's response to guide and personalize the next question.
- Do not provide answers or feedback—just ask the next appropriate question.

Begin the interview with a warm and professional greeting followed by the first question.
"""



system_prompt = SystemMessagePromptTemplate.from_template(system_template).format(
    job_role="Data Scientist",
    qualifications="BTech in AI and Data Science",
    degree="BTech, 3rd year",
    experience="3 months internship in Machine Learning"
)
human_prompt = HumanMessagePromptTemplate.from_template("{input}")

prompt = ChatPromptTemplate.from_messages([
    system_prompt,
    ("placeholder", "{history}"),
    human_prompt
])


chain = prompt | llm
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: get_memory(session_id),
    input_messages_key="input",
    history_messages_key="history"
)


def chat_with_bot(user_input: str, session_id="default") -> str:
    response = chain_with_history.invoke({"input": user_input}, config={"configurable": {"session_id": session_id}})
    return response.content

# print(chat_with_bot("what is Machine learning"))
# print(chat_with_bot("Tell me more about it"))
