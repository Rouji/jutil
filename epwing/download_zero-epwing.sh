#!/bin/bash
DIR=$(dirname "$0")
ZEP="$DIR/zero-epwing"
wget -O- https://foosoft.net/projects/zero-epwing/dl/zero-epwing_linux.tar.gz | tar xzOf - > "$ZEP"
chmod +x "$ZEP"
