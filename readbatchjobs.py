#!/pkg/.site/pkgs10/OSS-python-/3.4.1/x86_64-linux/bin/python

import os, re, smtplib, time

jobPattern = re.compile(r" *(\d+) *\w+ *(\w+) *(\w+) *\w+ *\w+-\w+ *(\w+) *(.*)")
username = 'textdakotakoelling'
password = 'textmyphone'
fromaddr = 'textdakotakoelling@gmail.com'
toaddrs  = '5127790688@txt.att.net'

prevjobdict = {}

def updateList(prevjobdict):
	jobDict = {}
	os.system("bjobs > mybjobs.log")
	logFile = open("mybjobs.log")
	for line in logFile.readlines():
		if line.find("JOBID") > -1:
			pass
		elif jobPattern.match(line):
			matches = jobPattern.match(line)
			jobid = matches.group(1)
			jobDict.update({jobid : time.time()})				
		else:
			pass
	logFile.close()
	os.system("rm -f mybjobs.log")

	keytoremove = ()
	for key in prevjobdict:
		if key not in jobDict:
			#job has finished
			jobid = key
			starttime = jobDict.get(key)
			endtime = time.time()
			print("Job finished: " + jobid)
			doneTextSend(jobid)
			keytoremove.append(key)
	for key in keytoremove:
		del prevjobdict[key]
	for key in jobDict:
		if key not in prevjobdict:
			print("adding job: " + key)
			prevjobdict.update({key: jobDict.get(key)})

def doneTextSend(process) :
    msg = ('\nDONE\nProcess: ' + str(process))
    myfile = open("message.txt", 'w')
    myfile.writelines(msg)
    myfile.close()
    os.system("sendmail " + toaddrs + " < message.txt")
    # # The actual mail send
    # print(msg)
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # print("server created")
    # server.starttls()
    # print("server started")
    # server.login(username,password)
    # print("loged in")
    # server.sendmail(fromaddr, toaddrs, msg)
    # print("mail sent")
    # server.quit()
    # print("quit")

doneTextSend("Hello")
# while True:
# 	updateList(prevjobdict)
# 	time.sleep(5) # 300 = 5 min
