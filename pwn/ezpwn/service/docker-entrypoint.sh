#!/bin/sh

if [ "$DASFLAG" ]; then
    INSERT_FLAG="$DASFLAG"
elif [ "$FLAG" ]; then
    INSERT_FLAG="$FLAG"
elif [ "$GZCTF_FLAG" ]; then
    INSERT_FLAG="$GZCTF_FLAG"
else
    INSERT_FLAG="flag{TEST_Dynamic_FLAG}"
fi

adduser --disabled-password --gecos "" ctf || true

echo "$INSERT_FLAG" > /home/ctf/flag
chown ctf:ctf /home/ctf/flag
chmod 400 /home/ctf/flag

socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"setpriv --reuid=ctf --regid=ctf --init-groups /home/ctf/attachment"
