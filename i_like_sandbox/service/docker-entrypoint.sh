#!/bin/bash

while true; do
    socat TCP-LISTEN:4444,reuseaddr,fork EXEC:"python3 /app/chal.py",stderr
done