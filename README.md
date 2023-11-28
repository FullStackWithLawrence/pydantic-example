# Canvas Automated Grader

A Python automatic grader that evaluates JSON responses from the API end point https://api.openai.lawrencemcdaniel.com/examples/default-marv-sarcastic-chat. Verifies the structural integrity of the JSON response and implements a graduated Rubric based on how closely the response submitted matches this successful [test case](./grader/tests/events/correct.json).

## Installation

```console
git clone https://github.com/lpm0073/automatic-grader.git
cd automatic-grader
make init
make activate
```

## Usage

```console
python3 -m grader.batch 'path/to/homework/json/files/'
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

### Developer setup

```console
git clone https://github.com/lpm0073/automatic-grader.git
cd automatic-grader
make init
make activate
make test
```
