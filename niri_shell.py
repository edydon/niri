
# py  niri_shell.py  -r C:\Users\edydo\AppData\Local\Programs\Python\Python37-32\niri\Run_File.json  -c C:\Users\edydo\AppData\Local\Programs\Python\Python37-32\niri\Config\niri_config.json

# py  C:\Users\edydo\Documents\Python\Projects\niri\niri_shell.py -r C:\Users\edydo\Documents\Python\Projects\niri\Run_File.json  -c C:\Users\edydo\Documents\Python\Projects\niri\Config\niri_config.json


# Load modules #
import os
import sys
from pprint  import pprint
import logging
import json
import getopt
from datetime        import date, datetime
import subprocess

# Get the current working directory #
cwd = os.getcwd()



##################
# Read arguments #
##################
try:  opts, args = getopt.getopt( sys.argv[ 1: ], "hlr:c:s:i:d:u:",["run_file=", "config_file=", "select=", "insert=", "delete=", "update="])
except getopt.GetoptError:  print( help_msg );  sys.exit(2)



##############################
# Get the configuration file #
##############################
config_file = os.path.join( cwd, "Config", "niri_config.json" )
for opt, arg in opts:
    if opt in ("-c", "--config_file"):  config_file = arg


if not os.path.exists( config_file ):
    print( f"Configuration file, {config_file}, does not exit" );  sys.exit(2)



###########################
# Read Configuration file #
###########################
with open( config_file ) as json_data_file:  data = json.load( json_data_file )



########################
# Check for a run file #
########################
run_file    = os.path.join( cwd, "Run_File.json" )
if not run_file:  run_file = os.path.join( data[ "home" ], "Run_File.json" )
for opt, arg in opts:
    if opt in ("-r", "--run_file"):     run_file    = arg



#################
# Build command #
#################
command = []
command.append( os.path.join( data[ "home" ], "niri.exe" ) )

if run_file:     command.append( "-r" );  command.append( run_file )
if config_file:  command.append( "-c" );  command.append( config_file )

for opt, arg in opts:
    if opt not in ("-c", "--config_file", "-r", "--run_file" ):
        if opt: command.append( opt )        

        if arg: command.append( arg )        



print( command )

############
# Run niri #
############

# Change area #
os.chdir( data[ "home" ] )


# Run the command #  
try:    output = subprocess.check_output( command, universal_newlines=True );
except  Exception as err:  print( str(err) );  sys.exit();

        
print( output )
 

# Return to starting area #
os.chdir( cwd )


