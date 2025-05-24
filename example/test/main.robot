*** Settings ***
Library    WebDialogs     WITH NAME    Dialogs

Suite Teardown   Dialogs.close
    

*** Test Cases ***
Ask For Name
    ${name}=    Get Value From User    What is your name?
    Log to console    Entered name: ${name}

    ${lastname}=    Get Value From User    What is your last name?
    Log to console    Entered last name: ${lastname}

Ask For Gender
    ${genders} =    Create List     Male   Female
    ${gender}=   Get Selection From User    What is your gender?     options=${genders}
    Log to console    Entered gender: ${gender}

Ask For Animals
    ${animals} =   Create List     Cats   Dogs  Horses
    ${selected_animals}=   Get Selections From User    What are your favorite animals?     options=${animals}
    Log to console    Entered animals: ${selected_animals}

Pass Or Fail
    ${result}     Execute Manual Step   Manual Verification
    Log to console      Result: ${result}

Pass Or Fail With Default Message
    Run Keyword And Expect Error    *Error*     Execute Manual Step   Manual Verification   default_error=Error message

Pause Execution
    Pause Execution     Connect cables

Custom Execution
    ${response} =   Execute Custom Step     step=complexform
    Log to console  ${response}