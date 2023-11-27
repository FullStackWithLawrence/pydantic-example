# -*- coding: utf-8 -*-
"""Provide a class for grading a submission against an assignment.""" ""

import json

from .exceptions import (
    IncorrectResponseTypeError,
    IncorrectResponseValueError,
    InvalidResponseStructureError,
    ResponseFailedError,
)


REQUIRED_KEYS_SPEC = "required-keys.json"
HUMAN_PROMPT = {"content": "a prompt from a human", "additional_kwargs": {}, "type": "human", "example": False}
AI_RESPONSE = {"content": "a response from the AI", "additional_kwargs": {}, "type": "ai", "example": False}


# flake8: noqa: E701
class AutomatedGrader:
    """Grade a submission against an assignment."""

    def __init__(self, assignment):
        self.assignment = assignment
        with open(REQUIRED_KEYS_SPEC, "r", encoding="utf-8") as f:  # pylint: disable=invalid-name
            self.required_keys = json.load(f)

    def validate_keys(self, subject, control):
        """Validate that the subject has all the keys in the control dict."""
        assignment_keys = set(subject.keys())
        required_keys = set(control.keys())

        if not required_keys.issubset(assignment_keys):
            raise InvalidResponseStructureError("The assignment is missing one or more required keys.")
        return True

    def validate_statuscode(self):
        """Validate that the assignment's statusCode is 200."""
        if not isinstance(self.assignment.get("statusCode"), int):
            raise IncorrectResponseTypeError("The assignment's statusCode must be an integer.")
        if not self.assignment["statusCode"] == 200:
            raise IncorrectResponseValueError("The assignment's statusCode must be 200.")
        return True

    def validate_base64encoded(self):
        """Validate that the assignment's isBase64Encoded is False."""
        if not isinstance(self.assignment.get("isBase64Encoded"), bool):
            raise IncorrectResponseTypeError("The assignment's base64Encoded must be a boolean.")
        if self.assignment["isBase64Encoded"]:
            raise IncorrectResponseValueError("The assignment's isBase64Encoded must be False.")

    def validate_body(self):
        """Validate that the assignment's body is a dict with the correct keys."""
        body = self.assignment.get("body")
        if not isinstance(body, dict):
            body_type = type(body)
            raise IncorrectResponseTypeError(f"The assignment's body must be a dict. Received {body_type}.")
        if not "chat_memory" in body:
            raise InvalidResponseStructureError(
                f"The assignment's body must have a key named chat_memory. body: {body}"
            )
        if not "messages" in body["chat_memory"]:
            raise InvalidResponseStructureError(
                f"The assignment's body.chat_memory must has a key named messages. body: {body}"
            )
        messages = body["chat_memory"]["messages"]
        if not isinstance(messages, list):
            messages_type = type(messages)
            raise IncorrectResponseTypeError(
                f"The assignment's body.chat_memory.messages must be a list. Received {messages_type}."
            )
        if len(messages) < 2:
            raise InvalidResponseStructureError(
                f"The messages list must contain at least two elements. messages: {messages}"
            )

        for message in messages:
            if not isinstance(message, dict):
                raise IncorrectResponseTypeError(
                    f"All elements in the messages list must be dictionaries. messages: {messages}"
                )

        human_prompt = messages[0]
        ai_response = messages[1]

        self.validate_keys(human_prompt, HUMAN_PROMPT)
        self.validate_keys(ai_response, AI_RESPONSE)

        if not human_prompt["type"] == "human":
            raise IncorrectResponseValueError(f"The first message must be a human prompt. first prompt: {human_prompt}")
        if not ai_response["type"] == "ai":
            raise IncorrectResponseValueError(f"The second message must be an AI response. response: {ai_response}")

    def validate_metadata(self):
        """Validate that the assignment's metadata is a dict with the correct keys."""
        body = self.assignment.get("body")
        request_meta_data = body["request_meta_data"]
        if not isinstance(request_meta_data, dict):
            raise InvalidResponseStructureError(f"The assignment must has a dict named request_meta_data. body: {body}")
        if not request_meta_data["lambda"] == "lambda_langchain":
            raise IncorrectResponseValueError(f"The request_meta_data.lambda must be lambda_langchain. body: {body}")
        if not request_meta_data["model"] == "gpt-3.5-turbo":
            raise IncorrectResponseValueError(f"The request_meta_data.model must be gpt-3.5-turbo. body: {body}")
        if not request_meta_data["end_point"] == "ChatCompletion":
            raise IncorrectResponseValueError(f"The request_meta_data.end_point must be ChatCompletion. body: {body}")

    def validate(self):
        """Validate the assignment data structure."""
        if not isinstance(self.assignment, dict):
            raise InvalidResponseStructureError("The assignment must be a dictionary.")
        self.validate_keys(self.assignment, self.required_keys)
        self.validate_statuscode()
        self.validate_base64encoded()
        self.validate_body()
        self.validate_metadata()

    def grade_response(self, grade, message):
        """Create a grade dict from the assignment."""
        return {
            "grade": grade,
            "message": message,
        }

    def grade(self):
        """Grade the assignment."""
        self.validate()
        try:
            self.validate()
        except InvalidResponseStructureError as e:
            return self.grade_response(75, e.message)
        except ResponseFailedError as e:
            return self.grade_response(80, e.message)
        except IncorrectResponseValueError as e:
            return self.grade_response(85, e.message)
        except IncorrectResponseTypeError as e:
            return self.grade_response(90, e.message)
        return self.grade_response(100, "Great job!")
