import re

class Stub:

	modulePattern = re.compile(r"[ \t]*module[ \t]+(\w+)")

	inputPattern = re.compile(r"[ \t]*input[ \t]+(\w+),?;?")
	sizedInputPattern = re.compile(r"[ \t]*input[ \t]*\[(.+)\][ \t]*(\w+),?;?")
	inoutPattern = re.compile(r"[ \t]*inout[ \t]*(\w+),?;?")
	sizedInoutPattern = re.compile(r"[ \t]*inout[ \t]*\[(.+)\][ \t]*(\w+),?;?")
	outputPattern = re.compile(r"[ \t]*output[ \t]*(\w+),?;?")
	sizedOutputPattern = re.compile(r"[ \t]*output[ \t]*\[(.+)\][ \t]*(\w+),?;?")
	parameterPattern = re.compile(r"[ \t]*(parameter[ \t]*.+),?;?")

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
			# find module name
			if Stub.modulePattern.match(line):
				matches = Stub.modulePattern.match(line)
				self.moduleName = matches.group(1)
				self.fileIsValid = True
			# find single bit inputs
			elif Stub.inputPattern.match(line):
				matches = Stub.inputPattern.match(line)
				portName = matches.group(1)
				newEntry = (portName)
				self.inputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			# find single bit inouts
			elif Stub.inoutPattern.match(line):
				matches = Stub.inoutPattern.match(line)
				portName = matches.group(1)
				newEntry = (portName)
				self.inoutList.append(newEntry)
				self.totalCount = self.totalCount + 1
			# find single bit outputs
			elif Stub.outputPattern.match(line):
				matches = Stub.outputPattern.match(line)
				portName = matches.group(1)
				newEntry = (portName)
				self.outputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			# find multi-bit inputs
			elif Stub.sizedInputPattern.match(line):
				matches = Stub.sizedInputPattern.match(line)
				portwidth = matches.group(1)
				portName = matches.group(2)
				newEntry = (portName, portwidth)
				self.inputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			# find multi-bit inouts
			elif Stub.sizedInoutPattern.match(line):
				matches = Stub.sizedInoutPattern.match(line)
				portwidth = matches.group(1)
				portName = matches.group(2)
				newEntry = (portName, portwidth)
				self.inoutList.append(newEntry)
				self.totalCount = self.totalCount + 1
			# find multi-bit outputs
			elif Stub.sizedOutputPattern.match(line):
				matches = Stub.sizedOutputPattern.match(line)
				portwidth = matches.group(1)
				portName = matches.group(2)
				newEntry = (portName, portwidth)
				self.outputList.append(newEntry)
				self.totalCount = self.totalCount + 1
			# find parameters
			elif Stub.parameterPattern.match(line):
				matches = Stub.parameterPattern.match(line)
				self.parameterList.append(matches.group(1))

		# sort lists
		#self.inputList.sort()
		#self.inoutList.sort()
		#self.outputList.sort()
		#self.parameterList.sort()

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
					print(entry[0] + " " + entry[1]) # sized port
				else:
					print(entry) # non-sized port
			print("INOUTS: ")
			for entry in self.inoutList:
				if not isinstance(entry, str):
					print(entry[0] + " " + entry[1]) # sized port
				else:
					print(entry) # non-sized port
			print("OUTPUTS: ")
			for entry in self.outputList:
				if not isinstance(entry, str):
					print(entry[0] + " " + entry[1]) # sized port
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

		# Start adding header io to stub
		stubFile.write("module " + self.moduleName + "\n\n(\n")
		if self.outputList:
			stubFile.write("  // OUTPUTS\n")
			for entry in self.outputList:
				if not isinstance(entry, str):
					stubFile.write("  " + entry[0]) # sized port
				else:
					stubFile.write("  " + entry) # non-sized port
				counter = counter + 1
				if counter < self.totalCount:
					stubFile.write(",\n")
				else:
					stubFile.write("\n")
		if self.inoutList:
			stubFile.write("\n  // INOUTS\n")
			for entry in self.inoutList:
				if not isinstance(entry, str):
					stubFile.write("  " + entry[0]) # sized port
				else:
					stubFile.write("  " + entry) # non-sized port
				counter = counter + 1
				if counter < self.totalCount:
					stubFile.write(",\n")
				else:
					stubFile.write("\n")
		if self.inputList:
			stubFile.write("\n  // INPUTS\n")
			for entry in self.inputList:
				if not isinstance(entry, str):
					stubFile.write("  " + entry[0]) # sized port
				else:
					stubFile.write("  " + entry) # non-sized port
				counter = counter + 1
				if counter < self.totalCount:
					stubFile.write(",\n")
				else:
					stubFile.write("\n")
		stubFile.write(");\n\n")
		# finish adding header io to stub

		# start adding parameter listing
		for entry in self.parameterList:
			stubFile.write("  " + entry + "\n")
		stubFile.write("\n")
		# finish adding parameter listing

		# start adding io direction and width
		if self.outputList:
			stubFile.write("  // OUTPUTS\n")
			for entry in self.outputList:
				if not isinstance(entry, str):
					stubFile.write("  output [" + entry[1] + "] " + entry[0]) # sized port
				else:
					stubFile.write("  output " + entry) # non-sized port
				stubFile.write(";\n")
		if self.inoutList:
			stubFile.write("\n  // INOUTS\n")
			for entry in self.inoutList:
				if not isinstance(entry, str):
					stubFile.write("  inout [" + entry[1] + "] " + entry[0]) # sized port
				else:
					stubFile.write("  inout " + entry) # non-sized port
				stubFile.write(";\n")
		if self.inputList:
			stubFile.write("\n  // INPUTS\n")
			for entry in self.inputList:
				if not isinstance(entry, str):
					stubFile.write("  input [" + entry[1] + "] " + entry[0]) # sized port
				else:
					stubFile.write("  input " + entry) # non-sized port
				stubFile.write(";\n")
		stubFile.write("\n")
		# finish adding io direction and width

		# start adding output/inout assignments
		for entry in self.outputList:
			if not isinstance(entry, str):
				stubFile.write("  assign " + entry[0] + " = 'b0;\n") # sized port
			else:
				stubFile.write("  assign " + entry + " = 1'b0;\n") # non-sized port
		for entry in self.inoutList:
			if not isinstance(entry, str):
				stubFile.write("  assign " + entry[0] + " = 'b0;\n") # sized port
			else:
				stubFile.write("  assign " + entry + " = 1'b0;\n") # non-sized port
		# finish adding output/inout assignments

		stubFile.write("\nendmodule")

	def closeFile(self):
		self.rtlFile.close()