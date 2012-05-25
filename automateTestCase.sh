# This shell script is used within an AWS instance to begin running the 
# Crescent City test case.  Results are stored locally and nohup is used so
# staying connected is not nessisary

#Jonathan Varkovitzky
#Feb 12, 2012

##################################################
## Remove Old Clawpack and Install New Clawpack ##
##################################################

#clawdir1
cd /home/ubuntu
rm -rf clawpack-4.x
git clone git://github.com/jsvarkovitzky/clawpack-4.x.git
#clawdir
cd /home/ubuntu/clawpack-4.x
python setenv.py
#source ~/.bashrc
source setenv.bash
#Return to home dir
cd /home/ubuntu

git clone git://github.com/jsvarkovitzky/CC.git
cp ~/keys.py /home/ubuntu/CC/.
#templatehomedir
cd /home/ubuntu/CC
python get_topo_s3.py

cd /home/ubuntu/CC/simulation

nohup time make .plots > nohup.out &
echo "Returning to driver \n"
exit