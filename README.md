[![Python](https://a11ybadges.com/badge?logo=python)](https://www.python.org/)
[![Pydantic](https://a11ybadges.com/badge?text=Pydantic&badgeColor=e92063)](https://www.langchain.com/)
[![JSON](https://a11ybadges.com/badge?logo=json)](https://www.json.org/json-en.html)
[![FullStackWithLawrence](https://a11ybadges.com/badge?text=FullStackWithLawrence&badgeColor=orange&logo=youtube&logoColor=282828)](https://www.youtube.com/@FullStackWithLawrence)

![GHA pushMain Status](https://img.shields.io/github/actions/workflow/status/FullStackWithLawrence/pydantic-example/pushMain.yml?branch=main)
[![AGPL License](https://img.shields.io/github/license/overhangio/tutor.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.en.html)
[![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

# Pydantic Examples

[Pydantic](https://docs.pydantic.dev/latest/) is the most widely used data validation library for Python. This repo demonstrates three popular use cases for Pydantic:

1. **Validation**. Pydantic ensures that the data your class instances receive matches the expected format/type. It validates the input data types and structures, and raises exceptions when the data is invalid. See the [example Python class](./grader/grader.py) in this repo.

2. **Data Parsing and Serialization**. See the [JSON validator](./grader/langchain.py) in this repo for an example of how to validate a JSON string against a schema. Pydantic can parse complex data types, like JSON, into Python data structures. It can also serialize Python objects back into JSON.

3. **Exception Handling**. See the [custom exceptions](./grader/exceptions.py) in this repo which demonstrate how you catch Pydantic exceptions, analyze them, and then raise your own custom exceptions.

## Installation

```console
git clone https://github.com/FullStackWithLawrence/pydantic-example.git
cd pydantic-example
make init
source venv/bin/activate
```

## Usage

```console
# command-line help
python3 -m grader.batch -h

# example usage
python3 -m grader.batch 'path/to/homework/json/files/'
```

### About This Example

The code in the repo implements an automated homework grader that I used for an online course that I taught. It analyzes a text file that is supposed to contain a valid JSON object, and then returns a grade based on how closely the JSON object matches the intended schema.

### Rubric

Rubric values are expressed as floats between 0 and 1.00, and can be overridden with environment variables.

```console
AG_INCORRECT_RESPONSE_TYPE_PENALTY_PCT=0.10
AG_INCORRECT_RESPONSE_VALUE_PENALTY_PCT=0.15
AG_RESPONSE_FAILED_PENALTY_PCT=0.20
AG_INVALID_RESPONSE_STRUCTURE_PENALTY_PCT=0.30
AG_INVALID_JSON_RESPONSE_PENALTY_PCT=0.50
```

### Expected output

```console
% done! Graded 10 assignments. Output files are in path/to/homework/json/files/out
```

<!-- prettier-ignore -->
```json
{
  "grade": 100,
  "message": "Great job!",
  "message_type": "Success"
}
```

<!-- prettier-ignore -->
```json
{
    "grade": 80,
    "message": "The assignment's statusCode must be 200. received: 403",
    "message_type": "ResponseFailedError"
}
```

<!-- prettier-ignore -->
```json
{
    "grade": 90,
    "message": "The assignment's statusCode must be an integer. received: <class 'str'>",
    "message_type": "IncorrectResponseTypeError"
}
```

<!-- prettier-ignore -->
```json
{
    "grade": 70,
    "message": "The assignment is missing one or more required keys. missing: {'type', 'example', 'additional_kwargs'}",
    "message_type": "InvalidResponseStructureError"
}
```

<!-- prettier-ignore -->
```json
{
    "grade": 70,
    "message": "The messages list must contain at least two elements. messages: [{'content': \"Oh, how delightful. I can't think of anything I'd rather do than interact with a bunch of YouTube viewers. Just kidding, I'd rather be doing literally anything else. But go ahead, introduce me to your lovely audience. I'm sure they'll be absolutely thrilled to meet me.\", 'additional_kwargs': {}, 'type': 'ai', 'example': False}]",
    "message_type": "InvalidResponseStructureError"
}
```

<!-- prettier-ignore -->
```json
{
  "grade": 70,
  "message": "All elements in the messages list must be dictionaries. messages: ['bad', 'data']",
  "message_type": "InvalidResponseStructureError"
}
```

<!-- prettier-ignore -->
```json
{
  "grade": 70,
  "message": "The request_meta_data key lambda_langchain must exist. request_meta_data: {}",
  "message_type": "InvalidResponseStructureError"
}
```

## Contributing

This project uses a mostly automated pull request and unit testing process. See the resources in .github for additional details. You additionally should ensure that pre-commit is installed and working correctly on your dev machine by running the following command from the root of the repo.

```console
pre-commit run --all-files
```

Pull requests should pass these tests before being submitted:

```console
make test
```

### Developer setup

```console
git clone https://github.com/lpm0073/automatic-grader.git
cd automatic-grader
make init
make activate
```
