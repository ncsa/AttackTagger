#!/bin/bash
# install utils and dev packages for a new linux box

# get root priviledge
[ "$UID" -eq 0 ] || exec sudo -E bash "$0" "$@"

# items in this array *must* be kept in order
array=( apt utils ansible dev java kernel net python vagrant shell apt-clean )
for i in "${array[@]}"
do
	source $BOOTSTRAP_OS_DIR/$i.sh
done
