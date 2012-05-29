This file contains instructions for using the automatic aws_automation repository to perform tsunami models automatically on EC2.

May 28, 2012

- Begin a micro instance with the ami ASCII-Format Geoclaw (ami-9216b3fb).
  - Select 'Launch Instance'
  - Select my AMIs -> all images -> search for ami
  - Select Mirco instance
  - Select Security Group = 'SSH-HTTPS'
  - Copy the Public DNS (ec2-xx-xx-xxx-xx.compute-1.amazonaws.com)
-Navigate to modeling folder on your personal machine to ssh to the new instance.
  - ssh onto the new intance using the command:	
  - >>ssh -i [custom].pem ubuntu@ec2-xx-xx-xxx-xx.compute-1.amazonaws.com
- Clone the code from github to ensure the newest version using:
  - >>git clone git://github.com/jsvarkovitzky/aws_automation.git
- Copy the following files to the instance into the same folder as aws_automation from your laptop:
  - keys.py
  - user_info_file.py
  - [custom].pem
  - Driver.csv
  - topo_list.py
  - To do this copy use the following command:
    - >>scp -i [custom].pem * ubuntu@ec2-xx-xx-xxx-xx.compute-1.amazonaws.com:/home/ubuntu/aws_automation/.
- Once all of these files are set up navigate to the aws_automation folder and execute the following command.
  - >>python botoConnect.py
  - At this point a new EC2 instance is started and the required files are uploaded to it.
  - Finally botoConnect.py executes a shell script that will perform the simulation automatically.
