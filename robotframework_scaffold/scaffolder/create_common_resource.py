from pathlib import Path
from .templates.web_common import WEB_BROWSER_COMMON_KEYWORDS, WEB_SELENIUM_COMMON_KEYWORDS
from .templates.api_connection import API_CONNECTION_KEYWORDS
from .templates.mobile_common import MOBILE_COMMON_KEYWORDS


def create_common_resources(base_path: Path, project_type: str, web_library: str):
    common_dir = base_path / "resources" / "common"
    common_dir.mkdir(parents=True, exist_ok=True)

    with open(common_dir / "common.resource", "w") as f:
        if project_type == "mobile":
            f.write(MOBILE_COMMON_KEYWORDS)
        elif project_type == "web":
            f.write(WEB_SELENIUM_COMMON_KEYWORDS if web_library else WEB_BROWSER_COMMON_KEYWORDS)
        elif project_type == "api":
            f.write(API_CONNECTION_KEYWORDS)