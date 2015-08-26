#!/pkg/.site/pkgs10/OSS-python-/3.4.1/x86_64-linux/bin/python
import os

os.system("bjobs > mybjobs.log")
print("Opening log file to read:")
logFile = open("mybjobs.log")
for line in logFile.readlines():
	print(line)
print("Closing log file...")
os.system("rm -f mybjobs.log")
