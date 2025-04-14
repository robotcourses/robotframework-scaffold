MOBILE_COMMON_KEYWORDS = """
*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Open App

    Open Application    
    ...    remote_url=http://localhost:4723/wd/hub
    ...    automationName=UIAutomator2
    ...    platformName=android
    ...    deviceName=Google Pixel 7 Pro
    ...    app=${CURDIR}${/}..${/}app${/}app.apk
    ...    disableIdLocatorAutocompletion=${True}

Wait Until Element Is Enabled
    [Arguments]    ${locator}

    WHILE    ${True}
        ${status}  Run Keyword And Return Status  Element Should Be Enabled    ${locator}
        Exit For Loop If    ${status}
    END

Wait Visible And Click Element
    [Arguments]    ${locator}

    Wait Until Element Is Visible    ${locator}
    Click Element    ${locator}

Wait Enabled And Click Element
    [Arguments]    ${locator}

    Wait Until Element Is Enabled    ${locator}
    Click Element    ${locator}

Wait Visible And Input Text
    [Arguments]    ${locator}    ${text}

    Wait Until Element Is Visible    ${locator}
    Click Element    ${locator}
    Is Keyboard Shown
    Input Text    ${locator}    ${text}

Swipe to Element
    [Arguments]  ${locator}

    ${start_x}  Set Variable  550
    ${start_y}  Set Variable  1260

    WHILE    ${True}    limit=60s
        ${status}  Run Keyword And Return Status  Wait Until Element Is Visible    ${locator}

        IF    ${status}
            Exit For Loop
        ELSE
            ${offset_x}  Set Variable  ${${start_x} + 5}
        END

        Swipe
        ...    start_x=${start_x}
        ...    start_y=${start_y}
        ...    offset_x=${offset_x}
        ...    offset_y=0
    END

Swipe Until Element Is Visible
    [Arguments]    ${locator}
    
    ${x}  Get Window Width
    ${y}  Get Window Height

    ${start_x}  Evaluate  ${x} / 2
    ${start_y}  Evaluate  ${y} / 2

    WHILE    ${True}    limit=60s
        ${status}    Run Keyword And Return Status    Wait Until Element Is Visible    ${locator}  1

        IF    ${status}
            Exit For Loop
        END

        Swipe    
        ...    start_x=${start_x}
        ...    start_y=${start_y}
        ...    offset_x=${start_x}
        ...    offset_y=0
    END
"""