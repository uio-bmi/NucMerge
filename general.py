# copyright (c) 2018 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------



from Bio.Seq import Seq
from Bio import SeqIO

import re
import os


def natural_key(string_):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string_)]



def READ_FASTA_ENTRY(file_name):
    fasta_sequences=[]
    sequence_name=[]
    full_names_dict={}

    sequences_dict={}

    
    if os.stat(file_name)[6]!=0: #not empty
       
        fh = open(file_name, "r")
        for record in SeqIO.parse(fh, "fasta"):
            short_name=str(record.id).split(' ')[0]
            sequence_name.append(short_name)
            full_names_dict[short_name]=str(record.id)

            fasta_sequences.append(str(record.seq))
            sequences_dict[short_name]=str(record.seq)

        
    return sequences_dict, sequence_name, full_names_dict


def COMPL_STRING(line):

    my_seq = Seq(line)
    compl_line=str(my_seq.reverse_complement())

    return compl_line

def WRITE_FASTA_FILE(new_asmb_file,sequences_dict):

    f=open(new_asmb_file,'w')

    for name in sorted(sequences_dict.keys(), key=natural_key):
        f.write('>'+name+'\n')

        sequence=sequences_dict[name]

        i = 0
        while i < len(sequence):
            chunk = sequence[i:i+70]

            
            f.write(chunk + '\n')
            i = i + 70


    f.close()


def GENERATE_GFF_OUTPUT(corrected_diff_dict,working_dir, prefix,asmb_1_dict, struct_modif_dict):

    f=open(working_dir+prefix+'_local_differences.gff','w')
    f.write('##gff-version 3\n')


    so_dict={'deletion':'SO:0000159', 'collapsed_repeat':'SO:0000159', 'collapsed_tandem_repeat':'SO:0000159',
             'insertion':'SO:0000667', 'unaligned_beginning':'SO:0000667', 'unaligned_end':'SO:0000667',
             'tandem_duplication':'SO:1000173','duplication':'SO:1000035','substitution':'SO:1000002' ,
             'gap':'SO:1000002', 'inserted_gap':'SO:0000667'}

    color_dict={'deletion':'#0000EE', 'collapsed_repeat':'#0000EE', 'collapsed_tandem_repeat':'#0000EE',
             'insertion':'#EE0000', 'unaligned_beginning':'#EE0000', 'unaligned_end':'#EE0000',
             'tandem_duplication':'#EE0000','duplication':'#EE0000','substitution':'#42C042',
                'gap':'#42C042', 'inserted_gap':'#EE0000'}

    ID_cur=1
    for cont_name in sorted(corrected_diff_dict.keys(), key=natural_key):
        if not corrected_diff_dict[cont_name]==[]:
            f.write('##sequence-region\t'+cont_name+'\t1\t'+str(len(asmb_1_dict[cont_name]))+'\n')

            for err in corrected_diff_dict[cont_name]:

                if err[1]=='.':
                    old_len=0
                else:
                    old_len=len(err[1])

                if err[2]=='.':
                    new_len=0
                else:
                    new_len=len(err[2])
                    

                f.write(cont_name+'\tNucMerge_v1.0\t'+so_dict[err[0][2]]+'\t'+str(err[0][0])+'\t'+str(err[0][1])+'\t.\t.\t.\tID=LD_'+str(ID_cur)+';ID_nucdiff='+err[0][8]+';Name='+err[0][2]+\
                                            ';old_len='+str(old_len)+';new_len='+str(new_len)+';old_seq='+err[1]+';new_seq='+err[2]+';color='+color_dict[err[0][2]]+'\n')
                ID_cur+=1


    f.close()


    f=open(working_dir+prefix+'_structural_differences.gff','w')
    f.write('##gff-version 3\n')


    so_dict={'inversion':'SO:1000036', 'breakpoint':'SO:0000699'}

    color_dict={'inversion':'#EE0000','breakpoint':'#0000EE'}

    ID_cur=1
    for cont_name in sorted(struct_modif_dict.keys(), key=natural_key):
        if not struct_modif_dict[cont_name]==[]:
            f.write('##sequence-region\t'+cont_name+'\t1\t'+str(len(asmb_1_dict[cont_name]))+'\n')

            for err in struct_modif_dict[cont_name]:

                f.write(cont_name+'\tNucMerge_v1.0\t'+so_dict[err[0]]+'\t'+str(err[1])+'\t'+str(err[2])+'\t.\t.\t.\tID=SD_'+str(ID_cur)+';Name='+err[0]+';ID_nucdiff='+err[3]+';Type_nucdiff='+err[4]+\
                                            ';color='+color_dict[err[0]]+'\n')
                ID_cur+=1


    f.close()   


