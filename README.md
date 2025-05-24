# RobotFramework - WebDialogs

WebDialogs is a Robot Framework library that allows you to run interactive dialogs in a web browser instead of the console or native GUI windows.
It is designed to be compatible with the official Robot Framework Dialog library, making migration or coexistence seamless.
Additionally, it supports creating more complex dialogs using HTML templates written with Jinja2, providing flexible and customizable interfaces.
Features

- Full support for dialogs compatible with Robot Framework's built-in Dialog library.
- Simple, responsive web interaction using Bootstrap.
- Embedded Flask web server, running alongside your tests.
- Support for dialogs with buttons, inputs, and selections.
- Ability to create custom HTML dialog templates with Jinja2.
- Architecture based on Robot Framework client + Flask server for maximum flexibility.

## Installation

pip install robotframework-webdialogs

## Basic Usage

```robotframework
*** Settings ***
Library    WebDialogs

*** Tasks ***
Pause Execution
    Pause Execution    Connect the cables and press continue
```
The test will pause and open a dialog in the browser.
To view it, open:

http://localhost:5000

## Advanced Usage: Custom HTML Dialogs

You can create HTML dialog templates with Jinja2 for complex interfaces.

Use keyword `Execute Custom Step     step=complexform` to open the custom dialog.
Create the dialog template in a file named `complexform.html` in the `templates/` folder in you root project.

## Complete Example

A fully working example is available in the example folder of the repository, which includes:
- Robot Framework test code
- Flask server code
- HTML templates
- Setup and run instructions

## Architecture
- Robot Framework Client: sends dialog requests to the server.
- Flask Server: exposes a web interface where users respond to dialogs.
- Asynchronous communication with blocking waits on the Robot side until user response.

## Requirements

- Python 3.9+
- Robot Framework 7.0+
- Modern web browser (Chrome, Firefox, Edge)

## Roadmap

- Documentation on creating and using custom Jinja2 templates.
- CI/CD integration examples.
- Improved error handling and support for concurrent sessions.
