API_CONNECTION_KEYWORDS = """
*** Settings ***
Resource    ../../base.resource

*** Keywords ***
Create App Session

    Create Session
    ...  alias=${alias}
    ...  url=${url}
    ...  verify=${False}
    ...  disable_warnings=${True}
"""