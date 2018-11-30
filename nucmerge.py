# copyright (c) 2018 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------

import sys
import argparse
import os
import shutil

import init
import run_tools
import general
import error_correction







def START(args):
    
    asmb_1=args['asmb_target']
    asmb_2=args['asmb_query']

    pe1_file=args['pe1_file']
    pe2_file=args['pe2_file']

    working_dir=args['working_dir']
    prefix=args['prefix']

    p_num=args['proc']

    

    nucdiff_dir=os.path.abspath(sys.argv[0].split('nucmerge')[0])+'/NucDiff/nucdiff/'
    nucbreak_dir=os.path.abspath(sys.argv[0].split('nucmerge')[0])+'/NucBreak/'

    asmb_1_dict, asmb_1_name_list, asmb_1_full_names_dict=general.READ_FASTA_ENTRY(asmb_1)
    asmb_2_dict, asmb_2_name_list, asmb_2_full_names_dict=general.READ_FASTA_ENTRY(asmb_2)

    working_dir,pe1_file,pe2_file,asmb_1,asmb_2=init.INIT_FUNC(working_dir,pe1_file,pe2_file,asmb_1,asmb_2)

    nucbreak_1_dict, nucbreak_2_dict, pilon_local_1_dict, pilon_local_2_dict, local_1_dict,struct_1_dict=run_tools.RUN_PARSE_TOOLS(working_dir,pe1_file,pe2_file,asmb_1,asmb_2,prefix, p_num, asmb_1_dict, asmb_2_dict, nucdiff_dir, nucbreak_dir)

    error_correction.CORRECT_ERRORS(nucbreak_1_dict, nucbreak_2_dict, pilon_local_1_dict, pilon_local_2_dict, local_1_dict,struct_1_dict,asmb_1_dict, asmb_2_dict, asmb_1_name_list,  working_dir,prefix)
    







#-------------------------------------------------------------
def main():
    
    argv=sys.argv
    parser = argparse.ArgumentParser()

    parser.add_argument('asmb_target',metavar='Target_assembly.fasta', type=str, help='- Fasta file with the target assembly')
    parser.add_argument('asmb_query',metavar='Query_assembly.fasta', type=str, help='- Fasta file with the query assembly')
    parser.add_argument('pe1_file',metavar='PE_reads_1.fastq', type=str, help='- Fastq file with the first part of paired-end reads. They are supposed to be forward-oriented.')
    parser.add_argument('pe2_file',metavar='PE_reads_2.fastq', type=str, help='- Fastq file with the second part of paired-end reads. They are supposed to be reverse-oriented.')
    parser.add_argument('working_dir',metavar='Output_dir', type=str, help='- Path to the directory where all intermediate and final results will be stored')
    parser.add_argument('prefix',metavar='Prefix', type=str, help='- Name that will be added to all generated files')
    parser.add_argument('--proc', metavar='int', type=int, nargs='?',default=1, help='- Number of processes to be used. It is advised to use 5 processes. [5] ')
    parser.add_argument('--version', action='version', version='NucMerge version 1.0.0')
    
    args=vars(parser.parse_args())

    START(args)

main()
