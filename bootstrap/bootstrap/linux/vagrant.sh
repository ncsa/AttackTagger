# vagrant key
wget https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant \
  -O $HOME/.ssh/id_rsa
wget https://raw.githubusercontent.com/mitchellh/vagrant/master/keys/vagrant.pub \
  -O $HOME/.ssh/id_rsa.pub
chmod 600 $HOME/.ssh/*
