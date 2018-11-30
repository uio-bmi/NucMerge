# copyright (c) 2018 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


import os
import sys

def INIT_FUNC(working_dir,pe1_file,pe2_file,asmb_1,asmb_2):

    cur_dir=os.getcwd()

    working_dir=os.path.abspath(working_dir)
    pe1_file=os.path.abspath(pe1_file)
    pe2_file=os.path.abspath(pe2_file)
    asmb_1=os.path.abspath(asmb_1)
    asmb_2=os.path.abspath(asmb_2)

    
    if not os.path.exists(asmb_1):
        print
        print 'ERROR: the provided fasta file with the target assembly does not exist'
        print
        sys.exit(0)

    if not os.path.exists(asmb_2):
        print
        print 'ERROR: the provided fasta file with the query assembly does not exist'
        print
        sys.exit(0)

    if not os.path.exists(pe1_file):
        print
        print 'ERROR: the provided fastq file with the first part of the reads does not exist'
        print
        sys.exit(0)

    if not os.path.exists(pe2_file):
        print
        print 'ERROR: the provided fastq file with the second part of the reads does not exist'
        print
        sys.exit(0) 


    if not os.path.exists(working_dir):
            cur_dir=os.getcwd()
            
            try:
                os.makedirs(working_dir)
            except OSError:
                print
                print 'ERROR: it is not possible to create working directory'
                print
                sys.exit(0)

    if not working_dir.endswith('/'):
        working_dir+='/'

    
        
    if not os.path.exists(working_dir+'NucDiff'):
        os.makedirs(working_dir+'NucDiff')

    if not os.path.exists(working_dir+'NucBreak_1'):
        os.makedirs(working_dir+'NucBreak_1')

    if not os.path.exists(working_dir+'NucBreak_2'):
        os.makedirs(working_dir+'NucBreak_2')

    if not os.path.exists(working_dir+'Pilon_1'):
        os.makedirs(working_dir+'Pilon_1')

    if not os.path.exists(working_dir+'Pilon_2'):
        os.makedirs(working_dir+'Pilon_2')
    
   
   
    return working_dir,pe1_file,pe2_file,asmb_1,asmb_2 
