# clean existing bootstrap installation
su -c "rm -rf ~/bootstrap" vagrant

# clone bootstrap repo
su -c "git clone git@bitbucket.org:pmcao/bootstrap.git" vagrant

# install
su -c "cd ~/bootstrap && ./install.sh -ba" vagrant
