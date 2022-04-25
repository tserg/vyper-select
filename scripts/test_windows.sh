#!/usr/bin/env bash

use_version=$(solc-select use 0.3.0)
if [[ $use_version != "Switched global version to 0.3.0"* ]]; then
  echo "WINDOWS FAILED: minimum version"
  exit 255
fi
echo "WINDOWS SUCCESS: minimum version"

latest_release=$(curl https://raw.githubusercontent.com/tserg/vyper-select/vyper/lib/windows/list.json |
  python3 -c "import sys,json; print(json.load(sys.stdin)['latestRelease'])")
use_version=$(solc-select use "$latest_release")
if [[ $use_version != "Switched global version to $latest_release" ]]; then
  echo "WINDOWS FAILED: maximum version"
  exit 255
fi
echo "WINDOWS SUCCESS: maximum version"

use_version=$(solc-select use 0.2.16 2>&1)
if [[ $use_version != *"Invalid version - only solc versions above '0.3.0' are available"* ]]; then
  echo "WINDOWS FAILED: version too low"
  exit 255
fi
echo "WINDOWS SUCCESS: version too low"

use_version=$(solc-select use 0.100.8 2>&1)
if [[ $use_version != *"Invalid version '$latest_release' is the latest available version"* ]]; then
  echo "WINDOWS FAILED: version too high"
  exit 255
fi
echo "WINDOWS SUCCESS: version too high"
