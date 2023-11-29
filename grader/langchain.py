# -*- coding: utf-8 -*-
"""LangChain  integration models"""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from .exceptions import (
    IncorrectResponseValueError,
    InvalidResponseStructureError,
    ResponseFailedError,
)


class LCRequestMetaData(BaseModel):
    """LangChain request meta data"""

    lambda_name: str = Field(..., alias="lambda")
    model: str
    end_point: str
    temperature: float = Field(..., ge=0, le=1)
    max_tokens: int = Field(..., gt=0)


class MessageType(Enum):
    """LangChain message type"""

    human = "human"
    ai = "ai"
    assistant = "assistant"


class LCMessage(BaseModel):
    """LangChain message"""

    content: str
    additional_kwargs: dict
    type: MessageType = Field(..., alias="type")
    example: bool


class LCChatMemory(BaseModel):
    """LangChain chat memory"""

    messages: List[LCMessage]


class LCBody(BaseModel):
    """LangChain body"""

    chat_memory: LCChatMemory
    output_key: Optional[str] = Field(None)
    input_key: Optional[str] = Field(None)
    return_messages: bool
    human_prefix: str = Field("Human")
    ai_prefix: str = Field("AI")
    memory_key: str = Field("chat_history")
    request_meta_data: LCRequestMetaData


class LCResponse(BaseModel):
    """LangChain Response Dict"""

    is_base64_encoded: bool = Field(..., alias="isBase64Encoded")
    status_code: int = Field(..., alias="statusCode", ge=200, le=599)
    body: LCBody

    def validate_status_code(self):
        """Validate that the status_code == 200"""
        if self.status_code != 200:
            raise ResponseFailedError(f"status_code must be 200. received: {self.status_code}")

    def validate_is_base64_encoded(self):
        """Validate that is_base64_encoded is False"""
        if self.is_base64_encoded:
            raise IncorrectResponseValueError("is_base64_encoded must be False")

    def validate_prompt_sequence(self):
        """Validate that the prompt sequence begins with a human message and ends with an ai message"""
        messages = self.body.chat_memory.messages
        if len(messages) < 2:
            raise InvalidResponseStructureError("messages must contain at least 2 objects")

        prompt_1 = messages[0]
        if prompt_1.type != MessageType.human:
            raise IncorrectResponseValueError(
                f"First message in prompt sequence must be of type {MessageType.human}. received: {prompt_1.type}"
            )
        prompt_2 = messages[1]
        if prompt_2.type != MessageType.ai:
            raise IncorrectResponseValueError(
                f"Second message in prompt sequence must be of type {MessageType.ai}. received: {prompt_2.type}"
            )

    def validate_request_meta_data(self):
        """Validate the request_meta_data"""
        request_meta_data = self.body.request_meta_data
        if request_meta_data.lambda_name != "lambda_langchain":
            raise IncorrectResponseValueError(
                f"lambda_name must be langchain. received: {request_meta_data.lambda_name}"
            )
        if not request_meta_data.model.startswith("gpt-3.5"):
            raise IncorrectResponseValueError(f"model must be gpt-3.5. received: {request_meta_data.model}")
        if not request_meta_data.end_point == "ChatCompletion":
            raise IncorrectResponseValueError(
                f"end_point must be ChatCompletion. received: {request_meta_data.end_point}"
            )

    def validate_response(self):
        """Validate the response"""
        self.validate_status_code()
        self.validate_is_base64_encoded()
        self.validate_prompt_sequence()
        self.validate_request_meta_data()
