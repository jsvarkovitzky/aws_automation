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
import user_info_file
user = user_info_file.user_info()

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

print "The pem key to be used is: %s" %user.pem_file
#Start a new instance
if 1:
    #Start a micro-instance
    conn.run_instances('ami-9216b3fb',key_name=user.pem_file,instance_type='m1.large',security_groups=[user.security_group])
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
driver_file = 'Driver.csv'
user_info_file = 'user_info_file.py'
topo_list = 'topo_list.csv'
#Test by scp-ing a text file to aws
print "Uploading files to instance..."

os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(key_file) + ' ubuntu@' + repr(dns) + ':.')
os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(script) + ' ubuntu@' + repr(dns) + ':.')
os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(driver_file) + ' ubuntu@' + repr(dns) + ':.')
os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(user_info_file) + ' ubuntu@' + repr(dns) + ':.')
os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(topo_list) + ' ubuntu@' + repr(dns) + ':.')
print "Executing shell script remotely..."
os.system('ssh -i ' + repr(user.pem_file) + '.pem ubuntu@' + repr(dns) + ' bash ' + repr(script) + '&')

print "You are not back on the driver instance"

