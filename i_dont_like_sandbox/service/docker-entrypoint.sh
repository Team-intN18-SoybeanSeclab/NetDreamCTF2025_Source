#!/bin/bash

chown root:root /flag
chmod 400 /flag

while true; do
    socat TCP-LISTEN:5555,reuseaddr,fork EXEC:"python3 /app/chal.py",stderr
done