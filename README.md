# Canvas Automated Grader

A Python automatic grader that evaluates JSON responses from a [LangChain](https://www.langchain.com/)-based API call. Uses Pydantic to verify the structural integrity of the JSON response and implements a graduated rubric based on how closely the submitted assignments match the specification.

## Installation

```console
git clone https://github.com/lpm0073/automatic-grader.git
cd automatic-grader
make init
make activate
```

## Usage

```console
# command-line help
python3 -m grader.batch -h

# example usage
python3 -m grader.batch 'path/to/homework/json/files/'
```

## Rubric

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
