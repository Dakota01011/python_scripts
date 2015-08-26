#!/bin/bash

echo "----------build_pop:--------------------------------------------------------------------------"
echo "   ./build_pop.py GEN_BUILD BUILD_NAME [fpga]"
echo "   GEN_BUILD                     => repo version name"
echo "   BUILD_NAME                    => local name"
echo "   [fpga]                        => optional, runs fpga hacks"
echo "----------------------------------------------------------------------------------------------"

let GEN_BUILD=$1
let BUILD_NAME=$2
let FPGA_BUILD=$3
#echo INFO:dssc pop -rec -replace ./settings
#dssc pop -rec -replace ./settings
echo INFO:./settings/bin/$GEN_BUILD $BUILD_NAME
#./settings/bin/$GEN_BUILD $BUILD_NAME
cd build
#echo INFO:source ./settings/setup_project.csh
#source ./settings/setup_project.csh
#echo INFO:source ./settings/bin/design_hacks_ulp1.csh
#source ./settings/bin/design_hacks_ulp1.csh
cd ./blocks/ulp_top/tool_data/fpga/
#pwd
#echo INFO:dssc pop -rec -replace . *
#dssc pop -rec -replace . *
if [$FPGA_BUILD = "fpga"]; then
	echo INFO:source ./scripts/fpga_hacks_ulp1.csh
	#source ./scripts/fpga_hacks_ulp1.csh
fi
