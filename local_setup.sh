#! /bin/sh
set -e
echo "======================================================================"
echo "Welcome to to the setup. This will setup the local virtual env." 
echo "And then it will install all the required python libraries."
echo "----------------------------------------------------------------------"
if [ -d "venv" ];
then
    echo "venv folder exists. Installing using pip"
else
    echo "creating venv and install using pip"
    pip3 install -q --upgrade pip
    pip3 install -q --upgrade virtualenv
    python3 -m virtualenv venv --python=python3.11 || (echo "ERROR in creating python3.11 virutal environment. Check if you have python 3.11 installed!!!" && exit 1)
fi

# Activate virtual env
. venv/bin/activate

# Upgrade the PIP
pip3 install --upgrade pip
pip3 install -r requirements.txt

# Work done. so deactivate the virtual env
deactivate
