# -*- coding: utf-8 -*-
"""LangChain  integration models"""

from typing import List, Optional

from pydantic import BaseModel, Field


class LCRequestMetaData(BaseModel):
    """LangChain request meta data"""

    lambda_name: str = Field(..., alias="lambda")
    model: str
    end_point: str
    temperature: float = Field(..., ge=0, le=1)
    max_tokens: int = Field(..., gt=0)


class LCMessage(BaseModel):
    """LangChain message"""

    content: str
    additional_kwargs: dict
    type: str
    example: bool


class LCChatMemory(BaseModel):
    """LangChain chat memory"""

    messages: List[LCMessage]

    # @model_validator(mode="after")
    # def validate_messages(self) -> "LCChatMemory":
    #     """Validate that chat memory contains at least 2 dicts"""
    #     if len(self.messages) < 2:
    #         raise ValueError("messages must contain at least 2 objects")
    #     return self


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
