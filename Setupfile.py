#!/pkg/.site/pkgs10/OSS-python-/3.4.1/x86_64-linux/bin/python

import sys, os, re
# ==============ULP1 Specific setup====================
## From ULP1 Project setup env scripts
LOGFILE = "SOC_QUERY.log"
PROJECT = os.environ.get('MASKNAME')
BSUB = 'bsub -K -P ' + os.environ.get('MASKNAME') + ' -G ' + os.environ.get('LSB_SUB_USER_GROUP') + ' -q normal -R rusage[mem=10000:swp=6000]'
prevlinePattern = re.compile(r" *if \{\[file exists \$\{DesignName\}_edif.xdc\]\} \{ read_xdc \$\{DesignName\}_edif.xdc \}.*")
linePattern = re.compile(r" *if \{\[file exists ../../../../constraints/pinloc_haps70.xdc\]\} \{ read_xdc ../../../../constraints/pinloc_haps70.xdc \}.*")

def clean_syn():
	print("__Deleting All Synplify Tool output files:__")
	os.system("rm -f " + LOGFILE)
	os.system("rm -rf " + os.environ.get('MASK_VERSION') + ".*/*")
	os.system("rm -f add_file.tcl")
	os.system("rm -f " + os.environ.get('MASK_VERSION') + ".prj")
	os.system("rm -f stdout.log")
	os.system("rm -f synlog.tcl")

def get_design_files():
	print("__Gathering .v and .sv files:__")
	os.system("soc -quiet query -block " + os.environ.get('SOC_TOPBLOCK') + " -bc fpga -list verilogfpgafiles > " + LOGFILE)
	print("__Gathering library directories:__")
	os.system("soc -quiet query -block " + os.environ.get('SOC_TOPBLOCK') + " -bc fpga -list veriloglibs >> " + LOGFILE)
	print("__Adding script flag & Gathering include directories")
	os.system("echo +incdir+: >> " + LOGFILE)
	os.system("soc -quiet query -block " + os.environ.get('SOC_TOPBLOCK') + " -bc fpga -list verilogfpgaincludedirs >> " + LOGFILE)
	print("__Converting design file list to synplify project format:__")
	print("  > Adding FPGA hacks needed outside of design env:")
	print("  > Outputing add_file.tcl:")
	os.system("../../../scripts/soc_query_parse " + LOGFILE)

def create_project():
	print("__Creating synplify .prj file, using add_file.tcl + project options:__")
	os.system(BSUB + " synplify_pro -batch ../../../scripts/create_proj.tcl")

def do_syn():
	print("__TOOL: Compile & Synthesize:__")
	val = os.system(BSUB + " -J " + PROJECT + "_syn synplify_pro -batch ../../../scripts/run_syn.tcl")
	return val

def hack_constraints():
	filein = open("./run_vivado_haps.tcl")
	fileout = open("./newfile.tcl", 'w')
	prevline = ""
	for line in filein.readlines():
		if prevlinePattern.match(prevline) and not linePattern.match(line):
			fileout.write("     if {[file exists ../../../../constraints/pinloc_haps70.xdc]} { read_xdc ../../../../constraints/pinloc_haps70.xdc }\n")
		fileout.write(line)
		prevline = line
	fileout.close()
	filein.close()

def do_place_and_route():
	print("__TOOL: Place & Route:__")
	os.chdir(r"ulp1_test4.haps70")
	os.system("mkdir -p ./log_files")
	hack_constraints()
	os.system("mv -f ./newfile.tcl ./run_vivado_haps.tcl")
	os.system(BSUB + " -J " + PROJECT + "_par vivado -mode batch -source ./run_vivado_haps.tcl -log log_files/vivado.log -journal log_files/vivado.jou")

try:
	option = sys.argv[1]
except:
	option = ""

if option == "new_run":
	newRunDir = sys.argv[2]
	os.system("mkdir -p RUNS/" + newRunDir)
	os.chdir(r"RUNS")
	os.chdir(newRunDir)
	os.system("mkdir synplify")
	os.system("mkdir vivado")
	os.system("mkdir identify")
elif option == "clean_syn":
	clean_syn()
elif option == "get_design_files":
	get_design_files()
elif option == "create_project":
	create_project()
elif option == "do_setup":
	clean_syn()
	get_design_files()
	create_project()
elif option == "do_instr":
	print("__TOOL: Instrument:__")
	os.system(BSUB + " -J " + PROJECT + "_instr identify_instrumentor_shell -licensetype identinstrumentor_xilinx instr.tcl")
elif option == "do_syn":
	val = do_syn()
	print("Exit code: " + repr(val))
elif option == "do_place_and_route":
	do_place_and_route()
elif option == "do_syn_and_par":
	val = do_syn()
	if not val:
		print("syn finished, continuing with par")
		do_place_and_route()
	else:
		print("syn failed")
else:
	print()
	print("----------SYNPLIFY.Makefile Targets:----------------------------------------------------------")
	print("   new_run <your_run>	=> Creates RUNS/<your_run> dir.")
	print("                          	     Creates RUNS/<your_run>/synplify dir.")
	print("                          	     Creates RUNS/<your_run>/identify dir.")
	print("                          	     Creates RUNS/<your_run>/vivado dir.")
	print("   clean_syn			=> Removes tool output files.")
	print("   get_design_files 		=> Runs soc query to gatehr design files.  Runs soc_query_parse.")
	print("   create_project		=> Creates Synplify project based on create_proj.tcl")
	print("   do_setup			=> clean syn > get_design_files > create_project")
	print("----------------------------------------------------------------------------------------------")
