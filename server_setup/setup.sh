#!/bin/bash
RED='\033[0;31m'
NC='\033[0m' # No Color
GREEN='\033[0;32m'
BLUE='\033[0;34m'
start=$(date +'%s')
pwd=`pwd`

# sudo apt-get update
# echo "============================================================================================================================================================="
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ python3.6 setup- Start ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
# sudo add-apt-repository ppa:deadsnakes/ppa   
# sudo apt-get update   
# sudo apt install python3.6

# echo "============================================================================================================================================================="
# echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ python3.6 setup- Complete ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"


printf "${BLUE}++++++++++++++++++++++++++++++++++++++++++   creating virtual env   ++++++++++++++++++++++++++++++++++++++++++\n"
# sudo apt-get install python3.6-venv python3.6-dev
cd ../../..
venv_path=`pwd`
printf "${BLUE}${venv_path}\n"

python3.6 -m venv venv_eth_2.0
cd venv_eth_2.0/bin
venv_path=`pwd`
printf "${BLUE}${venv_path}\n"
source activate
# cd $pwd
printf "${RED}++++++++++++++++++++++++++++++++++++++++++  Virtual env Complete     ++++++++++++++++++++++++++++++++++++++++++\n"

printf "${RED}++++++++++++++++++++++++++++++++++++++++++   INSTALLING DEPENEDNCYES   ++++++++++++++++++++++++++++++++++++++++++\n"

cd $pwd
pwd=`pwd`

printf "${BLUE}${pwd}"
pip install -r requirement.txt


printf "${BLUE}++++++++++++++++++++++++++++++++++++++++++   sucess   ++++++++++++++++++++++++++++++++++++++++++\n"
