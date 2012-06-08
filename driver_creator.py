def make_driver(driverMaster,driverSub,row):
    f = open(driverMaster)
    # Opening the new file and will overwrite a preexisting version
    f1 = open(driverSub,'w')

    i = 0
    for line in f.readlines():
        if i == 0:
            print "writing the header to file"
            f1.write(line)
        if i == row:
            print "Copying run number %s to new driver file."%i
            f1.write(line)
        else:
            print "Not copying row %s to file."%i
        i = i + 1
    f1.close
    f.close
    
