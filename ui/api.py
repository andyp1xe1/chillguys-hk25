import anonymizer
from google import genai
from typing import Tuple

client = anonymizer.Anonymizer()

def anonymize(text: str) -> Tuple[str, dict]:
    res = client.anonymize(text)
    return res

def deanonymize(text: str, metadata: dict):
    return client.deanonymize(text, metadata)

def gemini(text: str) -> str:
    prompt = f"""
        You will get a prompt from the user.
        This prompt will be in Romanian, and you should respond in Romanian.
        The prompt will contain certain placeholders for sensitive information, such as:
        - <NAME_1>
        - <NAME_2>
        - <EMAIL_1>
        - <ADDRESS_1>

        Each placeholder represents a specific type of sensitive information that has been anonymized, and is unique with an index number.
        Your task is to generate a response that is contextually relevant to the user's prompt, while ensuring that the placeholders are preserved in their original form.
        Do not attempt to replace or modify the placeholders in any way.
        Focus on providing a coherent and meaningful response that aligns with the content of the prompt, while maintaining the integrity of the anonymized data.

        Here is the user's prompt:

        {text}
    """

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    )
    return response.text if response.text else ""
