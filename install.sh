#!/bin/sh

mkdir ''$HOME'/.trans'
script_path=''$(dirname $(readlink -f "$0"))'/trans.py'
bin_path="/usr/bin/trans"

sudo ln -s $script_path $bin_path
