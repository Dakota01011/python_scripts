#!/usr/bin/python

import sys, re

regPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\d+),[ \t]+\$(\d+),[ \t]+\$(\d+)")
immPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\d+),[ \t]+\$(\d+),[ \t]+(\d+)")
branchPatten = re.compile(r"[ \t]*(\w+)[ \t]+\$(\d+),[ \t]+(\d+)")
multiPatten = re.compile(r"[ \t]*(\w+)[ \t]+\$(\d+),[ \t]+\$(\d+)")
noopPatten = re.compile(r"[ \t]*noop")
memPatten = re.compile(r"[ \t]*(\w+)[ \t]+\$(\d+),[ \t]+(\d+)[ \t]*\([ \t]*\$(\d+)\)")
jumpPatten = re.compile(r"[ \t]*(\w+)[ \t]+(\d+)")

def convertToNum(instruction):
	if regPattern.match(instruction):
		matches = regPattern.match(instruction)
		instr = matches.group(1)
	elif immPattern.match(instruction):
		matches = immPattern.match(instruction)
		instr = matches.group(1)
	elif branchPattern.match(instruction):
		matches = branchPattern.match(instruction)
		instr = matches.group(1)
	elif multiPattern.match(instruction):
		matches = multiPattern.match(instruction)
		instr = matches.group(1)
	elif noopPattern.match(instruction):
		matches = noopPattern.match(instruction)
		instr = matches.group(1)
	elif memPattern.match(instruction):
		matches = memPattern.match(instruction)
		instr = matches.group(1)
	elif jumpPattern.match(instruction):
		matches = jumpPattern.match(instruction)
		instr = matches.group(1)
	return 0

programList = []
userProgName = sys.argv[1]
userProg = open(userProgName)
for line in userProg.readlines():
	value = convertToNum(line)
	programList.append(vale)
userProg.close()

outputFile = open("MIPSoutput.txt")
for entry in programList:
	outputFile.write(entry)
outputFile.close()