#!/bin/sh

touch .env

for envvar in "$@"
do
   echo "$envvar" >> .env
done
