#!/usr/bin/env bash

use_version=$(solc-select use 0.3.0)
if [[ $use_version != "Switched global version to 0.3.0"* ]]; then
  echo "OS X FAILED: set minimum version"
  exit 255
fi
echo "OS X SUCCESS: set minimum version"

latest_release=$(curl https://raw.githubusercontent.com/tserg/vyper-select/vyper/lib/darwin/list.json |
  python3 -c "import sys,json; print(json.load(sys.stdin)['latestRelease'])")
use_version=$(solc-select use "$latest_release")
if [[ $use_version != "Switched global version to $latest_release" ]]; then
  echo "OS X FAILED: set maximum version"
  exit 255
fi
echo "OS X SUCCESS: set maximum version"

use_version=$(solc-select use 0.2.16 2>&1)
if [[ $use_version != *"Invalid version - only solc versions above '0.2.16' are available"* ]]; then
  echo "OS X FAILED: version too low"
  exit 255
fi
echo "OS X SUCCESS: version too low"

use_version=$(solc-select use 0.100.8 2>&1)
if [[ $use_version != *"Invalid version '$latest_release' is the latest available version"* ]]; then
  echo "OS X FAILED: version too high"
  exit 255
fi
echo "OS X SUCCESS: version too high"
