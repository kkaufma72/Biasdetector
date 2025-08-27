"""Interface with an LLM via LangChain to rewrite biased text."""

from __future__ import annotations

import os
import logging
from typing import Optional

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

logger = logging.getLogger(__name__)

REWRITE_PROMPT = (
    "Rewrite the following text to remove any gender or racial bias while"
    " preserving the original meaning. Return only the rewritten text.\n{text}"
)


def rewrite_text(text: str, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo") -> str:
    """Return a neutral rewrite of ``text`` using an LLM.

    If no API key is supplied, the original text is returned.
    """

    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        logger.warning("No OpenAI API key provided; returning original text")
        return text

    llm = ChatOpenAI(openai_api_key=key, model=model, temperature=0)
    prompt = ChatPromptTemplate.from_template(REWRITE_PROMPT)
    chain = prompt | llm
    try:
        return chain.invoke({"text": text}).content.strip()
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("LLM rewrite failed: %s", exc)
        return text
