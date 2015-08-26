#!/usr/bin/python

import sys, re
from bitstring import Bits

offsetPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w\w),[ \t]+(\d+)[ \t]*\([ \t]*\$(\w\w)\)")
reg3Pattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w\w),[ \t]+\$(\w\w),[ \t]+\$(\w\w)")
reg2Pattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w\w),[ \t]+\$(\w\w)")
reg2immPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w\w),[ \t]+\$(\w\w),[ \t]+(\d+)")
reg1Pattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w\w)")
reg1immPattern = re.compile(r"[ \t]*(\w+)[ \t]+\$(\w\w),[ \t]+(\d+)")
immPattern = re.compile(r"[ \t]*(\w+)[ \t]+(\d+)")
syscallPattern = re.compile(r"[ \t]*(\w+)")

def regNameToNumber(name):
	

def convertToNum(instruction):
	instrHex = 0
	if offsetPattern.match(instruction):
		# OP $t, offset($s)
		# ???? ??ss ssst tttt iiii iiii iiii iiii
		matches = offsetPattern.match(instruction)
		instr = matches.group(1)
		reg1 = matches.group(2)
		offset = matches.group(3)
		reg2 = matches.group(4)
		if instr == "LB": # 1000 00
			instrHex = '100000' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=offset, length=16)
		elif instr == "LW": # 1000 11
			instrHex = '100011' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=offset, length=16)
		elif instr == "SB": # 1010 00
			instrHex = '101000' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=offset, length=16)
		elif instr == "SW": # 1010 11
			instrHex = '101011' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=offset, length=16)
	elif reg3Pattern.match(instruction):
		matches = reg3Pattern.match(instruction)
		instr = matches.group(1)
		reg1 = matches.group(2)
		reg2 = matches.group(3)
		reg3 = matches.group(4)
		if instr == "ADD":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000100000'
		elif instr == "ADDU":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000100001'
		elif instr == "AND":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000100100'
		elif instr == "OR":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000100101'
		elif instr == "SLLV":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000000100'
		elif instr == "SLT":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000101010'
		elif instr == "SLTU":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000101011'
		elif instr == "SRLV":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000000110'
		elif instr == "SUB":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000100010'
		elif instr == "SUBU":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000100011'
		elif instr == "XOR":
			instrHex = '000000' + Bits(int=reg2, length=5) + Bits(int=reg3, length=5) + Bits(int=reg1, length=5) + '00000100110'
	elif reg2Pattern.match(instruction):
		matches = reg2Pattern.match(instruction)
		instr = matches.group(1)
		reg1 = matches.group(2)
		reg2 = matches.group(3)
		if instr == "DIV":
			instrHex = '000000' + Bits(int=reg1, length=5) + Bits(int=reg2, length=5) + '0000000000011010'
		elif instr == "DIVU":
			instrHex = '000000' + Bits(int=reg1, length=5) + Bits(int=reg2, length=5) + '0000000000011011'
		elif instr == "MULT":
			instrHex = '000000' + Bits(int=reg1, length=5) + Bits(int=reg2, length=5) + '0000000000011000'
		elif instr == "MULTU":
			instrHex = '000000' + Bits(int=reg1, length=5) + Bits(int=reg2, length=5) + '0000000000011001'
	elif reg2immPattern.match(instruction):
		matches = reg2immPattern.match(instruction)
		instr = matches.group(1)
		reg1 = matches.group(2)
		reg2 = matches.group(3)
		immValue = matches.group(4)
		if instr == "ADDI":
			instrHex = '001000' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=16)
		elif instr == "ADDIU":
			instrHex = '001001' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=16)
		elif instr == "ANDI":
			instrHex = '001100' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=16)
		elif instr == "BEQ":
			instrHex = '000100' + Bits(int=reg1, length=5) + Bits(int=reg2, length=5) + Bits(int=immValue, length=16)
		elif instr == "BNE":
			instrHex = '000101' + Bits(int=reg1, length=5) + Bits(int=reg2, length=5) + Bits(int=immValue, length=16)
		elif instr == "ORI":
			instrHex = '001101' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=16)
		elif instr == "SLL":
			instrHex = '000000' + '00000' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=5) + '000000'
		elif instr == "SLTI":
			instrHex = '001010' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=16)
		elif instr == "SLTIU":
			instrHex = '001011' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=16)
		elif instr == "SRA":
			instrHex = '000000' + '00000' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=5) + '000011'
		elif instr == "SRL":
			instrHex = '000000' + '00000' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=5) + '000010'
		elif instr == "XORI":
			instrHex = '001110' + Bits(int=reg2, length=5) + Bits(int=reg1, length=5) + Bits(int=immValue, length=16)
	elif reg1Pattern.match(instruction):
		matches = reg1Pattern.match(instruction)
		instr = matches.group(1)
		reg1 = matches.group(2)
		if instr == "JR":
			instrHex = '000000' + Bits(int=reg1, length=5) + '000000000000000001000'
		elif instr == "MFHI":
			instrHex = Bits(int=0, length=16) + Bits(int=reg1, length=5) + '00000010000'
		elif instr == "MFLO":
			instrHex = Bits(int=0, length=16) + Bits(int=reg1, length=5) + '00000010010'
	elif reg1immPattern.match(instruction):
		matches = reg1immPattern.match(instruction)
		instr = matches.group(1)
		reg1 = matches.group(2)
		addr = matches.group(3)
		if instr == "BGEZ":
			instrHex = '000001' + Bits(int=reg1, length=5) + '00001' + Bits(int=addr, length=16)
		elif instr == "BGEZAL":
			instrHex = '000001' + Bits(int=reg1, length=5) + '10001' + Bits(int=addr, length=16)
		elif instr == "BGTZ":
			instrHex = '000111' + Bits(int=reg1, length=5) + '00000' + Bits(int=addr, length=16)
		elif instr == "BLEZ":
			instrHex = '000110' + Bits(int=reg1, length=5) + '00000' + Bits(int=addr, length=16)
		elif instr == "BLTZ":
			instrHex = '000001' + Bits(int=reg1, length=5) + '00000' + Bits(int=addr, length=16)
		elif instr == "BLTZAL":
			instrHex = '000001' + Bits(int=reg1, length=5) + '10000' + Bits(int=addr, length=16)
		elif instr == "LUI":
			instrHex = '00111100000' + Bits(int=reg1, length=5) + Bits(int=addr, length=16)
	elif immPattern.match(instruction):
		matches = immPattern.match(instruction)
		instr = matches.group(1)
		addr = matches.group(2)
		if instr == "J":
			instrHex = '000010' + Bits(int=addr, length=26)
		elif instr == "JAL":
			instrHex = '000011' + Bits(int=addr, length=26)
	elif syscallPattern.match(instruction):
		matches = syscallPattern.match(instruction)
		instr = matches.group(1)
		if instr == "NOOP":
			instrHex = Bits(int=0, length=32)
		elif instr == "SYSCALL":
			instrHex = Bits(int=0, length=26) + '001100'
	return instrHex

programList = []
userProgName = sys.argv[1]
userProg = open(userProgName)
for line in userProg.readlines():
	value = convertToNum(line)
	Bits(int=-1, length=12)
	programList.append(vale)
userProg.close()

outputFile = open("MIPSoutput.txt")
for entry in programList:
	outputFile.write(entry)
outputFile.close()