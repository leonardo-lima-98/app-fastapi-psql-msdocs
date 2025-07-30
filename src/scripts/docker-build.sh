#!/bin/bash

git_hash=$(git rev-parse --short HEAD)

docker build -t fast_zero-app:$git_hash-v0.0$versao .
