#!/usr/bin/env bash
CUR_DIR=$(pwd)
VENV_DIR="$CUR_DIR/venv"
GECKO_VER="geckodriver-v0.32.1"
GECKO_ARCHIVE="$GECKO_VER-macos-aarch64.tar.gz"
GECKO_DRIVER_URL="https://github.com/mozilla/geckodriver/releases/download/v0.32.1/$GECKO_ARCHIVE"

if [ $# -gt 0 ] && [ $1 == "clean" ]; then
  echo "cleaning up"
  rm -rf $VENV_DIR
  rm -rf $GECKO_ARCHIVE
  rm -f geckodriver
  rm -rf bin
  rm -rf __pycache__
  rm -rf .pytest_cache
else
  echo "Preparing environment"
  cd $CUR_DIR
  python3 -m venv $VENV_DIR
  . $VENV_DIR/bin/activate
  pip3 install -r requirements.txt

  # Installing gecko driver for firefox
  # as an example (script can be extended to set up drivers from your platform)
  if [ $(uname) == "Darwin" ] && [ $(uname -m) == "arm64" ] ; then
    mkdir bin
    PATH="$(realpath bin):$PATH"
    curl -LO $GECKO_DRIVER_URL
    tar -zxf $GECKO_ARCHIVE
    mv geckodriver bin
  else
    echo "Please install browser driver manually and run tests manually"
    echo -n "Anyway "
  fi

  # launch test with test discovery
  echo "Launching test discovery"
  python3 -m unittest
fi


