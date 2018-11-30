# copyright (c) 2018 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------


from multiprocessing import Pool
import subprocess
import os


import general



#---------------------------------------------------------------------------------------------------------------        
        
def RUN_NUCDIFF(asmb_1, asmb_2, working_dir, prefix, nucdiff_dir):

    subprocess.call(['nucdiff', asmb_1,asmb_2, working_dir,prefix ])

      

def RUN_NUCBREAK(asmb, pe1_file, pe2_file, working_dir, prefix, nucbreak_dir):

    subprocess.call(['python', nucbreak_dir+'nucbreak.py', asmb, pe1_file, pe2_file, working_dir,prefix ])



def RUN_BWA(work_dir, prefix, assembly, PE_reads_1, PE_reads_2):
    
    subprocess.check_call(['bwa','index', '-p', work_dir+prefix, assembly])
    f=open( work_dir + prefix+'_all.sam','w')
    subprocess.check_call(['bwa','mem','-R', '@RG\tID:id\tSM:sample\tLB:lib', work_dir+prefix, PE_reads_1,PE_reads_2],stdout=f )
    f.close()

    f=open(work_dir+prefix+'_all.bam','w')
    subprocess.call(['samtools', 'view', '-Sb',  work_dir+prefix+'_all.sam'],stdout=f )
    f.close()
    subprocess.call(['samtools', 'sort',work_dir+prefix+'_all.bam', '-o', work_dir+prefix+'_all_sorted.bam']) 
    subprocess.call(['samtools', 'index', work_dir+prefix+'_all_sorted.bam', work_dir+prefix+'_all_sorted.bai'])

    return work_dir+prefix+'_all_sorted.bam'



def RUN_PILON(asmb_file, pe_1_file, pe_2_file, working_dir, prefix):

    if not os.path.exists(working_dir+'bwa'):
        os.makedirs(working_dir+'bwa')

    pe_bam_all=RUN_BWA(working_dir+'bwa/', prefix, asmb_file, pe_1_file, pe_2_file)

    f=open(working_dir+prefix+'.out','w')
    subprocess.check_call(['pilon','--genome',asmb_file,'--frags', pe_bam_all, '--output', prefix, '--outdir', working_dir, '--changes', '--fix','all,breaks'],stdout=f )
    f.close()
    


#-----------------------------------------------------------------------------------------------------
def PARSE_NUCBREAK(file_1,asmb_dict):
    break_1_dict={}

    for cont_name in asmb_dict.keys():
        break_1_dict[cont_name]=[]
    

    f=open(file_1)

    line=f.readline()
    line=f.readline()

    while line:
        temp=line[:-1].split()
        cont_name=temp[0]
        cont_st=int(temp[1])
        cont_end=int(temp[2])

        break_1_dict[cont_name].append([cont_st, cont_end])
        
        
        line=f.readline()

    f.close()

 

    return break_1_dict

#--------------------------------------------------------------------------------------------------------
def PARSE_NUCDIFF(file_prefix, asmb_dict):

    struct_dict={}
    local_dict={}

    for cont_name in asmb_dict.keys():
        struct_dict[cont_name]=[]
        local_dict[cont_name]=[]

    
    f=open(file_prefix+'_query_snps.gff')
    line=f.readline()
    line=f.readline()

    while line:
        if not line.startswith('##sequence-region'):
            temp=line[:-1].split()
            cont_name=temp[0]
            cont_st=int(temp[3])
            cont_end=int(temp[4])

            tmp=temp[8].split(';')
            err_len=int(tmp[2].split('=')[1])
            cont_dir=int(tmp[3].split('=')[1])
            ref_name=tmp[4].split('=')[1]

            if '-' in tmp[5].split('=')[1]:
                ref_st=int(tmp[5].split('=')[1].split('-')[0])
                ref_end=int(tmp[5].split('=')[1].split('-')[1])
            else:
                ref_st=int(tmp[5].split('=')[1])
                ref_end=int(tmp[5].split('=')[1])

            
            if tmp[1].split('=')[1] in ['substitution', 'gap']:
                if cont_dir==1:
                    ref_i=ref_st
                    for i in range(cont_st, cont_end+1):
                        local_dict[cont_name].append([i, i,tmp[1].split('=')[1],1, cont_dir, ref_name, ref_i,ref_i,tmp[0].split('=')[1] ])
                        ref_i+=1
                else:
                    ref_i=ref_end
                    for i in range(cont_st, cont_end+1):
                        local_dict[cont_name].append([i, i,tmp[1].split('=')[1],1, cont_dir, ref_name, ref_i,ref_i,tmp[0].split('=')[1] ])
                        ref_i-=1

            elif tmp[1].split('=')[1] in ['insertion','deletion', 'inserted_gap']:
                if local_dict[cont_name]!=[]:
                    if local_dict[cont_name][-1][0]==cont_st and local_dict[cont_name][-1][0]==cont_end:
                        if local_dict[cont_name][-1][5]==ref_name:
                             local_dict[cont_name].append([cont_st, cont_end,tmp[1].split('=')[1],err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])

                    else:
                        local_dict[cont_name].append([cont_st, cont_end,tmp[1].split('=')[1],err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])
                else:
                        local_dict[cont_name].append([cont_st, cont_end,tmp[1].split('=')[1],err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])
            
           
        line=f.readline()

    f.close()
    
    
    f=open(file_prefix+'_query_struct.gff')
    line=f.readline()
    line=f.readline()

    while line:
        if not line.startswith('##sequence-region'):
            temp=line[:-1].split()

            cont_name=temp[0]
            cont_st=int(temp[3])
            cont_end=int(temp[4])

            tmp=temp[8].split(';')
            
            if tmp[1].split('=')[1] in ['insertion','duplication','deletion','collapsed_repeat', 'tandem_duplication','collapsed_tandem_repeat', 'gap', 'inserted_gap', 'substitution']:
                                        
                diff_type=tmp[1].split('=')[1]
                
                cont_dir=int(tmp[3].split('=')[1])
                ref_name=tmp[4].split('=')[1]

                if not ( '-' in tmp[5].split('=')[1]):
                    ref_st=int(tmp[5].split('=')[1])
                    ref_end=int(tmp[5].split('=')[1])
                else:
                    ref_st=int(tmp[5].split('=')[1].split('-')[0])
                    ref_end=int(tmp[5].split('=')[1].split('-')[1])

                err_len=int(tmp[2].split('=')[1])

                if diff_type in ['collapsed_repeat']:
                   
                    if local_dict[cont_name]!=[]:
                        if local_dict[cont_name][-1][0]==cont_st and local_dict[cont_name][-1][1]==cont_end and local_dict[cont_name][-1][2]=='deletion' and local_dict[cont_name][-1][5]==ref_name :
                            if cont_dir==1 and local_dict[cont_name][-1][7]==ref_st-1:
                                local_dict[cont_name][-1][8]=local_dict[cont_name][-1][8]+'_'+tmp[0].split('=')[1]+'_'+str(local_dict[cont_name][-1][3])+'_'+str(err_len)+'_'+str(local_dict[cont_name][-1][6])+'_'+str(local_dict[cont_name][-1][7])
                                local_dict[cont_name][-1][7]=ref_end
                                local_dict[cont_name][-1][3]+=err_len
                                if err_len>16:
                                    local_dict[cont_name][-1][2]='collapsed_repeat'
                                
                            elif cont_dir==-1 and local_dict[cont_name][-1][6]==ref_end+1:
                                local_dict[cont_name][-1][8]=local_dict[cont_name][-1][8]+'_'+tmp[0].split('=')[1]+'_'+str(local_dict[cont_name][-1][3])+'_'+str(err_len)+'_'+str(local_dict[cont_name][-1][6])+'_'+str(local_dict[cont_name][-1][7])
                                local_dict[cont_name][-1][6]=ref_st
                                local_dict[cont_name][-1][3]+=err_len
                                if err_len>16:
                                    local_dict[cont_name][-1][2]='collapsed_repeat'
                            else:
                                
                                local_dict[cont_name].append([cont_st, cont_end,diff_type,err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])
                        else:
                            local_dict[cont_name].append([cont_st, cont_end,diff_type,err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])
                    else:
                        local_dict[cont_name].append([cont_st, cont_end,diff_type,err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])

                elif diff_type in ['duplication']:
                
                    if local_dict[cont_name]!=[]:
                        if local_dict[cont_name][-1][6]==ref_st and local_dict[cont_name][-1][7]==ref_end and local_dict[cont_name][-1][2]=='insertion' and local_dict[cont_name][-1][5]==ref_name :
                            if local_dict[cont_name][-1][1]==cont_st-1:
                                local_dict[cont_name][-1][8]=local_dict[cont_name][-1][8]+'_'+tmp[0].split('=')[1]+'_'+str(local_dict[cont_name][-1][3])+'_'+str(err_len)+'_'+str(local_dict[cont_name][-1][0])+'_'+str(local_dict[cont_name][-1][1])
                                local_dict[cont_name][-1][1]=cont_end
                                local_dict[cont_name][-1][3]+=err_len
                                if err_len>16:
                                    local_dict[cont_name][-1][2]='duplication'
                            else:
                                local_dict[cont_name].append([cont_st, cont_end,diff_type,err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])
                        else:
                            local_dict[cont_name].append([cont_st, cont_end,diff_type,err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])
                    else:
                
                        local_dict[cont_name].append([cont_st, cont_end,diff_type,err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])
                else:
                    local_dict[cont_name].append([cont_st, cont_end,diff_type,err_len, cont_dir, ref_name, ref_st,ref_end,tmp[0].split('=')[1] ])

                     
            elif tmp[1].split('=')[1] in ['unaligned_sequence']:
                a='do_nothing'
            else:
                if tmp[1].split('=')[1] in ['translocation-overlap', 'translocation-insertion', 'translocation-insertion_ATGCN', 'translocation-inserted_gap']:
                    ref_seq_1=tmp[3].split('=')[1]
                    end_r_1=int(tmp[11].split('=')[1])
                    ref_seq_2=tmp[12].split('=')[1]
                    st_r_2=int(tmp[18].split('=')[1])
                    type_er=tmp[1].split('=')[1]

                    struct_dict[cont_name].append([type_er,cont_st,cont_end,ref_seq_1,end_r_1, ref_seq_2,st_r_2,tmp[0].split('=')[1]])
                    
                    
                elif tmp[1].split('=')[1] in ['relocation-overlap','relocation-insertion', 'relocation-insertion_ATGCN', 'relocation-inserted_gap']:
                    ref_seq_1=tmp[3].split('=')[1]
                    end_r_1=int(tmp[11].split('=')[1])
                    st_r_2=int(tmp[17].split('=')[1])
                    type_er=tmp[1].split('=')[1]

                    struct_dict[cont_name].append([type_er,cont_st,cont_end,ref_seq_1,end_r_1, ref_seq_1,st_r_2,tmp[0].split('=')[1]])

                
                elif tmp[1].split('=')[1] in ['translocation']:
                    ref_seq_1=tmp[2].split('=')[1]
                    end_r_1=int(tmp[10].split('=')[1])
                    ref_seq_2=tmp[11].split('=')[1]
                    st_r_2=int(tmp[17].split('=')[1])
                    type_er=tmp[1].split('=')[1]

                    struct_dict[cont_name].append([type_er,cont_st,cont_end,ref_seq_1,end_r_1, ref_seq_2,st_r_2,tmp[0].split('=')[1]])

                elif tmp[1].split('=')[1] in ['relocation']:
                    ref_seq_1=tmp[2].split('=')[1]
                    end_r_1=int(tmp[10].split('=')[1])
                    st_r_2=int(tmp[16].split('=')[1])
                    type_er=tmp[1].split('=')[1]

                    struct_dict[cont_name].append([type_er,cont_st,cont_end,ref_seq_1,end_r_1, ref_seq_1,st_r_2,tmp[0].split('=')[1]])
                    
                elif tmp[1].split('=')[1] in ['inversion']:
                    ref_seq=tmp[4].split('=')[1]
                    st_r=int(tmp[5].split('=')[1].split('-')[0])
                    end_r=int(tmp[5].split('=')[1].split('-')[1])
                    c_dir=int(tmp[3].split('=')[1])
                    type_er=tmp[1].split('=')[1]

                    struct_dict[cont_name].append([type_er,cont_st,cont_end,ref_seq,st_r,end_r,c_dir,tmp[0].split('=')[1]])

                elif tmp[1].split('=')[1].startswith('reshuffling'):
                    ref_seq=tmp[4].split('=')[1]
                    st_r=int(tmp[5].split('=')[1].split('-')[0])
                    end_r=int(tmp[5].split('=')[1].split('-')[1])
                    c_dir=int(tmp[3].split('=')[1])
                    
                    type_er=tmp[1].split('=')[1]

                    struct_dict[cont_name].append([type_er,cont_st,cont_end,ref_seq,st_r,end_r,c_dir,tmp[0].split('=')[1]])
                                                     
                else:
                    a='do_nothing'
                    
        line=f.readline()


    f.close()
    
    return local_dict,struct_dict
    

#--------------------------------------------------------------------------------------------------------------------
def PARSE_PILON(file_change,file_out,working_dir,asmb_1_dict, nucdiff_dir):

    result_dict={}

    for cont_name in asmb_1_dict.keys():
        result_dict[cont_name]=[]

    f=open(file_change,'r')

    line=f.readline()
    while line:
        
        temp=line[:-1].split(' ')

        cont_name=temp[0].split(':')[0]
        
        old_seq=temp[2]
        new_seq=temp[3]

        if '-' in temp[0].split(':')[1]:
            pos_st=int(temp[0].split(':')[1].split('-')[0])
            pos_end=int(temp[0].split(':')[1].split('-')[1])

            
            

            if len(new_seq)>1:
                general.WRITE_FASTA_FILE(working_dir+'temp_1.fasta',{'query_1':old_seq})
                general.WRITE_FASTA_FILE(working_dir+'temp_2.fasta',{'ref_1':new_seq})

                if len(new_seq)<65 or len(old_seq)<65:
                    subprocess.call(['nucdiff','--nucmer_opt', '-c 10' ,  working_dir+'temp_2.fasta', working_dir+'temp_1.fasta', working_dir+'NucDiff_temp','temp' ])
                else:
                    
                    RUN_NUCDIFF(working_dir+'temp_2.fasta', working_dir+'temp_1.fasta', working_dir+'NucDiff_temp', 'temp',nucdiff_dir )

                local_temp_dict,struct_temp_dict=PARSE_NUCDIFF(working_dir+'/NucDiff_temp/results/'+'temp',{'query_1':old_seq})

                

                if local_temp_dict=={'query_1': []}:
                    result_dict[cont_name].append([pos_st, pos_end,pos_end-pos_st+1])

                else:
                    for entry in local_temp_dict['query_1']:
                        result_dict[cont_name].append([pos_st-1+entry[0], pos_st-1+entry[1],pos_st-1+entry[1]-pos_st+1-entry[0]+1])
                    

                
            else:
                result_dict[cont_name].append([pos_st, pos_end,pos_end-pos_st+1 ])
        else:
            pos_st=int(temp[0].split(':')[1])

        
            result_dict[cont_name].append([pos_st, pos_st, len(temp[3])])

            
            
        line=f.readline()


    f=open(file_out,'r')

    for line in f:

        

        if line.startswith('Processing') and ':' in line and '-' in line:
            cont_name=line[:-1].split(' ')[1].split(':')[0]
            flag=1

        elif '# fix break' in line:
            temp=line[:-1].split(':')[2].split(' ')[0]

            if '-' in temp:
                pos_st=int(temp.split('-')[0])
                pos_end=int(temp.split('-')[1])
            else:
                pos_st=int(temp)
                pos_end=int(temp)

            result_dict[cont_name].append([pos_st, pos_end,0])

          
    f.close()

    return result_dict

#---------------------------------------------------------------------------------------------

def RUN_TOOLS(input_list):

    if input_list[0]=='RUN_NUCBREAK':
        RUN_NUCBREAK(input_list[1], input_list[2], input_list[3], input_list[4], input_list[5], input_list[6])

    elif input_list[0]=='RUN_PILON':
        RUN_PILON(input_list[1], input_list[2], input_list[3], input_list[4],input_list[5])
        
    elif input_list[0]=='RUN_NUCDIFF':
        RUN_NUCDIFF(input_list[1], input_list[2], input_list[3], input_list[4], input_list[5])

    


#----------------------------------------------------------------------------------------------




def RUN_PARSE_TOOLS(working_dir,pe1_file,pe2_file,asmb_1,asmb_2,prefix, p_num, asmb_1_dict, asmb_2_dict, nucdiff_dir, nucbreak_dir):

    p=Pool(p_num)

    input_list=[
                ['RUN_NUCBREAK',asmb_1, pe1_file, pe2_file, working_dir+'NucBreak_1', prefix+'_1', nucbreak_dir],
                ['RUN_NUCBREAK',asmb_2, pe1_file, pe2_file, working_dir+'NucBreak_2', prefix+'_2', nucbreak_dir],
                ['RUN_PILON',asmb_1, pe1_file, pe2_file, working_dir+'Pilon_1/', prefix+'_1'],
                ['RUN_PILON',asmb_2, pe1_file, pe2_file, working_dir+'Pilon_2/', prefix+'_2'],
                ['RUN_NUCDIFF',asmb_2,asmb_1,  working_dir+'NucDiff', prefix, nucdiff_dir]
                ]

    output=p.map(RUN_TOOLS,input_list)
    p.close()

    
    nucbreak_1_dict=PARSE_NUCBREAK(working_dir+'NucBreak_1/Results/'+prefix+'_1_breakpoints.bedgraph',asmb_1_dict)
    nucbreak_2_dict=PARSE_NUCBREAK(working_dir+'NucBreak_2/Results/'+prefix+'_2_breakpoints.bedgraph',asmb_2_dict)

    pilon_local_1_dict=PARSE_PILON(working_dir+'Pilon_1/'+prefix+'_1.changes',working_dir+'Pilon_1/'+prefix+'_1.out',working_dir,asmb_1_dict, nucdiff_dir)
    pilon_local_2_dict=PARSE_PILON(working_dir+'Pilon_2/'+prefix+'_2.changes',working_dir+'Pilon_2/'+prefix+'_2.out',working_dir,asmb_2_dict, nucdiff_dir)

    local_1_dict,struct_1_dict=PARSE_NUCDIFF(working_dir+'NucDiff/results/'+prefix,asmb_1_dict)



    return nucbreak_1_dict, nucbreak_2_dict, pilon_local_1_dict, pilon_local_2_dict, local_1_dict,struct_1_dict
    
