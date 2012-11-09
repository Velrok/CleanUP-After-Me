#!/bin/bash
echo "-> installing pip, the better python package manager"
sudo easy_install pip

echo "-> installing required pyhton packages"
sudo pip install sh
sudo pip install nose
sudo pip install pinocchio