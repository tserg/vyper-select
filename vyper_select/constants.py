import os
from pathlib import Path

# DIRs path
if "VIRTUAL_ENV" in os.environ:
    HOME_DIR = Path(os.environ["VIRTUAL_ENV"])
else:
    HOME_DIR = Path.home()
VYPER_SELECT_DIR = HOME_DIR.joinpath(".vyper-select")
ARTIFACTS_DIR = VYPER_SELECT_DIR.joinpath("artifacts")

# CLI Flags
INSTALL_VERSIONS = "INSTALL_VERSIONS"
USE_VERSION = "USE_VERSION"
SHOW_VERSIONS = "SHOW_VERSIONS"
UPGRADE = "UPGRADE"

LINUX_AMD64 = "linux"
MACOSX_AMD64 = "darwin"
WINDOWS_AMD64 = "windows"

EARLIEST_RELEASE = {"darwin": "0.3.0", "linux": "0.3.0", "windows": "0.3.0"}
