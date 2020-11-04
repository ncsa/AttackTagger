#!/bin/bash
# install utils and dev packages for a new linux box

# items in this array *must* be kept in order
array=( apt utils java dev python apt-clean opengm )
#array=( opengm)
for i in "${array[@]}"
do
  source ./scripts/$i.sh
done 
