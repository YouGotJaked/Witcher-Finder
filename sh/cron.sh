#!/bin/bash
cwd="$(dirname "$0")"
export PATH=$PATH:/usr/local/bin
cd $cwd/../
source ./venv/bin/activate && python3 -m ebay
