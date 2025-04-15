GITIGNORE_CONTENT = """
__pycache__/
*.py[cod]
*$py.class

.env/
.venv/
venv/

*.log
*.xml
*.html
output/
report/
log.html
output.xml
report.html

.vscode/

.DS_Store
Thumbs.db

poetry.lock
"""

API_STRUCTURE = f"""
│   .gitignore
│   base.resource
│   pyproject.toml
│   README.md
│   
├───resources
│   ├───common
│   ├───connections
│   ├───data
│   ├───routes
│   └───utils
└───tests
"""

WEB_STRUCTURE = f"""
│   .gitignore
│   base.resource
│   pyproject.toml
│   README.md
│
├───resources
│   ├───common
│   ├───data
│   ├───locators
│   ├───pages
│   └───utils
└───tests
"""

MOBILE_STRUCTURE = f"""
│   .gitignore
│   base.resource
│   pyproject.toml
│   README.md
│   
├───resources
│   ├───app
│   ├───common
│   ├───data
│   ├───locators
│   ├───pages
│   └───utils
└───tests
"""

API_BASE_RESOURCE = f"""
*** Settings ***
## Libraries
Library    RequestsLibrary

## Custom Libraries

## Connections
Resource    resources/connections/session.resource
Variables   resources/connections/session_data.yml
"""

SELENIUM_BASE_RESOURCE = f"""
*** Settings ***
## Libraries
Library    SeleniumLibrary
"""

BROWSER_BASE_RESOURCE = f"""
*** Settings ***
## Libraries
Library    BrowserLibrary
"""

MOBILE_BASE_RESOURCE = f"""
*** Settings ***
## Libraries
Library    AppiumLibrary
"""