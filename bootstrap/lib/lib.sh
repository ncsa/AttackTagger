hello(){
	echo "hello"
}

base_dir(){
	BASE_DIR=$(pwd)/$(dirname $BASH_SOURCE)
}
