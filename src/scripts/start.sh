#!/bin/bash

env=$(poetry env activate) && $env

# uvicorn src.app:app --host 0.0.0.0 --port 8888