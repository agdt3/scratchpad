#! /bin/bash

g++ -pipe -O2 -std=c++11 "$1.cpp" -lm -o "$1"
