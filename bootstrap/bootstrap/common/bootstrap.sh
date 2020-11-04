[ "$UID" -eq 0 ] || exec sudo -E bash "$0" "$@"
pip3 install -r $BOOTSTRAP_COMMON_DIR/requirements.txt
