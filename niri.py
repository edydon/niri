
# py  niri.py  -r C:\Users\edydo\AppData\Local\Programs\Python\Python37-32\niri\Run_File.json  -c C:\Users\edydo\AppData\Local\Programs\Python\Python37-32\niri\Config\niri_config.json

# py  C:\Users\edydo\Documents\Python\Projects\niri\niri.py -r C:\Users\edydo\Documents\Python\Projects\niri\Run_File.json  -c C:\Users\edydo\Documents\Python\Projects\niri\Config\niri_config.json


# Load modules #
import os
import sys
from pprint  import pprint
import logging
import json
import getopt
from datetime        import date, datetime

# Get the current working directory #
cwd = os.getcwd()


###########################
# Read configuration file #
###########################
# Read arguments #
try:  opts, args = getopt.getopt( sys.argv[ 1: ], "hlr:c:s:i:d:u:",["run_file=", "config_file=", "select=", "insert=", "delete=", "update="])
except getopt.GetoptError:  print( help_msg );  sys.exit(2)


# Get the config file name #
config_file = os.path.join( cwd, "Config", "niri_config.json" )
run_file    = os.path.join( cwd, "Run_File.json" )

for opt, arg in opts:
    if opt in ("-c", "--config_file"):  config_file = arg
    if opt in ("-r", "--run_file"):     run_file    = arg

if not os.path.exists( config_file ):
    print( f"Configuration file, {config_file}, does not exit" );  sys.exit(2)



##############
# Initialize #
##############
# Read Configuration file #
with open( config_file ) as json_data_file:  data = json.load( json_data_file )


# Import module, Initialize #
sys.path.append( data[ "home" ] )

import Initialize


# Initialize system #
Initialize.initialize( **data )


######################
# Initialize logging #
######################
logger = logging.getLogger( __name__ )
logger.propagate = False

data[ "log_filename" ] = "niri_" + datetime.now().strftime('%Y-%m-%d') + '.log'


# Create logging handler #
f_handler = logging.FileHandler( os.path.join( data[ "log_area" ], data["log_filename" ] ) )
f_handler.setLevel( data[ "log_level" ] )

formatter = logging.Formatter( '%(asctime)s - %(levelname)s - %(module)s - %(message)s')


f_handler.setFormatter( formatter )


# Set up logging #
logger.setLevel( data[ "log_level" ] )
logger.addHandler( f_handler )

data[ "logger" ] = logger


########################
# Import local modules #
########################
from AppDatabase     import AppDatabase
from RunFileRowList  import RunFileRowList
from Database        import Database


from Command         import Command
from datetime        import date, datetime



def main( argv ):

    logger.debug('Starting niri')



    # Process args #
    parms = process_args( argv )



    ######################
    # Change AppDatabase #
    ######################
    if parms[ "change_flag" ]:
        try: change_AppDatabase( parms );
        except  Exception as message:  print( message );
        finally: sys.exit(0);



    ###################
    # Process RunFile #
    ###################
    # Read the Run File #
    try: app_row_list = RunFileRowList( run_file, data )
    except  Exception as message:  print( message );  sys.exit(0)



    # Read the App Database #
    try: app_db = AppDatabase( data )
    except  Exception as message:  print( message );  sys.exit(0)



    ############################
    # Loop through the RunFile #
    ############################
    return_codes = {}
    for app_row  in  app_row_list:

        # Get the App parameters #
        app_parms = app_row.get_app_data();

        print( "Running, ", app_parms[ "app_name" ] ) 
        logger.debug( "Running, " + app_parms[ "app_name" ] )


        # Get the template #
        # Source the database #
        if not app_parms[ "command_parameters" ].get( "source_name" ):
            try: template = app_db.get_app( app_parms[ "app_name" ] )[ "content" ]
            except  Exception as message:  print( message );  sys.exit(0)

        # Source a file #
        else:
            print( "Sourcing file..." )
            template_file = app_parms[ "command_parameters" ].get( "source_name" )

            if app_parms[ "command_parameters" ].get( "source_area" ):
                template_area = app_parms[ "command_parameters" ].get( "source_area" )

            else: 
                template_area = cwd


            source_file = os.path.join( template_area, template_file )
            try: template = app_db.get_app_from_file( app_parms[ "app_name" ], source_file )[ "content" ]
            except  Exception as message:  print( message );  sys.exit(0)


        # Instantiate a Command object #
        try: cmd = Command( app_parms, template, data[ "logger" ] )
        except  Exception as message:  print( message );  sys.exit(0)


        # Run the App #
        try: cmd.run();
        except  Exception as message:  print( message );  sys.exit(0)



#####################
# Process arguments #
#####################
def  process_args( argv ):

    #################
    # Get arguments #
    #################
    app_template = ''
    app_name     = ''
    outputfile   = ''

    help_msg     = """
usage:  niri  [options] 

    options:

        -h                            Display help
        -l                            Display all database Apps

        -r,  run_file=,    <Run file>       Run Apps listed in <Run file>
        -c,  config_file=, <Config file>    Sets configuration data

        -s,  select=,   <App name>    Display template for this App
        -i,  insert=,   <App file>    Insert App from <App file>
        -d,  delete=,   <App name>    Delete this App from the database
        -u,  update=,   <App file>    Update this App """

    parms = {}


    # Read arguments #
    try:  opts, args = getopt.getopt(argv,"hlr:c:s:i:d:u:",["run_file=", "config_file=", "select=", "insert=", "delete=", "update="])
    except getopt.GetoptError:  print( help_msg );  sys.exit(2)

    parms[ "change_flag" ] = 0

    # Set parameters based on arguments #
    for opt, arg in opts:

        if opt in ( "-s", "--select", "-i", "--insert", "-u", "--update", "-d", "--delete", "-l" ):
            parms[ "change_flag" ] = 1


        # Help #
        if opt == '-h':  print( help_msg );  sys.exit()


        # Insert App Template #
        elif opt in ("-i", "--insert"):    parms[ "app_template" ] = arg


        # Select App Template #
        elif opt in ("-s", "--select"):    parms[ "select_app_name" ] = arg


        # List Apps #
        elif opt in ("-l"):                parms[ "list" ] = 1


        # Select App Template #
        elif opt in ("-d", "--delete"):    parms[ "delete_app_name" ] = arg


        # Select App Template #
        elif opt in ("-u", "--update"):    parms[ "update_app_template" ] = arg

    return parms



######################
# Change AppDatabase #
######################
def  change_AppDatabase( parms ):

    ##############
    # Insert App #
    ##############
    if parms.get( "app_template" ):
        AppDatabase( cwd ).insert( parms[ "app_template" ] )
        print( "App inserted" )


    ##############
    # Select App #
    ##############
    if parms.get( "select_app_name" ):
        app = AppDatabase( cwd ).display_app( parms[ "select_app_name" ] )
     

    #############
    # List Apps #
    #############
    if parms.get( "list" ):
        app = AppDatabase( cwd ).list_apps()


    ##############
    # Delete App #
    ##############
    if parms.get( "delete_app_name" ):
        app = AppDatabase( cwd ).delete( parms[ "delete_app_name" ] )
        print( f'App, {parms[ "delete_app_name" ]}, deleted' )



    ##############
    # Update App #
    ##############
    if parms.get( "update_app_template" ):
        app = AppDatabase( cwd )

        update_app_name = app.get_name_from_file( parms[ "update_app_template" ] )

        app.delete( update_app_name )
        
        app.insert(  parms[ "update_app_template" ] )
        print( f"App, {update_app_name}, updated" )




if __name__ == '__main__':
    main( sys.argv[ 1: ] )




"""
Read Configuration file into object
	Configuration file object
		List of Configuration file rows
			Configuration file row
				Dictionary
					AppTemplate name
					Configuration row data


Loop through the Configuration file rows in proper order
	If parameter_file_name is set
		Load the template parameters into the parameter_file_name 	


	Build the script using 
		AppTemplate
		template parameters
		script_result_parameter( value(script_result_parameter) : result_value )


	If script_name is set 
		Load the generated script into script_name 	

		
	Run command
		exec_area + command_line_prefix + script + command_line_suffix

		If output_file_name is set
			Load the output into output_file_name 	

		If script_result_parameter is set
			Load the result value into dictionary,  
			script_result_parameter( value(script_result_parameter) : result_value )
"""	


