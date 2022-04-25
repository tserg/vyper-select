import argparse
import subprocess
import sys
from .constants import (
    ARTIFACTS_DIR,
    INSTALL_VERSIONS,
    SHOW_VERSIONS,
    USE_VERSION,
    UPGRADE,
)
from .vyper_select import (
    valid_install_arg,
    valid_version,
    get_installable_versions,
    install_artifacts,
    switch_global_version,
    current_version,
    installed_versions,
    halt_old_architecture,
    upgrade_architecture,
)


def vyper_select() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        help="Allows users to install and quickly switch between Vyper compiler versions"
    )
    parser_install = subparsers.add_parser(
        "install", help="list and install available Vyper versions"
    )
    parser_install.add_argument(
        INSTALL_VERSIONS,
        help='specific versions you want to install "3.0.0" or "all"',
        nargs="*",
        default=list(),
        type=valid_install_arg,
    )
    parser_use = subparsers.add_parser("use", help="change the version of global Vyper compiler")
    parser_use.add_argument(
        USE_VERSION, help="Vyper version you want to use (eg: 0.3.0)", type=valid_version, nargs="?"
    )
    parser_use.add_argument("--always-install", action="store_true")
    parser_use = subparsers.add_parser("versions", help="prints out all installed Vyper versions")
    parser_use.add_argument(SHOW_VERSIONS, nargs="*", help=argparse.SUPPRESS)
    parser_use = subparsers.add_parser("upgrade", help="upgrades vyper-select")
    parser_use.add_argument(UPGRADE, nargs="*", help=argparse.SUPPRESS)

    args = vars(parser.parse_args())

    if args.get(INSTALL_VERSIONS) is not None:
        versions = args.get(INSTALL_VERSIONS)
        if not versions:
            print("Available versions to install:")
            for version in get_installable_versions():
                print(version)
        else:
            install_artifacts(args.get(INSTALL_VERSIONS))

    elif args.get(USE_VERSION) is not None:
        switch_global_version(args.get(USE_VERSION), args.get("always_install"))

    elif args.get(SHOW_VERSIONS) is not None:
        res = current_version()
        if res:
            (current_ver, source) = res
        for version in reversed(sorted(installed_versions())):
            if res and version == current_ver:
                print(f"{version} (current, set by {source})")
            else:
                print(version)
    elif args.get(UPGRADE) is not None:
        upgrade_architecture()
    else:
        parser.parse_args(["--help"])
        sys.exit(0)


def vyper() -> None:
    res = current_version()
    if res:
        (version, _) = res
        path = ARTIFACTS_DIR.joinpath(f"vyper.{version}", f"vyper.{version}")
        halt_old_architecture(path)
        try:
            process = subprocess.run(
                [str(path)] + sys.argv[1:], stdout=subprocess.PIPE, stdin=None, check=True
            )
            print(str(process.stdout, "utf-8"))
        except subprocess.CalledProcessError:
            sys.exit(1)
    else:
        sys.exit(1)
