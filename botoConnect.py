#This program test various capabilities of the boto package for use with
#the Crescent City tsunami modeling problem

#Jonathan Varkovitzky
#May 13, 2012

#Initialize connection
from boto.ec2.connection import *
from numpy import *
from scipy.special import *
import os
import time
import keys
import sys

################                                                                
## Status Bar ##                                                                
################                                                                

def status(n,N):
    n = float(n)
    N = float(N)
    percent = n/N*100
    sys.stdout.write("[==> ]%3d%%\r" %percent)
    sys.stdout.flush()

##################
## Main Program ##
##################

#Initialize connection with EC2 using personal keys

conn = EC2Connection(keys.aws_key('access'),keys.aws_key('secret'))

#Start a new instance
if 1:
    #Start a micro-instance
    conn.run_instances('ami-9216b3fb',key_name='research',instance_type='m1.large',security_groups=['SSHHTTPAllowed'])
    #Brief pause to wait for instance to start up
    pause_time = 60
    print "Pausing for %s seconds to allow instance to turn on..."%pause_time
    for i in range(0,pause_time):
        time.sleep(1)
        status(i,pause_time)

#Retrieve information for connection
reservations = conn.get_all_instances()
instance = reservations[-1].instances[-1]
dns = str(instance.public_dns_name)

print "Instance_id:"
print(instance)
print "DNS name:"
print(dns)

script = 'automateTestCase.sh'
key_file = 'keys.py'
driver_file = 'Driver_Test.csv'
#Test by scp-ing a text file to aws
print "Uploading files to instance..."
exec('os.system("scp -i research.pem -o StrictHostKeyChecking=no %r ubuntu@%s:.")'%(key_file,dns))
exec('os.system("scp -i research.pem -o StrictHostKeyChecking=no %r ubuntu@%s:.")'%(script,dns))
exec('os.system("scp -i research.pem -o StrictHostKeyChecking=no %r ubuntu@%s:.")'%(driver_file,dns))

print "Executing shell script remotely..."
os.system("ssh -i research.pem ubuntu@%s 'bash %r' "%(dns,script))


