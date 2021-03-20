#!/usr/bin/env bash

OPTIONS=$(getopt -o i:h: -l input,output -- "$@")

usage(){
  echo "It is a simple 'Hello world' Programm  [-i input of the file to read in]" 1>&2
 }

exit_abnormal(){
  usage
  exit 1
}

if [ $? -ne 0 ]; then
  echo "getopt error"
  exit 1
fi

eval set -- $OPTIONS

while getopts "i:h:" options; do
  case "${options}" in
    h)
      exit_abnormal
      exit 1
      ;;
    i)
      INPUT=${OPTARG}
      echo "Hello World!"
      printf %s "$(< $INPUT)"
      ;;
    :)
      echo "Error: -${OPTARG} requires an argument"
      exit_abnormal
      ;;
    *)
      exit_abnormal
      ;;
  esac
done