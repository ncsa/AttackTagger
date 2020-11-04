# change shell
# if [[ -z ${BOOTSTRAP_USER} ]]; then
# 	chsh -s /bin/zsh $BOOTSTRAP_USER
# else
# 	echo "user name is not defined"
# fi

[ "$UID" -eq 0 ] || exec sudo -E bash "$0" "$@"
if [[ -z ${BOOTSTRAP_USER} ]]; then
	echo "User name not defined for chaning shell"
	exit 1
fi

echo "Changing shell for ${BOOTSTRAP_USER}"
# chsh -s /bin/zsh $BOOTSTRAP_USER
su $BOOTSTRAP_USER
cd $HOME
echo $(whoami)
