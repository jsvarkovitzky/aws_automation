# This shell script is used within an AWS instance to begin a simulation of
# the users choice.  Results are stored locally and nohup is used so
# staying connected is not nessisary

#Jonathan Varkovitzky
#Feb 12, 2012

cd /home/ubuntu
rm -rf clawpack-4.x
rm -rf CC
git clone git://github.com/jsvarkovitzky/clawpack-4.x.git

#Set environment vars to use new clawpack
cd /home/ubuntu/clawpack-4.x
python setenv.py
source setenv.bash

#Return to home dir
cd /home/ubuntu

git clone git://github.com/jsvarkovitzky/CC.git
cp ~/keys.py /home/ubuntu/CC/.

cd /home/ubuntu/CC
#Download topo files from AWS-S3
python get_topo_s3.py 

#Begin simulation
cd /home/ubuntu/CC/simulation
nohup python runSimulation.py > nohup.out 2>&1 & 

exit

