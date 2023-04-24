#!/usr/bin/python3
###############################################################################
#
# cnv_fixedlengthfile_2_xml_v01.pl : convert fixed length file to xml more complex
# --------------------------------------------------------------------------------
#
# system .............: aix / linux
# directory ..........: 
# programm ...........: 
# version / release ..: 0.1
# date ...............: 05.05.2015 mg version 0.1
#
# programmer .........: Marcel Gross
# departement ........: IT
#
# application group...: 
#                        
# application ........: SAP PI patops
#
# usage ..............: Usage : ${pgname} -f <file_name>  
#					                      -c <configuration_name> 
#				                          [ -o ] <output_file_name>
#					                      [ -s ] split (create a separate xml file per Record-Node)
#					                      [ -a ] create Attributes on Record-Node and Record Type Node
#					                      [ -d ] create XSD definition file
#					                      [ -v ] verbose xml output 
#
#                       example: ./cnv_fixedlengthfile_2_xml_v01.py -f FI.82731mg.txt -c FOS_FI82
#                                ./cnv_fixedlengthfile_2_xml_v01.py -f FI.82731mg.txt -c FOS_FI82
# special ............: 
#			            Log Handling Module lhm0101.pm is required
#
#
# history ............: 05.05.2015 16:26 mg
#                       base version
#
### Libraries #################################################################
#
import sys
import getopt
import io
import os
import traceback
import socket
import hashlib
#import sqlite3
#import requests
#import hashlib
#import base64
#import subprocess
#import shlex
#import uuid
#import pwd
import re
import shutil
#
from datetime  import datetime, timedelta
from time      import sleep , time
#
import xmltodict
import json
import collections
import configparser
#
import lhm0101 as lhm0101
#
### Functions #################################################################
#------------------------------------------------------------------------------ 
#
# MAIN sub : cnv_fixedlengthfile_2_xml_v01
#
#
def cnv_fixedlengthfile_2_xml_v01 (parameters):
#
    global start_time
    start_time =  time()				# Start Date + Time
    global wrklog
#
# init : variables
#
    db          = ""                                        # init db
    cursor      = ""                                        # init db cursor
    version     = 0.1                                       # Application Version
    config_file = "cnv_fixedlengthfile_2_xml_v01.py.ini"       # Application Configuration File#   
    appl_name   = "mm_CNV"          				        # Application Name
#
    PROC_id = os.getpid()				                    # Process-ID
    HOST_id = socket.gethostname()			                # Host-Name
    #print str(HOST_id)
#
# define : log file location + current python function name
#
    currentFuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name	# get current function name
    curfunc = currentFuncName()				                            # Current Function Name
    #wrklog = (sys.argv[0]) + ".log"
    wrklog = "/var/log/mm_apps/" + appl_name + "/" + os.path.basename(sys.argv[0]) + "_" + curfunc + "_" + str(PROC_id) +".log"		# work log file
    #print("Log is .: %s"   % str(wrklog)) 
    #print ("Current_Function: "  + str(curfunc))
#
# create : log header in log file
#
    try:
        lhm0101.print_log_header(wrklog,appl_name)
    except Exception as e:
        print ("LogFile can not be created.")
        print(e)
        raise (e)
#
# log : runtime python version
#
    python_version = str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro)
    if sys.version_info > (3,0) :
       #print ("python version: " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro))
       pass
    #
    statyp = "INFO"
    status = "0000"
    statxt = "python version: " + str(sys.version_info.major) + "." + str(sys.version_info.minor) + "." + str(sys.version_info.micro)
    try:
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
    except Exception as e:
        print ("LogFile can not be updated.")
        print(e)
        raise (e)
        pass
#
#
# get : parameters
#
    WRK_FILE, WRK_CONFIG, WRK_OUTPUT, WRK_SPLIT, WRK_ATTR, WRK_CREATE_XSD, WRK_VERBOSE = get_parameters (parameters)
#
# read : configuration file
#
    read_config_file(config_file, WRK_CONFIG) 				
#
#
#
# write : Log-Footer
#
    lhm0101.print_log_footer(wrklog,start_time)
#
    return()
#
#------------------------------------------------------------------------------ 
#
def read_config_file (config_file, WRK_CONFIG):
#
    config_file = "cnv_fixedlengthfile_2_xml_v01.py.json"
    with open(config_file) as f:
        data = json.load(f)
#    print(data)
#    print(data['FOS_FI82']['NAMESPACE'])
    print(data['FOS_FI82']['REC_ART'])
#    print(data['FOS_FI82']['RECORD_NAME'])
#    print(data['FOS_FI82'])
#
    return()
#
#------------------------------------------------------------------------------ 
#
# sub : read_config_file
#
def read_config_file_X (config_file, WRK_CONFIG):
#
    status = "0120"
#
    if os.path.isfile(config_file):
        statyp = "INFO "
        statxt = f"Configuration file >{config_file}< is existing."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
        statyp = "ERR-T"
        statxt = f"Configuration file >{config_file}< is not existing."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
        lhm0101.print_log_footer(wrklog,start_time)
        print(f"{statyp}:{statxt}\n", file=sys.stderr)
        exit(1)
#
    status = "0130"
    if os.access(config_file, os.R_OK):
        statyp = "INFO "
        statxt = f"Configuration file - read test of file >{config_file}< was successful."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
        statyp = "ERR-T"
        statxt = f"Configuration file - read test of file >{config_file}< is not readable."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
        lhm0101.print_log_footer(wrklog,start_time)
        print(f"{statyp}:{statxt}\n", file=sys.stderr)
        exit(1)
#
    status = "0140"
    cfg = configparser.ConfigParser( strict=False )
    try:
        cfg.read(config_file)
    except Exception as e:
        statyp = "ERR-T"
        statxt = f"Configuration file - not able to open config file >{config_file}<."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
        lhm0101.print_log_footer(wrklog,start_time)
        print(f"{statyp}:{statxt}\n", file=sys.stderr)
        raise (e)
        exit(1)
    else:
        statyp = "INFO "
        statxt = f"Configuration file - file open for ConfigParser >{config_file}< was successful."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
# check : if configuration section exists in configuration file
#
    REC_TYPE        = WRK_CONFIG
    CFG_COUNTER     = 0
#
    status = "0150"
#
    if REC_TYPE not in cfg.sections():
        statyp = "CFG-T"
        statxt = f"Configuration Section {REC_TYPE} not found in config-file - configuration error. config file >{config_file}<."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
        lhm0101.print_log_footer(wrklog,start_time)
        print(f"{statyp}:{statxt}\n", file=sys.stderr)
        exit(1)
    else:
        statyp = "INFO "
        statxt = f"Configuration Section {REC_TYPE} found in config-file >{config_file}< was successful."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
#  
# Read configuration file entry RECORD_NAME for the dedicated REC_TYPE 
#
    status = "0160"
#
    try:
        CFG_RECORD_NAME = cfg.get(REC_TYPE, 'RECORD_NAME')
    except configparser.NoOptionError:
        statyp = "CFG-T"
        statxt = f"Configuration RECORD_NAME is missing for Configuration >{REC_TYPE}< in ini-file - check failed."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
        lhm0101.print_log_footer(wrklog,start_time)
        print(f"{statyp}:{statxt}\n", file=sys.stderr)
        exit(1)
    else:
        statyp = "INFO"
        statxt = f"Configuration RECORD_NAME >{CFG_RECORD_NAME}< was found in the ini-file - check successful."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
#  
# Read configuration file entry NAMESPACE for the dedicated REC_TYPE
#
    status = "0160"
#
    try:
        CFG_NAMESPACE = cfg.get(REC_TYPE, 'NAMESPACE')
    except configparser.NoOptionError:
        statyp = "CFG-T"
        statxt = f"Configuration NAMESPACE is missing for Configuration >{REC_TYPE}< in ini-file - check failed."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
        lhm0101.print_log_footer(wrklog,start_time)
        print(f"{statyp}:{statxt}\n", file=sys.stderr)
        exit(1)
    else:
        statyp = "INFO"
        statxt = f"Configuration NAMESPACE >{CFG_NAMESPACE}< was found in the ini-file - check successful."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
#  
# Read configuration file entries REC_ART for the dedicated REC_TYPE
#
    status = "0160"
#
    try:
        CFG_REC_ARTS = cfg.get(REC_TYPE, 'REC_ART')
    except configparser.NoOptionError:
        statyp = "CFG-T"
        statxt = f"Configuration REC_ART is missing for Configuration >{REC_TYPE}< in ini-file - check failed."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
        lhm0101.print_log_footer(wrklog,start_time)
        print(f"{statyp}:{statxt}\n", file=sys.stderr)
        exit(1)
    else:
        statyp = "INFO"
        statxt = f"Configuration REC_ART >{CFG_REC_ARTS}< was found in the ini-file - check successful."
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
##
    return()
#
#------------------------------------------------------------------------------ 
#
# sub : get parameters
#
def get_parameters (argv):
#
# init : usage
#
    USAGE = "Usage : " + __file__ + " -f <file_name> -c <configuration_name> [-o <output_file_name] [-s] [-a] [-d] [-v]"
#
# Init : WRK_FILE, WRK_CONFIG, WRK_OUTPUT, WRK_SPLIT, WRK_ATTR, WRK_CREATE_XSD, WRK_VERBOSE
#
    WRK_FILE        = ""            # -f file name
    WRK_CONFIG      = ""            # -c configuration name
    WRK_OUTPUT      = ""            # -o output_file_name
    WRK_SPLIT       = ""            # -s - split (create a separate xml file per Record-Node)
    WRK_ATTR        = ""            # -a - add Attributes (on Record-Node)
    WRK_CREATE_XSD  = ""            # -d - write xsd definition file
    WRK_VERBOSE     = ""            # -v - verbose xml output
#    
    #print (argv)
    try:
       opts, args = getopt.getopt(argv,"?hf:c:o:sadv",["help","file_name=","configuration=","output_file_name=","split","add_attributes","xsd_file","verbose"])
    except getopt.GetoptError:
       print (USAGE)
       sys.exit(2)
    #print (opts)
    for opt, arg in opts:
       if opt in ("-?", "-h", "--help"):
          print (USAGE)
          sys.exit(0)
       elif opt in ("-f", "--file_name"):
          WRK_FILE = arg
       elif opt in ("-c", "--configuration"):
          WRK_CONFIG = arg
       elif opt in ("-o", "--output_file_name"):
          WRK_OUTPUT = arg
       elif opt in ("-s", "--split"):
          WRK_SPLIT = 'ON'
       elif opt in ("-a", "--add_attributes"):
          WRK_ATTR = 'ON'
       elif opt in ("-d", "--xsd_file"):
          WRK_CREATE_XSD = 'ON'
       elif opt in ("-v", "--verbose"):
          WRK_VERBOSE = 'ON'
       else: 
          print ("Unknown parameter: " + opt + " argument: " + arg)
          sys.exit(2)
#
# write : log_line with all received input parameters 
#
    status = "0010"
    statyp = "INFO"
    statxt = "input parameter: " + str(argv)
    lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
#
# check : received parameters
#
# check : Parameter -f <file_name>
#
    status = "0020"
#
    if WRK_FILE == '':
       statyp = "ERR-T"
       statxt = str('Parameter -f <file_name> is missing.')
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
       lhm0101.print_log_footer(wrklog,start_time)
       print (statxt)
       sys.exit(1)
    else:
       statyp = "INFO"
       statxt = str("Parameter -f <file_name> has the value >" + str(WRK_FILE) + "<.")
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
    status = "0030"
#
    if WRK_FILE == "-":
        statyp = "INFO "
        statxt = "Parameter -f <file> file >{}< is - will read input from <stdin>.".format(WRK_FILE)
        lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
        status = "0040"
        if os.path.isfile(WRK_FILE):
            statyp = "INFO "
            statxt = f"Parameter -f <file> file >{WRK_FILE}< is existing."
            lhm0101.print_log_line(wrklog,statyp,status,statxt)
        else:
            statyp = "ERR-T"
            statxt = f"Parameter -f <file> file >{WRK_FILE}< is not existing."
            lhm0101.print_log_line(wrklog,statyp,status,statxt)
            lhm0101.print_log_footer(wrklog,start_time)
            print(f"{statyp}:{statxt}\n", file=sys.stderr)
            exit(1)
#
        status = "0050"
        if os.access(WRK_FILE, os.R_OK):
            statyp = "INFO "
            statxt = f"Parameter -f <file> read test of file >{WRK_FILE}< was successful."
            lhm0101.print_log_line(wrklog,statyp,status,statxt)
        else:
            statyp = "ERR-T"
            statxt = f"Parameter -f <file> read test of file >{WRK_FILE}< is not readable."
            lhm0101.print_log_line(wrklog,statyp,status,statxt)
            lhm0101.print_log_footer(wrklog,start_time)
            print(f"{statyp}:{statxt}\n", file=sys.stderr)
            exit(1)
#
# check : Parameter -c <configuration>
#
    status = "0060"
#
    if WRK_CONFIG == '':
       statyp = "ERR-T"
       statxt = str('Parameter -c <configuration> is missing.')
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
       lhm0101.print_log_footer(wrklog,start_time)
       print (statxt)
       sys.exit(1)
    else:
       statyp = "INFO"
       statxt = str("Parameter -c <configuration> has the value >" + str(WRK_CONFIG) + "<.")
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
# check : Parameter -o <output_file_name>
#
    status = "0070"
#
    if WRK_OUTPUT == '':
       statyp = "INFO"
       statxt = str("Parameter -o - output file name >" + str(WRK_OUTPUT) + "< was not selected.")
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
       statyp = "INFO"
       statxt = str("Parameter -o <output_file_name> has the value >" + str(WRK_OUTPUT) + "<.")
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
# check : parameter -s - split (create a separate xml file per Record-Node)
#
    status = "0080"
    if WRK_SPLIT == "ON": 
       statyp = "INFO"
       statxt = "Parameter -s - split (create a separate xml file per Record-Node) is set: " + str(WRK_SPLIT)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
       statyp = "INFO"
       statxt = "Parameter -s - split (create a separate xml file per Record-Node) is not set. " + str(WRK_SPLIT)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
# check : -a - add Attributes (on Record-Node)
#
    status = "0090"
    if WRK_ATTR == "ON": 
       statyp = "INFO"
       statxt = "Parameter -a - add Attributes (on Record-Node) is set: " + str(WRK_ATTR)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
       statyp = "INFO"
       statxt = "Parameter -a - add Attributes (on Record-Node) is not set. " + str(WRK_ATTR)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
# check : parameter -d - write xsd definition file
#
    status = "0100"
    if WRK_CREATE_XSD == "ON": 
       statyp = "INFO"
       statxt = "Parameter -d - write xsd definition file is set: " + str(WRK_CREATE_XSD)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
       statyp = "INFO"
       statxt = "Parameter -d - write xsd definition file is not set. " + str(WRK_CREATE_XSD)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
# check : parameter -v (verbose)
#
    status = "0110"
    if WRK_VERBOSE == "ON": 
       statyp = "INFO"
       statxt = "Parameter -v for verbose is set: " + str(WRK_VERBOSE)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
    else:
       statyp = "INFO"
       statxt = "Parameter -v for verbose is not set. " + str(WRK_VERBOSE)
       lhm0101.print_log_line(wrklog,statyp,status,statxt)
#
    return (WRK_FILE, WRK_CONFIG, WRK_OUTPUT, WRK_SPLIT, WRK_ATTR, WRK_CREATE_XSD, WRK_VERBOSE)
#
#------------------------------------------------------------------------------ 
### Main Program ##############################################################
#
if __name__ == '__main__':
#
    parameters  = sys.argv[1:]
    #print ("sys.argv : " + str(sys.argv[1:]) + "\n")
    #print ("parameter: " + str(parameters) + "\n")
    cnv_fixedlengthfile_2_xml_v01 (parameters)
#
### END #######################################################################
