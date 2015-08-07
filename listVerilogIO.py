#!/pkg/.site/pkgs10/OSS-python-/3.4.1/x86_64-linux/bin/python

import sys, re, xlsxwriter

modulePattern = re.compile(r" *module +(\w+)")
inputPattern = re.compile(r" *input +(\w+),?;?")
sizedInputPattern = re.compile(r" *input *\[\d+:\d+\] *(\w+),?;?")
inoutPattern = re.compile(r" *inout *(\w+),?;?")
sizedInoutPattern = re.compile(r" *inout *\[\d+:\d+\] *(\w+),?;?")
outputPattern = re.compile(r" *output *(\w+),?;?")
sizedOutputPattern = re.compile(r" *output *\[\d+:\d+\] *(\w+),?;?")
parameterPattern = re.compile(r" *parameter *(\w+),?;?")

moduleNames = ""
IOList = []

def parseFile():
	fileIsValid = False
	currentIOList = []
	for line in rtlFile.readlines():
		if modulePattern.match(line):
			fileIsValid = True
		elif inputPattern.match(line):
			matches = inputPattern.match(line)
			portName = matches.group(1)
			currentIOList.append(portName)
		elif inoutPattern.match(line):
			matches = inoutPattern.match(line)
			portName = matches.group(1)
			currentIOList.append(portName)
		elif outputPattern.match(line):
			matches = outputPattern.match(line)
			portName = matches.group(1)
			currentIOList.append(portName)
		elif sizedInputPattern.match(line):
			matches = sizedInputPattern.match(line)
			portName = matches.group(1)
			currentIOList.append(portName)
		elif sizedInoutPattern.match(line):
			matches = sizedInoutPattern.match(line)
			portName = matches.group(1)
			currentIOList.append(portName)
		elif sizedOutputPattern.match(line):
			matches = sizedOutputPattern.match(line)
			portName = matches.group(1)
			currentIOList.append(portName)

	IOList.append(currentIOList)
	return fileIsValid

def createFile():
	IOFile = open("./IOList.log", 'w')
	for filelist in IOList:
		for entry in filelist:
			IOFile.write(entry + "\n")
		IOFile.write("\n")
	IOFile.close()

if not sys.argv[1] == "-list": 
	# Single file
	rtlFileName = sys.argv[1]

	rtlFile = open(rtlFileName)
	if parseFile():
		createFile()
	else:
		print("Stub is not valid.")
	rtlFile.close()
else:
	# List of files
	listFileName = sys.argv[2]
	listFile = open(listFileName)
	for line in listFile.readlines():
		try:
			rtlFile = open(line)
		except:
			match = re.match(r"(.*)\n", line)
			rtlFile = open(match.group(1))
		if parseFile():
			createFile()
		else:
			print("Stub is not valid.")
		rtlFile.close()
	listFile.close()

	print(IOList)
