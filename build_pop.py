#!/pkg/.site/pkgs10/OSS-python-/3.4.1/x86_64-linux/bin/python

import sys, os

validcall = True
try:
	gen_build = sys.argv[1]
	build_name = sys.argv[2]
except:
	validcall = False
if validcall:
	print("INFO:dssc pop -rec -replace ./settings")
	os.system("dssc pop -rec -replace ./settings")
	print("INFO:./settings/bin/" + gen_build + " " + build_name)
	os.system("./settings/bin/" + gen_build + " " + build_name)
	os.chdir(r"build")
	# ------source does not work --------
	print("INFO:source ./settings/setup_project.csh")
	os.system("source ./settings/setup_project.csh")
	print("INFO:source ./settings/bin/design_hacks_ulp1.csh")
	os.system("source ./settings/bin/design_hacks_ulp1.csh")
	# ------source does not work --------
	os.chdir(r"blocks")
	os.chdir(r"ulp_top")
	os.chdir(r"tool_data")
	os.chdir(r"fpga")
	print(os.getcwd())
	print("INFO:dssc pop -rec -replace . *")
	os.system("dssc pop -rec -replace . *")
	try:
		fpga_build = sys.argv[3]
	except:
		fpga_build = ""
	if fpga_build == "fpga":
		# ------source does not work --------
		print("INFO:source ./scripts/fpga_hacks_ulp1.csh")
		os.system("source ./scripts/fpga_hacks_ulp1.csh")
		# ------source does not work --------
else:
	print()
	print("----------build_pop:--------------------------------------------------------------------------")
	print("   ./build_pop.py gen_build build_name [fpga]")
	print("   gen_build                     => repo version name")
	print("   build_name                    => local name")
	print("   [fpga]                        => optional, runs fpga hacks")
	print("----------------------------------------------------------------------------------------------")
