#!/pkg/.site/pkgs10/OSS-python-/3.4.1/x86_64-linux/bin/python
#/usr/bin/python3

import sys, re
from Stub import Stub #First is the module (file) and second is the class

if not sys.argv[1] == "-list": 
	# Single file
	rtlFileName = sys.argv[1]

	myStub = Stub(rtlFileName)
	if myStub.parseFile():
		myStub.createFile()
	else:
		print("Stub is not valid.")
	myStub.closeFile()
else:
	# List of files
	listFileName = sys.argv[2]
	listFile = open(listFileName)
	for line in listFile.readlines():
		try:
			myStub = Stub(line)
			print(line)
		except:
			match = re.match(r"(.*)\n", line)
			myStub = Stub(match.group(1))
			print(match.group(1))
		if myStub.parseFile():
			myStub.createFile()
		else:
			print("Stub is not valid.")
		myStub.closeFile()
	listFile.close()
