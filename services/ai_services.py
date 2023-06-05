# services\ai_services.py
import traceback
from fastapi import HTTPException
from logger import logger
from typing import Dict
import json
import openai

def ask_question(input_text: str, envs: Dict[str, str]) -> str:
    try:
        openai.api_key = envs["OPENAI_API_KEY"]
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Answer the following question as best you can: {question}",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        logger.info("ask_question: %s", response)
        return response.choices[0].text.strip()
    except Exception as e:
        logger.error("ask_question Exception: %s", e)
        logger.error("Exception type: %s", type(e).__name__)
        logger.error("Traceback: %s", traceback.format_exc())
        error_message = f"An error of type {type(e).__name__} occurred. Arguments:\n{e.args}"
        raise HTTPException(status_code=500, detail=error_message)

def sentiment_analysis(text: str, api_key: str) -> str:
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="davinci-codex",
            prompt=f"Analyze the sentiment of the following text: {text}",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        logger.info("sentiment_analysis: %s", response)
        sentiment = response.choices[0].text.strip()
        sentiment_dict = {"positive": float(sentiment.split()[0]), "negative": float(sentiment.split()[1])}
        return json.dumps(sentiment_dict)
    except Exception as e:
        logger.error("sentiment_analysis Exception: %s", e)
        logger.error("Exception type: %s", type(e).__name__)
        logger.error("Traceback: %s", traceback.format_exc())
        error_message = f"An error of type {type(e).__name__} occurred. Arguments:\n{e.args}"
        raise HTTPException(status_code=500, detail=error_message)

def execute_ai_service(service: str, input_data: str, envs: Dict[str, str]) -> Dict[str, str]:
    if service == "q&a":
        return {"result": ask_question(input_data, envs["OPENAI_API_KEY"])}
    elif service == "sentiment_analysis":
        return {"result": sentiment_analysis(input_data, envs["OPENAI_API_KEY"])}
    else:
        return {"error": "Invalid service specified"}

AI_SERVICES = {
    "q&a": ask_question,
    "sentiment_analysis": sentiment_analysis
}