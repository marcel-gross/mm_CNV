#!/usr/bin/python 
#
# lhm0101.py : log_hander_module for python
# -----------------------------------------
#
### Libraries #################################################################
#
import sys
import io
import os
import socket
import subprocess
import shlex
import pwd
#
from datetime  import datetime
from time      import time, sleep, gmtime, strftime
from threading import Thread
#
### Variables #################################################################
# 
#
### Functions #################################################################
#------------------------------------------------------------------------------ 
#
# sub : print_log_header
#
def print_log_header(wrklog, appl_name):
#    sys_name         =  socket.getfqdn()	# <-very slow!
    currentFuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
#
    sys_name         =  socket.gethostname()
    pgm_name         =  os.path.basename(sys.argv[0])
    curfunc          =  currentFuncName(1)		#(current function caller is currentFuncName(1))
    pid              =  os.getpid()
    uid              =  os.getuid()
    user_name        =  pwd.getpwuid(uid)[0]
    pgm_pwd          =  os.getcwd()
    
    current_datetime = datetime.now()
    line_dashes  =  "--------------------------------------------------------------------------------\n"
    line_titel   =  "\nSYSTEM - PROGRAMM - FILE INFORMATION \n------------------------------------ \n\n"
    line_pgminfo1 =  "Program call ..................: " + pgm_name + "\n"  
    line_pgminfo2 =  "Start-Date and Time ...........: " + str(current_datetime) + "\n\n"  
    line_pgminfo3 =  "System name ...................: " + sys_name + "\n"  
    line_pgminfo4 =  "Process ID ....................: " + str(pid) + "\n"  
    line_pgminfo5 =  "User name .....................: " + user_name + "\n"  
    line_pgminfo6 =  "Working Directory .............: " + pgm_pwd + "\n"  
    line_pgminfo7 =  "Application Name ..............: " + appl_name + "\n"  
    line_pgminfo8 =  "Program Name...................: " + pgm_name + "\n"  
    line_pgminfo9 =  "Function Name..................: " + curfunc + "\n"  
    line_pgminfo10 =  "Logfile Name...................: " + wrklog   + "\n\n"  
    line_pgminfo11 = "\n"  
    try:
        File = open(wrklog, 'w') 			# Open binary output file
        File.writelines(line_dashes) 			# Write byte string
        File.writelines(line_titel) 			# Write byte string
        File.writelines(line_pgminfo1) 			# Write byte string
        File.writelines(line_pgminfo2) 			# Write byte string
        File.writelines(line_pgminfo3) 			# Write byte string
        File.writelines(line_pgminfo4) 			# Write byte string
        File.writelines(line_pgminfo5) 			# Write byte string
        File.writelines(line_pgminfo6) 			# Write byte string
        File.writelines(line_pgminfo7) 			# Write byte string
        File.writelines(line_pgminfo8) 			# Write byte string
        File.writelines(line_pgminfo9) 			# Write byte string
        File.writelines(line_pgminfo10) 		# Write byte string
        File.writelines(line_dashes) 			# Write byte string
        File.writelines(line_pgminfo11)			# Write byte string
        File.close()					#
        #os.chmod(wrklog, 33270)				# chmod to 766
    except Exception as e:
        print ("Log_Header write was not successful.")
        print(e)
        raise(e)
    return
#
#------------------------------------------------------------------------------ 
#
# sub : print_log_line
#
def print_log_line(wrklog,statyp,status,statxt):
    pgm_name =  (sys.argv[0])
    currentFuncName = lambda n=0: sys._getframe(n + 1).f_code.co_name
#    curfunc          =  currentFuncName(1) +"_"+ currentFuncName(2) +"+"+ currentFuncName(3) +"+"+ currentFuncName(4)+"+"+ currentFuncName(5)		#(current function caller is currentFuncName(1))
    curfunc          =  currentFuncName(1)
    current_datetime = datetime.now()
#    string = str(current_datetime) + ":" + statyp + ":" + pgm_name + ":" + status + ":" + statxt + "\n"
    string = str(current_datetime) + ":" + statyp + ":" + curfunc + ":" + status + ":" + statxt + "\n"
    try:
        File = open(wrklog, 'a') 			# Open binary output file
        File.writelines(string)	 			# Write byte string
        File.close()					#
    except Exception as e:
        print ("Log_Line write was not successful.")
        print(e)
        raise(e)
    return
#
#------------------------------------------------------------------------------ 
#
# sub : print_log_footer
#
def print_log_footer(wrklog,start_time):
    current_datetime = datetime.now()
    line_endtim =  "\nEnd-Date and Time: ............: " ":" + str(current_datetime) + ""  
    line_elatim =  "\nElapsed Time: .................: " ":" + str(time() - start_time) + "\n"  
    line_dashes  =  "\n--------------------------------------------------------------------------------\n\n"
    try:
        File = open(wrklog, 'a') 			# Open binary output file
        File.writelines(line_endtim) 			# Write byte string
        File.writelines(line_elatim) 			# Write byte string
        File.writelines(line_dashes) 			# Write byte string
        File.close()					#
        os.chmod(wrklog, 33270)				# chmod to 766
    except Exception as e:
        print ("Log_Footer write was not successful.")
        print(e)
        raise(e)
    return
#
### END #######################################################################
