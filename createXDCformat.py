#!/pkg/.site/pkgs10/OSS-python-/3.4.1/x86_64-linux/bin/python

import sys, re

midpattern = re.compile(r"(.+)\n")
endpattern = re.compile(r"(.+)")
listFileName = sys.argv[1]
listFile = open(listFileName)
XDCFile = open("pinloc_haps70.xdc", 'w')
for line in listFile.readlines():
	if midpattern.match(line):
		matches = midpattern.match(line)
		port = matches.group(1)
		print(port)
		XDCFile.write("# \n")
		XDCFile.write("set_property PACKAGE_PIN     pin        [get_ports {" + port + "}]\n")
		XDCFile.write("set_property IOSTANDARD      LVCMOS33   [get_ports {" + port + "}]\n\n")
	elif endpattern.match(line):
		matches = endpattern.match(line)
		port = matches.group(1)
		print(port)
		XDCFile.write("# \n")
		XDCFile.write("set_property PACKAGE_PIN     pin        [get_ports {" + port + "}]\n")
		XDCFile.write("set_property IOSTANDARD      LVCMOS33   [get_ports {" + port + "}]\n\n")
	else:
		pass
XDCFile.close()
listFile.close()