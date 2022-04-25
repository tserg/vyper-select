## solc 0.4.5 ##
vyper-select use 0.3.0  &> /dev/null
solc ./scripts/vyper_tests/vy030.vy

if [[ $? != 0 ]]; then
  echo "FAILED: vy030_success" $?
  exit 255
fi
echo "SUCCESS: vy030_success"
