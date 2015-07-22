import re

class Stub:

	modulePattern = re.compile(r" *module +(\w+)")

	inputPattern = re.compile(r" *input +(\w+),?;?")
	sizedInputPattern = re.compile(r" *input *\[(\d+):(\d+)\] *(\w+),?;?")
	inoutPattern = re.compile(r" *inout *(\w+),?;?")
	sizedInoutPattern = re.compile(r" *inout *\[(\d+):(\d+)\] *(\w+),?;?")
	outputPattern = re.compile(r" *output *(\w+),?;?")
	sizedOutputPattern = re.compile(r" *output *\[(\d+):(\d+)\] *(\w+),?;?")
	parameterPattern = re.compile(r" *parameter *(\w+),?;?")

	def __init__(self, rtlFileName):
		self.rtlFile = open(rtlFileName)
		self.inputList = []
		self.inoutList = []
		self.outputList = []
		self.parameterList = []
		self.fileIsValid = False
		self.totalCount = 0

	def parseFile(self):
		for line in self.rtlFile.readlines():
			if Stub.modulePattern.match(line):
				matches = Stub.modulePattern.match(line)
				self.moduleName = matches.group(1)
				self.fileIsValid = True
			elif Stub.inputPattern.match(line):
				matches = Stub.inputPattern.match(line)
				portName = matches.group(1)
				newEntry = (portName)
				self.inputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			elif Stub.inoutPattern.match(line):
				matches = Stub.inoutPattern.match(line)
				portName = matches.group(1)
				newEntry = (portName)
				self.inoutList.append(newEntry)
				self.totalCount = self.totalCount + 1
			elif Stub.outputPattern.match(line):
				matches = Stub.outputPattern.match(line)
				portName = matches.group(1)
				newEntry = (portName)
				self.outputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			elif Stub.sizedInputPattern.match(line):
				matches = Stub.sizedInputPattern.match(line)
				startnum = int(matches.group(1))
				endnum = int(matches.group(2))
				portName = matches.group(3)
				newEntry = (portName, startnum, endnum)
				self.inputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			elif Stub.sizedInoutPattern.match(line):
				matches = Stub.sizedInoutPattern.match(line)
				startnum = int(matches.group(1))
				endnum = int(matches.group(2))
				portName = matches.group(3)
				newEntry = (portName, startnum, endnum)
				self.inoutList.append(newEntry)
				self.totalCount = self.totalCount + 1
			elif Stub.sizedOutputPattern.match(line):
				matches = Stub.sizedOutputPattern.match(line)
				startnum = int(matches.group(1))
				endnum = int(matches.group(2))
				portName = matches.group(3)
				newEntry = (portName, startnum, endnum)
				self.outputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			elif Stub.parameterPattern.match(line):
				matches = Stub.parameterPattern.match(line)
				self.parameterList.append(matches.group(1))

		if self.fileIsValid:
			return True
		else:
			return False

	def printIO(self):
		if self.fileIsValid:
			print("The module name is: " + self.moduleName)
			print("INPUTS: ")
			for entry in self.inputList:
				if not isinstance(entry, str):
					print(entry[0] + " " + repr(entry[1]) + " " + repr(entry[2])) # sized port
				else:
					print(entry) # non-sized port
			print("INOUTS: ")
			for entry in self.inoutList:
				if not isinstance(entry, str):
					print(entry[0] + " " + repr(entry[1]) + " " + repr(entry[2])) # sized port
				else:
					print(entry) # non-sized port
			print("OUTPUTS: ")
			for entry in self.outputList:
				if not isinstance(entry, str):
					print(entry[0] + " " + repr(entry[1]) + " " + repr(entry[2])) # sized port
				else:
					print(entry) # non-sized port
			print("PARAMETERS: ")
			for entry in self.parameterList:
				print(entry)
		else:
			print("File IO is not valid")

	def createFile(self):
		stubFile = open(self.moduleName + ".v", 'w')
		counter = 0

		if not stubFile:
			print("WARNING : Can't open output file for " + self.moduleName)
			return

		print ("Creating or Updating file " + self.moduleName + ".v")
		stubFile.write("module " + self.moduleName + "\n\n(\n")
		if self.outputList:
			stubFile.write("  // OUTPUTS\n")
			for entry in self.outputList:
				if not isinstance(entry, str):
					stubFile.write("  output [" + repr(entry[1]) + ":" + repr(entry[2]) + "] " + entry[0]) # sized port
				else:
					stubFile.write("  output " + entry) # non-sized port
				counter = counter + 1
				if counter < self.totalCount:
					stubFile.write(",\n")
				else:
					stubFile.write("\n")
		if self.inoutList:
			stubFile.write("  // INOUTS\n")
			for entry in self.inoutList:
				if not isinstance(entry, str):
					stubFile.write("  inout [" + repr(entry[1]) + ":" + repr(entry[2]) + "] " + entry[0]) # sized port
				else:
					stubFile.write("  inout " + entry) # non-sized port
				counter = counter + 1
				if counter < self.totalCount:
					stubFile.write(",\n")
				else:
					stubFile.write("\n")
		if self.inputList:
			stubFile.write("  // INPUTS\n")
			for entry in self.inputList:
				if not isinstance(entry, str):
					stubFile.write("  input [" + repr(entry[1]) + ":" + repr(entry[2]) + "] " + entry[0]) # sized port
				else:
					stubFile.write("  input " + entry) # non-sized port
				counter = counter + 1
				if counter < self.totalCount:
					stubFile.write(",\n")
				else:
					stubFile.write("\n")
		stubFile.write(");\n\n")
		for entry in self.parameterList:
			stubFile.write("  parameter " + entry + ";")
		for entry in self.outputList:
			if not isinstance(entry, str):
				if entry[1]>entry[2]:
					size = entry[1]-entry[2]+1
				else:
					size = entry[2]-entry[1]+1
				stubFile.write("  assign " + entry[0] + " = " + repr(size) + "'b0;\n") # sized port
			else:
				stubFile.write("  assign " + entry + " = 1'b0;\n") # non-sized port
		for entry in self.inoutList:
			if not isinstance(entry, str):
				if entry[1]>entry[2]:
					size = entry[1]-entry[2]+1
				else:
					size = entry[2]-entry[1]+1
				stubFile.write("  assign " + entry[0] + " = " + repr(size) + "'b0;\n") # sized port
			else:
				stubFile.write("  assign " + entry + " = 1'b0;\n") # non-sized port
		stubFile.write("\nendmodule")

	def closeFile(self):
		self.rtlFile.close()