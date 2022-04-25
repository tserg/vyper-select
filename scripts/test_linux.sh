#!/usr/bin/env bash

sudo python3 setup.py install
vyper-select install all

use_version=$(vyper-select use 0.3.0)
if [[ $use_version != *"Switched global version to 0.3.0"* ]]; then
  echo "LINUX FAILED: minimum version"
  exit 255
fi
echo "LINUX SUCCESS: minimum version"

latest_release=$(curl https://raw.githubusercontent.com/tserg/vyper-select/vyper/lib/linux/list.json |
  python3 -c "import sys,json; print(json.load(sys.stdin)['latestRelease'])")
use_version=$(solc-select use "$latest_release")
if [[ $use_version != "Switched global version to $latest_release" ]]; then
  echo "LINUX FAILED: maximum version"
  exit 255
fi
echo "LINUX SUCCESS: maximum version"

use_version=$(solc-select use 0.2.16 2>&1)
if [[ $use_version != *"Invalid version - only Vyper versions above '0.3.0' are available"* ]]; then
  echo "LINUX FAILED: version too low"
  exit 255
fi
echo "LINUX SUCCESS: version too low"

use_version=$(solc-select use 0.100.8 2>&1)
if [[ $use_version != *"Invalid version '$latest_release' is the latest available version"* ]]; then
  echo "LINUX FAILED: version too high"
  exit 255
fi
echo "LINUX SUCCESS: version too high"
