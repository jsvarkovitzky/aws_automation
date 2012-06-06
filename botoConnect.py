#This program test various capabilities of the boto package for use with
#the Crescent City tsunami modeling problem

#Jonathan Varkovitzky
#May 13, 2012

#Initialize connection
from boto.ec2.connection import *
from numpy import *
from scipy.special import *
import os, subprocess
import time
import keys
import sys
import user_info_file
import csv

#Makes user specific data callable in this script
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

####################
## Start Instance ##
####################

def start_instance():
    print "The pem key to be used is: %s" %user.pem_file
    #if 1 -> New Instance, if = 0 -> use last created instance
    if 1:
        conn.run_instances('ami-9216b3fb',key_name=user.pem_file,instance_type='m1.large',security_groups=[user.security_group])
        #Brief pause to wait for instance to start up
        pause_time = 60 #seconds
        print "Pausing for %s seconds to allow instance to turn on..."%pause_time
        for i in range(0,pause_time):
            time.sleep(1)
            status(i,pause_time)

        #Retrieve information for connection
        reservations = conn.get_all_instances()
        instance = reservations[-1].instances[-1]
        dns = str(instance.public_dns_name)

        #Print relavant connection information
        print "Instance_id: %s" %(instance)
        print "DNS name: %s" %(dns)

        #Beginin uploading all relavant files to instance
        print "Uploading files to instance..."
        
        local_file_names = [key_file,script,driver_file,user_info_file,topo_list,georegion_list,tidegauge_list,fixedgrid_list]
        ec2_file_names = [key_file,script,driver_file,user_info_file,topo_list,georegion_list,tidegauge_list,fixedgrid_list]
        """
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(key_file) + ' ubuntu@' + repr(dns) + ':.')
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(script) + ' ubuntu@' + repr(dns) + ':.')
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(driver_file) + ' ubuntu@' + repr(dns) + ':.')
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(user_info_file) + ' ubuntu@' + repr(dns) + ':.')
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(topo_list) + ' ubuntu@' + repr(dns) + ':topo_list.csv')
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(georegion_list) + ' ubuntu@' + repr(dns) + ':georegion_list.csv')
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(tidegauge_list) + ' ubuntu@' + repr(dns) + ':tidegauge_list.csv')
        os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(fixedgrid_list) + ' ubuntu@' + repr(dns) + ':fixedgrid_list.csv')
        """
        for i in range(0,len(local_file_names)):
            file_uploader(local_file_names[i],ec2_file_names[i],dns)

        #Start job on new instance
        print "Executing shell script remotely..."
        command = 'ssh -i ' + str(user.pem_file) + '.pem ubuntu@' + str(dns) + " ' . " + str(script) + " &'"
        os.system(command)
        
        print "*********************************************"
        print "** You are now back on the driver instance **"
        print "*********************************************"

###################
## File Uploader ##
###################

def file_uploader(local_file_name,ec2_file_name,dns):
    os.system('scp -i ' + repr(user.pem_file) + '.pem -o StrictHostKeyChecking=no ' + repr(local_file_name) + 
              ' ubuntu@' + repr(dns) + ':' + repr(ec2_file_name))

##################
## Main Program ##
##################

#Initialize connection with EC2 using personal keys
conn = EC2Connection(keys.aws_key('access'),keys.aws_key('secret'))

#Read the Driver file to be used
driver_file = 'Driver.csv'
driver_block = genfromtxt(driver_file, dtype=None, delimiter=',', skip_header=1)

for row in driver_block:
    script = 'automateTestCase.sh'
    key_file = 'keys.py'
    user_info_file = 'user_info_file.py'
    topo_list = row[8]
    georegion_list = row[9]
    tidegauge_list = row[10]
    fixedgrid_list = row[11]
    start_instance()
    
