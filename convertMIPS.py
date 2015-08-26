#!/usr/bin/python3

import sys, re
from bitstring import Bits

offsetPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w+),[ \t]+(\d+)[ \t]*\([ \t]*\$(\w+)\)")
reg3Pattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w+),[ \t]+\$(\w+),[ \t]+\$(\w+)")
reg2immPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w+),[ \t]+\$(\w+),[ \t]+(-?\d+)")
reg2Pattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w+),[ \t]+\$(\w+)")
reg1Pattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w+)")
reg1immPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w+),[ \t]+(-?\d+)")
immPattern = re.compile(r"[ \t]*(\w+)[ \t]+(-?\d+)")
syscallPattern = re.compile(r"[ \t]*(\w+)")
regLookupTable = {'zero':0, 'at':1, 'v0':2, 'v1':3, 'a0':4, 'a1':5, 'a2':6, 'a3':7, 't0':8, 't1':9, 't2':10, 't3':11, 't4':12, 't5':13, 't6':14, 't7':15, 's0':16, 's1':17, 's2':18, 's3':19, 's4':20, 's5':21, 's6':22, 's7':23, 't8':24, 't9':25, 'k0':26, 'k1':27, 'gp':28, 'sp':29, 'fp':30, 'ra':31}

def regNameToNumber(name):
	if name in regLookupTable:
		regNumber = regLookupTable[name]
	else:
		regNumber = int(name)
	return regNumber

def convertToNum(instruction):
	instrHex = -1
	if offsetPattern.match(instruction):
		# OP $t, offset($s)
		# ???? ??ss ssst tttt iiii iiii iiii iiii
		matches = offsetPattern.match(instruction)
		instr = matches.group(1)
		reg1 = regNameToNumber(matches.group(2))
		offset = int(matches.group(3))
		reg2 = regNameToNumber(matches.group(4))
		num1 = Bits(uint=reg1, length=5)
		num2 = Bits(uint=reg2, length=5)
		num3 = Bits(int=offset, length=16)
		if instr.lower() == "LB".lower(): # 1000 00
			#instrHex = '100000' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=offset, length=16)
			instrHex = Bits().join(['0b100000', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=offset, length=16)])
		elif instr.lower() == "LW".lower(): # 1000 11
			#instrHex = '100011' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=offset, length=16)
			instrHex = Bits().join(['0b100011', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=offset, length=16)])
		elif instr.lower() == "SB".lower(): # 1010 00
			#instrHex = '101000' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=offset, length=16)
			instrHex = Bits().join(['0b101000', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=offset, length=16)])
		elif instr.lower() == "SW".lower(): # 1010 11
			#instrHex = '101011' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=offset, length=16)
			instrHex = Bits().join(['0b101011', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=offset, length=16)])
	elif reg3Pattern.match(instruction):
		matches = reg3Pattern.match(instruction)
		instr = matches.group(1)
		reg1 = regNameToNumber(matches.group(2))
		reg2 = regNameToNumber(matches.group(3))
		reg3 = regNameToNumber(matches.group(4))
		if instr.lower() == "ADD".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000100000'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000100000'])
		elif instr.lower() == "ADDU".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000100001'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000100001'])
		elif instr.lower() == "AND".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000100100'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000100100'])
		elif instr.lower() == "OR".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000100101'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000100101'])
		elif instr.lower() == "SLLV".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000000100'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000000100'])
		elif instr.lower() == "SLT".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000101010'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000101010'])
		elif instr.lower() == "SLTU".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000101011'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000101011'])
		elif instr.lower() == "SRLV".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000000110'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000000110'])
		elif instr.lower() == "SUB".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000100010'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000100010'])
		elif instr.lower() == "SUBU".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000100011'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000100011'])
		elif instr.lower() == "XOR".lower():
			#instrHex = '000000' + Bits(uint=reg2, length=5) + Bits(uint=reg3, length=5) + Bits(uint=reg1, length=5) + '00000100110'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg2, length=5), Bits(uint=reg3, length=5), Bits(uint=reg1, length=5), '0b00000100110'])
	elif reg2immPattern.match(instruction):
		matches = reg2immPattern.match(instruction)
		instr = matches.group(1)
		reg1 = regNameToNumber(matches.group(2))
		reg2 = regNameToNumber(matches.group(3))
		immValue = int(matches.group(4))
		if instr.lower() == "ADDI".lower():
			#instrHex = '001000' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b001000', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "ADDIU".lower():
			#instrHex = '001001' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b001001', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "ANDI".lower():
			#instrHex = '001100' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b001100', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "BEQ".lower():
			#instrHex = '000100' + Bits(uint=reg1, length=5) + Bits(uint=reg2, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b000100', Bits(uint=reg1, length=5), Bits(uint=reg2, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "BNE".lower():
			#instrHex = '000101' + Bits(uint=reg1, length=5) + Bits(uint=reg2, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b000101', Bits(uint=reg1, length=5), Bits(uint=reg2, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "ORI".lower():
			#instrHex = '001101' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b001101', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "SLL".lower():
			#instrHex = '000000' + '00000' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=5) + '000000'
			instrHex = Bits().join([Bits(uint=0, length=11), Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=5), '0b000000'])
		elif instr.lower() == "SLTI".lower():
			#instrHex = '001010' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b001010', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "SLTIU".lower():
			#instrHex = '001011' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b001011', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=16)])
		elif instr.lower() == "SRA".lower():
			#instrHex = '000000' + '00000' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=5) + '000011'
			instrHex = Bits().join([Bits(uint=0, length=11), Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=5), '0b000011'])
		elif instr.lower() == "SRL".lower():
			#instrHex = '000000' + '00000' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=5) + '000010'
			instrHex = Bits().join([Bits(uint=0, length=11), Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=5), '0b000010'])
		elif instr.lower() == "XORI".lower():
			#instrHex = '001110' + Bits(uint=reg2, length=5) + Bits(uint=reg1, length=5) + Bits(int=immValue, length=16)
			instrHex = Bits().join(['0b001110', Bits(uint=reg2, length=5), Bits(uint=reg1, length=5), Bits(int=immValue, length=16)])
	elif reg2Pattern.match(instruction):
		matches = reg2Pattern.match(instruction)
		instr = matches.group(1)
		reg1 = regNameToNumber(matches.group(2))
		reg2 = regNameToNumber(matches.group(3))
		if instr.lower() == "DIV".lower():
			#instrHex = '000000' + Bits(uint=reg1, length=5) + Bits(uint=reg2, length=5) + '0000000000011010'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg1, length=5), Bits(uint=reg2, length=5), '0b0000000000011010'])
		elif instr.lower() == "DIVU".lower():
			#instrHex = '000000' + Bits(uint=reg1, length=5) + Bits(uint=reg2, length=5) + '0000000000011011'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg1, length=5), Bits(uint=reg2, length=5), '0b0000000000011011'])
		elif instr.lower() == "MULT".lower():
			#instrHex = '000000' + Bits(uint=reg1, length=5) + Bits(uint=reg2, length=5) + '0000000000011000'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg1, length=5), Bits(uint=reg2, length=5), '0b0000000000011000'])
		elif instr.lower() == "MULTU".lower():
			#instrHex = '000000' + Bits(uint=reg1, length=5) + Bits(uint=reg2, length=5) + '0000000000011001'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg1, length=5), Bits(uint=reg2, length=5), '0b0000000000011001'])
	elif reg1Pattern.match(instruction):
		matches = reg1Pattern.match(instruction)
		instr = matches.group(1)
		reg1 = regNameToNumber(matches.group(2))
		if instr.lower() == "JR".lower():


			#instrHex = '000000' + Bits(uint=reg1, length=5) + '000000000000000001000'
			instrHex = Bits().join([Bits(uint=0, length=6), Bits(uint=reg1, length=5), '0b000000000000000001000'])
		elif instr.lower() == "MFHI".lower():
			#instrHex = Bits(int=0, length=16) + Bits(uint=reg1, length=5) + '00000010000'
			instrHex = Bits().join([Bits(uint=0, length=16), Bits(uint=reg1, length=5), '0b00000010000'])
		elif instr.lower() == "MFLO".lower():
			#instrHex = Bits(int=0, length=16) + Bits(uint=reg1, length=5) + '00000010010'
			instrHex = Bits().join([Bits(uint=0, length=16), Bits(uint=reg1, length=5), '0b00000010010'])
	elif reg1immPattern.match(instruction):
		matches = reg1immPattern.match(instruction)
		instr = matches.group(1)
		reg1 = regNameToNumber(matches.group(2))
		addr = int(matches.group(3))
		if instr.lower() == "BGEZ".lower():
			#instrHex = '000001' + Bits(uint=reg1, length=5) + '00001' + Bits(int=addr, length=16)
			instrHex = Bits().join(['0b000001', Bits(uint=reg1, length=5), '0b00001', Bits(int=addr, length=16)])
		elif instr.lower() == "BGEZAL".lower():
			#instrHex = '000001' + Bits(uint=reg1, length=5) + '10001' + Bits(int=addr, length=16)
			instrHex = Bits().join(['0b000001', Bits(uint=reg1, length=5), '0b10001', Bits(int=addr, length=16)])
		elif instr.lower() == "BGTZ".lower():
			#instrHex = '000111' + Bits(uint=reg1, length=5) + '00000' + Bits(int=addr, length=16)
			instrHex = Bits().join(['0b000111', Bits(uint=reg1, length=5), '0b00000', Bits(int=addr, length=16)])
		elif instr.lower() == "BLEZ".lower():
			#instrHex = '000110' + Bits(uint=reg1, length=5) + '00000' + Bits(int=addr, length=16)
			instrHex = Bits().join(['0b000110', Bits(uint=reg1, length=5), '0b00000', Bits(int=addr, length=16)])
		elif instr.lower() == "BLTZ".lower():
			#instrHex = '000001' + Bits(uint=reg1, length=5) + '00000' + Bits(int=addr, length=16)
			instrHex = Bits().join(['0b000001', Bits(uint=reg1, length=5), '0b00000', Bits(int=addr, length=16)])
		elif instr.lower() == "BLTZAL".lower():
			#instrHex = '000001' + Bits(uint=reg1, length=5) + '10000' + Bits(int=addr, length=16)
			instrHex = Bits().join(['0b000001', Bits(uint=reg1, length=5), '0b10000', Bits(int=addr, length=16)])
		elif instr.lower() == "LUI".lower():
			#instrHex = '00111100000' + Bits(uint=reg1, length=5) + Bits(int=addr, length=16)
			instrHex = Bits().join(['0b00111100000', Bits(uint=reg1, length=5), Bits(int=addr, length=16)])
	elif immPattern.match(instruction):
		matches = immPattern.match(instruction)
		instr = matches.group(1)
		addr = int(matches.group(2))
		if instr.lower() == "J".lower():
			#instrHex = '000010' + Bits(int=addr, length=26)
			instrHex = Bits().join(['0b000010', Bits(int=addr, length=26)])
		elif instr.lower() == "JAL".lower():
			#instrHex = '000011' + Bits(int=addr, length=26)
			instrHex = Bits().join(['0b000011', Bits(int=addr, length=26)])
	elif syscallPattern.match(instruction):
		matches = syscallPattern.match(instruction)
		instr = matches.group(1)
		if instr.lower() == "NOOP".lower():
			#instrHex = Bits(int=0, length=32)
			instrHex = Bits().join([Bits(int=0, length=32)])
		elif instr.lower() == "SYSCALL".lower():
			#instrHex = Bits(int=0, length=26) + '001100'
			instrHex = Bits().join([Bits(int=addr, length=26), '0b001100'])
	return instrHex

def extractFromProgramFile(userProgName):
	instructionList = []
	userProg = open(userProgName)
	for line in userProg.readlines():
		value = convertToNum(line)
		if not type(value) == int:
			instructionList.append(value)
	userProg.close()
	return instructionList

def groupInstructions(instructionList):
	programList = []
	while len(instructionList) >= 8:
		programList.append(str(instructionList[7]).split('x')[1]+str(instructionList[6]).split('x')[1]+str(instructionList[5]).split('x')[1]+str(instructionList[4]).split('x')[1]+str(instructionList[3]).split('x')[1]+str(instructionList[2]).split('x')[1]+str(instructionList[1]).split('x')[1]+str(instructionList[0]).split('x')[1])
		del instructionList[0:8] # deletes 0-7 not 8
	instructionList.reverse()
	lastline = ""
	for i in range(8-len(instructionList)):
		lastline += "00000000"
	for entry in instructionList:
		lastline += str(entry).split('x')[1]
	programList.append(lastline)
	return programList

def writeOutputFile(programList):
	#from 00 to 7F
	#64 hex per line
	#8 instr per line
	#.INIT_00(256'h0000),
	outputFile = open("MIPSoutput.txt", 'w')
	number = 0
	for entry in programList:
		hexstring = str(Bits(int=number, length=8)).split('x')[1]
		outputFile.write(".INIT_" + hexstring + "(256'h" + entry + "),\n")
		number = number + 1
	while number < 0x80:
		hexstring = str(Bits(int=number, length=8)).split('x')[1]
		outputFile.write(".INIT_" + hexstring + "(256'h" + str(Bits(int=0, length=256)).split('x')[1] + "),\n")
		number = number + 1
	outputFile.close()

userProgName = sys.argv[1]
instructionList = extractFromProgramFile(userProgName)
programList = groupInstructions(instructionList)
writeOutputFile(programList)