This file contains instructions for using the automatic aws_automation repository to perform tsunami models automatically on EC2.

May 28, 2012

- Begin a micro instance with the ami ASCII-Format Geoclaw (ami-9216b3fb).
  - Be sure to allow ssh and https connectivity to allow for access to user and other instances.
- Clone the code from github to ensure the newest version using:
  - >>git clone git@github.com:jsvarkovitzky/aws_automation.git
- Copy the following files to the instance into the same folder as aws_automation:
  - keys.py
  - user_info_file.py
  - [custom].pem
  - Driver.csv
  - topo_list.py
- Once all of these files are set up navigate to the aws_automation folder and execute the following command.
  - >>python botoConnect.py
  - At this point a new EC2 instance is started and the required files are uploaded to it.
  - Finally botoConnect.py executes a shell script that will perform the simulation automatically.
