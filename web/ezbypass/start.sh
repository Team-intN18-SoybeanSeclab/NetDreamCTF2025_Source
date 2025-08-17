#!/bin/bash

echo -n "$FLAG" > /flag


chmod 777 /flag

unset FLAG

exec apache2-foreground