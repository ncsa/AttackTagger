# Setup dev environment for osx and ubuntu
# Time-stamp: <2014-10-24 13:02:03 phcao>


#
# constants
#
# Absolute path to this script, e.g. /home/user/bin/foo.sh

export BASE_DIR=$(pwd)
# BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
OS=$(uname -s | tr '[:upper:]' '[:lower:]')

export BOOTSTRAP_DOTFILES_DIR=$BASE_DIR/dotfiles
export BOOTSTRAP_LIB_DIR=$BASE_DIR/lib

export BOOTSTRAP_BOOTSTRAP_DIR=$BASE_DIR/bootstrap
export BOOTSTRAP_ANSIBLE_DIR=$BOOTSTRAP_BOOTSTRAP_DIR/ansible

export BOOTSTRAP_OS_DIR=$BOOTSTRAP_BOOTSTRAP_DIR/$OS
export BOOTSTRAP_COMMON_DIR=$BOOTSTRAP_BOOTSTRAP_DIR/common
export VAGRANT_DIR=/vagrant

#
# library
#
# . $BOOTSTRAP_LIB_DIR/lib.sh

#
# helper functions
#

# bootstrap
bootstrap () {
  $BOOTSTRAP_OS_DIR/bootstrap.sh

  # post-bootstrap
  $BOOTSTRAP_COMMON_DIR/bootstrap.sh
}

# run ansible playbook
run_ansible_playbook () {
  ansible-playbook $BOOTSTRAP_ANSIBLE_DIR/dev.yml -i $BOOTSTRAP_ANSIBLE_DIR/.ansible_hosts -Kv
}

# install dotfiles
dotfiles () {
  $BOOTSTRAP_DOTFILES_DIR/bootstrap.sh
}

#
# main bash file
#

# parse arguments
while getopts :bmlvpdu flag; do
  case $flag in
    b)
	  bootstrap
      ;;
    m)
	  run_ansible_playbook
      ;;
    l)
      ;;
    v)
	  cd $VAGRANT_DIR
	  ./install.sh -b
	  ;;
    p)
	  ansible all -m ping -i $BOOTSTRAP_ANSIBLE_DIR/.ansible_hosts
      ;;
    d)
	  dotfiles
      ;;
    u)
	  export BOOTSTRAP_USER=$OPTARG
      ;;
    ?)
      exit 0
      ;;
  esac
done

# print remaining arguments
shift $(( ${OPTIND} - 1 )); echo "${*}"

# print usage
display_usage () {
	me=$(basename $0)
	echo "Setup dev environment for OSX and Ubuntu" 
	echo "You need to sudo this script in Ubuntu" 
	echo "Usage: $me [arguments]" 
	echo "-bm: bootstrap for Mac" 
	echo "-bl: bootstrap for Linux/Docker" 
	echo "-v: bootstrap for Vagrant boxes" 
	echo "-p: ping all hosts defined in .ansible_hosts file" 
	echo "-d: install dotfiles" 
	echo "-u: username" 
	echo "On a fresh machine, run: $me -ba" 
}

# display usage
if [ $OPTIND -eq 1 ]; then display_usage; fi
