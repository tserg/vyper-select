import argparse
import json
from zipfile import ZipFile
import os
import shutil
import re
import sys
import urllib.request
from distutils.version import StrictVersion
from .constants import *

Path.mkdir(ARTIFACTS_DIR, parents=True, exist_ok=True)


def halt_old_architecture(path: Path) -> None:
    if not Path.is_file(path):
        raise argparse.ArgumentTypeError(
            "vyper-select is out of date. Please run `vyper-select update`"
        )



def upgrade_architecture() -> None:
    currently_installed = installed_versions()
    if len(currently_installed) > 0:
        if Path.is_file(ARTIFACTS_DIR.joinpath(f"vyper.{currently_installed[0]}")):
            shutil.rmtree(ARTIFACTS_DIR)
            Path.mkdir(ARTIFACTS_DIR, exist_ok=True)
            install_artifacts(currently_installed)
            print("vyper-select is now up to date! 🎉")
        else:
            raise argparse.ArgumentTypeError("vyper-select is already up to date")
    else:
        raise argparse.ArgumentTypeError("Run `vyper-select install --help` for more information")


def current_version() -> (str, str):
    version = os.environ.get("VYPER_VERSION")
    source = "VYPER_VERSION"
    if version:
        if version not in installed_versions():
            raise argparse.ArgumentTypeError(
                f"Version '{version}' not installed (set by {source}). Run `vyper-select install {version}`."
            )
    else:
        source = VYPER_SELECT_DIR.joinpath("global-version")
        if Path.is_file(source):
            with open(source) as f:
                version = f.read()
        else:
            raise argparse.ArgumentTypeError(
                "No Vyper version set. Run `vyper-select use VERSION` or set VYPER_VERSION environment variable."
            )
    return version, source


def installed_versions() -> [str]:
    return [
        f.replace("vyper.", "") for f in sorted(os.listdir(ARTIFACTS_DIR)) if f.startswith("vyper.")
    ]


def install_artifacts(versions: [str]) -> None:
    releases = get_available_versions()

    for version, artifact in releases.items():
        if "all" not in versions:
            if versions and version not in versions:
                continue

        (url, _) = get_url(version, artifact)
        artifact_file_dir = ARTIFACTS_DIR.joinpath(f"vyper.{version}")
        Path.mkdir(artifact_file_dir, parents=True, exist_ok=True)
        print(f"Installing '{version}'...")
        urllib.request.urlretrieve(url, artifact_file_dir.joinpath(f"vyper.{version}"))
        Path.chmod(artifact_file_dir.joinpath(f"vyper.{version}"), 0o775)
        print(f"Version '{version}' installed.")


def get_url(version: str = "", artifact: str = "") -> (str, str):
    return (
        f"https://github.com/vyperlang/vyper/releases/download/v{version}/{artifact}",
        f"https://raw.githubusercontent.com/tserg/vyper-select/vyper/lib/{vyperlang_platform()}/list.json",
    )


def switch_global_version(version: str, always_install: bool) -> None:
    if version in installed_versions():
        with open(f"{VYPER_SELECT_DIR}/global-version", "w") as f:
            f.write(version)
        print("Switched global version to", version)
    elif version in get_available_versions():
        if always_install:
            install_artifacts([version])
            switch_global_version(version, always_install)
        else:
            raise argparse.ArgumentTypeError(f"'{version}' must be installed prior to use.")
    else:
        raise argparse.ArgumentTypeError(f"Unknown version '{version}'")


def valid_version(version: str) -> str:
    match = re.search(r"^(\d+)\.(\d+)\.(\d+)$", version)

    if match is None:
        raise argparse.ArgumentTypeError(f"Invalid version '{version}'.")

    (_, list_url) = get_url()
    list_json = urllib.request.urlopen(list_url).read()
    latest_release = json.loads(list_json)["latestRelease"]
    if StrictVersion(version) > StrictVersion(latest_release):
        raise argparse.ArgumentTypeError(
            f"Invalid version '{latest_release}' is the latest available version"
        )

    return version


def valid_install_arg(arg: str) -> str:
    if arg == "all":
        return arg
    return valid_version(arg)


def get_installable_versions() -> [str]:
    installable = list(set(get_available_versions()) - set(installed_versions()))
    installable.sort(key=StrictVersion)
    return installable


def get_available_versions() -> [str]:
    (_, list_url) = get_url()
    list_json = urllib.request.urlopen(list_url).read()
    available_releases = json.loads(list_json)["releases"]
    if vyperlang_platform() == LINUX_AMD64:
        (_, list_url) = get_url(version=EARLIEST_RELEASE[LINUX_AMD64])
        github_json = urllib.request.urlopen(list_url).read()
        additional_linux_versions = json.loads(github_json)["releases"]
        available_releases.update(additional_linux_versions)

    return available_releases


def vyperlang_platform() -> str:
    if sys.platform.startswith("linux"):
        platform = LINUX_AMD64
    elif sys.platform == "darwin":
        platform = MACOSX_AMD64
    elif sys.platform == "win32" or sys.platform == "cygwin":
        platform = WINDOWS_AMD64
    else:
        raise argparse.ArgumentTypeError("Unsupported platform")
    return platform
