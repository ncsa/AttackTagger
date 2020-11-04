#opengm library stuff
apt-get install libhdf5-serial-dev libboost-dev libboost-all-dev libboost-python-dev python-numpy doxygen -y

git clone https://github.com/opengm/opengm.git
cd opengm
git reset --hard 571e75abe66c73cc2a554e9e22563750c83509e2
cmake -DWITH_BOOST=ON -DBUILD_PYTHON_WRAPPER=ON -DWITH_HDF5=ON
make
