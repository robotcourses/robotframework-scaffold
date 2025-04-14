WEB_SELENIUM_COMMON_KEYWORDS = """
*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Wait And Click Element
    [Arguments]    ${locator}

    Wait Until Element Is Visible    ${locator}
    Click Element    ${locator}

Wait And Input Text
    [Arguments]    ${locator}    ${text}

    Wait Until Element Is Visible    ${locator}
    Input Text    ${locator}    ${text}

Wait Element Should Contain Text
    [Arguments]    ${locator}    ${expectedText}

    Wait Until Element Is Visible  ${locator}
    Element Should Contain  ${locator}  ${expectedText}
"""

WEB_BROWSER_COMMON_KEYWORDS = """
*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Wait And Click Element
    [Arguments]    ${locator}

    Wait For Elements State    ${locator}    visible
    Click                      ${locator}

Wait And Input Text
    [Arguments]    ${locator}    ${text}

    Wait For Elements State    ${locator}    visible
    Fill Text                  ${locator}    ${text}

Wait Element Should Contain Text
    [Arguments]    ${locator}    ${expectedText}

    Wait For Elements State    ${locator}    visible
    ${actual}    Get Text      ${locator}
    Should Contain             ${actual}     ${expectedText}
"""