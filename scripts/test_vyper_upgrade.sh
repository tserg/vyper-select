#!/usr/bin/env bash

### Install old version of vyper
sudo pip3 uninstall vyper-select
sudo pip3 install vyper-select
old_vyper_version=$(vyper --version)
vyper-select install 0.3.0
all_old_versions=$(vyper-select versions)

### Install new version of vyper
sudo python3 setup.py develop
new_vyper_version=$(vyper --version)
all_new_versions=$(vyper-select versions)

### halt if vyper version is accidentally changed
if [ "$old_vyper_version" != "$new_vyper_version" ]; then
  echo "vyper version changed"
  exit 255
fi

if [ "$all_old_versions" != "$all_new_versions" ]; then
  echo "Upgrade failed"
  exit 255
fi

echo "Upgrade successful"
