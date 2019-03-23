import json
import os
import sys
import logging

# Exceptions # 
class NoRowsError( Exception ):

    def __init__( self, value="" ):  self.value = value

    def __str__( self ):  return repr( self.value )



def  initialize( **data ):

    # Insert module paths #
    sys.path.append( os.path.join( data[ "home"], 'Database' ) )
    sys.path.append( os.path.join( data[ "home"], 'AppTemplate' ) )
    sys.path.append( os.path.join( data[ "home"], 'RuleList' ) )
    sys.path.append( os.path.join( data[ "home"], 'Command' ) )
    sys.path.append( os.path.join( data[ "home"], 'RunFileRowList' ) )
    sys.path.append( os.path.join( data[ "home"], 'AppDatabase' ) )

