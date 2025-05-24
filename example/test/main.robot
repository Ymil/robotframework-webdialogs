*** Settings ***
Documentation     Test suite demonstrating web dialogs interaction
...               Covers user input collection, selections, and manual verification
Library          WebDialogs    WITH NAME    Dialogs
Suite Teardown   Dialogs.Close
Test Timeout     2 minutes

*** Variables ***
${DEFAULT_DELAY}    1s    # Configurable delay between interactions

*** Test Cases ***
Get User Personal Information
    [Documentation]    Collects basic personal information through dialogs
    ${name}=    Dialogs.Get Value From User    Please enter your first name:
    Log To Console    User provided name: ${name}
    
    ${lastname}=    Dialogs.Get Value From User    Please enter your last name:
    Log To Console    User provided last name: ${lastname}

Select Gender From Options
    [Documentation]    Demonstrates single-selection dialog
    @{genders}=    Create List    Male    Female    Non-binary    Prefer not to say
    ${gender}=    Dialogs.Get Selection From User    
    ...    Please select your gender:    
    ...    options=${genders}
    Log To Console    Selected gender: ${gender}

Select Multiple Favorite Animals
    [Documentation]    Demonstrates multi-selection dialog with validation
    @{animals}=    Create List    Cats    Dogs    Horses    Birds    Fish
    ${selected_animals}=    Dialogs.Get Selections From User    
    ...    Select your favorite animals:    
    ...    options=${animals}
    
    Should Not Be Empty    ${selected_animals}    No animals selected
    Log To Console    Favorite animals: ${selected_animals}

Manual Verification Step
    [Documentation]    Requires manual user verification
    ${verification_result}=    Dialogs.Execute Manual Step    
    ...    Please verify the device connection    
    Log To Console    Verification result: ${verification_result}

Handle Failed Manual Verification
    [Documentation]    Tests error handling for manual steps
    Run Keyword And Expect Error    *Verification Failed*    
    ...    Dialogs.Execute Manual Step    
    ...    This step should fail    
    ...    default_error=Verification Failed

Pause Execution For Physical Action
    [Documentation]    Pauses test for physical interaction
    Dialogs.Pause Execution    
    ...    Please connect the network cables before continuing    

Process Complex Form Submission
    [Documentation]    Tests custom form handling
    ${form_response}=    Dialogs.Execute Custom Step    
    ...    step=complexform    
    
    Should Contain    ${form_response}    SUCCESS    Form submission failed
    Log To Console    Form processing result: ${form_response}