#!/usr/bin/env bash

sh -c 'echo "set const" >> .nanorc'

sh -c 'echo "set tabsize 4" >> .nanorc'

sh -c 'echo "set tabstospaces" >> .nanorc'

adduser --disabled-password --gecos "" steve

usermod -aG sudo steve

cp .nanorc /home/steve/

mkdir -p /etc/ssh/steve