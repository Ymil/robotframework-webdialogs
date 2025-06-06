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

![ezgif-3341d1f635d951](https://github.com/user-attachments/assets/6be4c67d-66ac-4227-b1da-f346b55fea88)

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

## Examples

### Dialogs.Get Value From User

```robotframework
Get User Personal Information
    [Documentation]    Collects basic personal information through dialogs
    ${name}=    Dialogs.Get Value From User    Please enter your first name:
    Log To Console    \nUser provided name: ${name}
```

![](assets/Get%20Value%20From%20User.png)

### Dialogs.Get Selection From User

```robotframework
Select Gender From Options
    [Documentation]    Demonstrates single-selection dialog
    @{genders}=    Create List    Male    Female    Non-binary    Prefer not to say
    ${gender}=    Dialogs.Get Selection From User    
    ...    Please select your gender:    
    ...    options=${genders}
    Log To Console   \nSelected gender: ${gender}
```

![](assets/Get%20Selection%20From%20User.png)


### Dialogs.Get Selections From User

```robotframework
Select Multiple Favorite Animals
    [Documentation]    Demonstrates multi-selection dialog with validation
    @{animals}=    Create List    Cats    Dogs    Horses    Birds    Fish
    ${selected_animals}=    Dialogs.Get Selections From User    
    ...    Select your favorite animals:    
    ...    options=${animals}
    
    Should Not Be Empty    ${selected_animals}    No animals selected
    Log To Console    \nFavorite animals: ${selected_animals}
```

![](assets/Get%20Selections%20From%20User.png)

### Dialogs.Pause Execution

```robotframework
Pause Execution
    [Documentation]    Pauses test execution and opens a dialog
    Dialogs.Pause Execution    Connect the cables and press continue
```

![](assets/Pause%20Execution.png)

### Dialogs.Execute Manual Step

```robotframework
Manual Verification Step
    [Documentation]    Requires manual user verification
    ${verification_result}=    Dialogs.Execute Manual Step    
    ...    Please verify the device connection    
    Log To Console    \nVerification result: ${verification_result}
```

![](assets/Execute%20Manual%20Step.png)

### Dialogs.Execute Custom Step

```robotframework
Process Complex Form Submission
    [Documentation]    Tests custom form handling
    ${form_response}=    Dialogs.Execute Custom Step    
    ...    step=complexform    
    
    Should Contain    ${form_response}    input    Form submission failed
    Log To Console    \nForm processing result: ${form_response}
```

![](assets/Execute%20Custom%20Step.png)


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

- [ ] Add test to the library.
- [ ] Documentation on creating and using custom Jinja2 templates.
- [ ] CI/CD integration examples.
- [ ] Improved error handling and support for concurrent sessions.
