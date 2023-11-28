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
        with open("data/" + REQUIRED_KEYS_SPEC, "r", encoding="utf-8") as f:  # pylint: disable=invalid-name
            self.required_keys = json.load(f)

    def validate_keys(self, subject, control):
        """Validate that the subject has all the keys in the control dict."""
        assignment_keys = set(subject.keys())
        required_keys = set(control.keys())

        if not required_keys.issubset(assignment_keys):
            missing_keys = required_keys.difference(assignment_keys)
            raise InvalidResponseStructureError(
                f"The assignment is missing one or more required keys. missing: {missing_keys}"
            )
        return True

    def validate_statuscode(self):
        """Validate that the assignment's statusCode is 200."""
        if "statusCode" not in self.assignment:
            raise InvalidResponseStructureError(f"The assignment must have a statusCode. assignment: {self.assignment}")
        if not isinstance(self.assignment.get("statusCode"), int):
            status_code_type = type(self.assignment.get("statusCode"))
            raise IncorrectResponseTypeError(
                f"The assignment's statusCode must be an integer. received: {status_code_type}"
            )
        status_code = self.assignment["statusCode"]
        if not status_code == 200:
            raise ResponseFailedError(f"The assignment's statusCode must be 200. received: {status_code}")
        return True

    def validate_base64encoded(self):
        """Validate that the assignment's isBase64Encoded is False."""
        if "isBase64Encoded" not in self.assignment:
            raise InvalidResponseStructureError(
                f"The assignment must have a isBase64Encoded. assignment: {self.assignment}"
            )
        is_base64_encoded = self.assignment.get("isBase64Encoded")
        if not isinstance(is_base64_encoded, bool):
            is_base64_encoded_type = type(is_base64_encoded)
            raise IncorrectResponseTypeError(
                f"The assignment's base64Encoded must be a boolean. received: {is_base64_encoded_type}"
            )
        if self.assignment["isBase64Encoded"]:
            raise IncorrectResponseValueError("The assignment's isBase64Encoded must be False.")

    def validate_body(self):
        """Validate that the assignment's body is a dict with the correct keys."""
        if "body" not in self.assignment:
            raise InvalidResponseStructureError(f"The assignment must have a body. assignment: {self.assignment}")

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
                raise InvalidResponseStructureError(
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
            meta_data_type = type(request_meta_data)
            raise InvalidResponseStructureError(
                f"The assignment must has a dict named request_meta_data. received: {meta_data_type}"
            )
        if request_meta_data.get("lambda") is None:
            raise InvalidResponseStructureError(
                f"The request_meta_data key lambda_langchain must exist. request_meta_data: {request_meta_data}"
            )
        if request_meta_data.get("model") is None:
            raise InvalidResponseStructureError(
                f"The request_meta_data key model must exist. request_meta_data: {request_meta_data}"
            )
        if request_meta_data.get("end_point") is None:
            raise InvalidResponseStructureError(
                f"The request_meta_data end_point must exist. request_meta_data: {request_meta_data}"
            )

        if not request_meta_data.get("lambda") == "lambda_langchain":
            raise IncorrectResponseValueError(f"The request_meta_data.lambda must be lambda_langchain. body: {body}")
        if not request_meta_data.get("model") == "gpt-3.5-turbo":
            raise IncorrectResponseValueError(f"The request_meta_data.model must be gpt-3.5-turbo. body: {body}")
        if not request_meta_data.get("end_point") == "ChatCompletion":
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

    def grade_response(self, grade, message=None):
        """Create a grade dict from the assignment."""
        message_type = message.__class__.__name__ if message else "Success"
        message = str(message) if message else "Great job!"
        return {
            "grade": grade,
            "message": message,
            "message_type": message_type,
        }

    def grade(self):
        """Grade the assignment."""
        try:
            self.validate()
        except InvalidResponseStructureError as e:
            return self.grade_response(70, e)
        except ResponseFailedError as e:
            return self.grade_response(80, e)
        except IncorrectResponseValueError as e:
            return self.grade_response(85, e)
        except IncorrectResponseTypeError as e:
            return self.grade_response(90, e)
        return self.grade_response(100)
