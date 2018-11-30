# copyright (c) 2018 Ksenia Khelik
#
# This Source Code Form is subject to the 
# terms of the Mozilla Public License, v. 2.0. 
# If a copy of the MPL was not distributed 
# with this file, You can obtain one at 
# https://mozilla.org/MPL/2.0/.
#
#-------------------------------------------------------------------------------

import shutil
import os

import general



def IS_COVERED(st_point,end_point,interv_list, flank,shift,err_type,tool_name):

    both_flag=0
    st_flag=0
    end_flag=0
    shift_flag=0

    flag=0

    if err_type in ['substitution']:
        for entry in interv_list:
            if entry[0]==st_point and entry[1]==end_point:
                flag=1
                break

    elif err_type in ['deletion']:
        for entry in interv_list:
            if entry[0]<=st_point and st_point-entry[0]<=flank and entry[1]>=end_point  and entry[1]-end_point<=flank:
                flag=1
                break
            elif end_point<entry[0] and entry[0]-end_point<=shift and entry[1]-end_point<=flank:
                flag=1
                break
            elif st_point>entry[1] and st_point-entry[1]<=shift and st_point-entry[0]<=flank:
                flag=1
                break

    elif err_type in ['insertion']:
        for entry in interv_list:
            if entry[0]<=st_point and st_point-entry[0]<=flank and entry[1]>=end_point  and entry[1]-end_point<=flank:
                flag=1
                break
            elif st_point>entry[0] and st_point<entry[1] and end_point>entry[1] and st_point-entry[0]<=flank and end_point-entry[1]<=flank and end_point-st_point<=entry[1]-entry[0]:
                flag=1
                break
            elif st_point<entry[0] and end_point >entry[0] and end_point>entry[1] and entry[0]-st_point<=flank and entry[1]-end_point<=flank and end_point-st_point<=entry[1]-entry[0]:
                flag=1
                break
            elif end_point==entry[0]-1 and end_point-st_point==entry[1]-entry[0]:
                flag=1
                break
            elif st_point==entry[1]+1 and end_point-st_point==entry[1]-entry[0]:
                flag=1
                break
    elif err_type in ['collapsed_repeat']:
        for entry in interv_list:
            if st_point>=entry[0] and st_point-entry[0]<=flank and end_point<=entry[1] and entry[1]-end_point<=flank:
                flag=1
                break
            elif st_point<=entry[0] and end_point>=entry[1]:
                if tool_name=='NucBreak':
                   flag=1
                   break
                else:
                    if entry[1]-entry[0]>15:
                        flag=1
                        break
                    

    elif err_type in ['duplication']:
        for entry in interv_list:
            if entry[0]<=st_point and st_point-entry[0]<=flank and entry[1]>=end_point  and entry[1]-end_point<=flank:
                flag=1
                break
            elif st_point>entry[0] and st_point<entry[1] and end_point>entry[1] and st_point-entry[0]<=flank and end_point-entry[1]<=shift and end_point-st_point<=entry[1]-entry[0]:
                flag=1
                break
            elif st_point<entry[0] and end_point >entry[0] and end_point>entry[1] and entry[0]-st_point<=shift and entry[1]-end_point<=flank and end_point-st_point<=entry[1]-entry[0]:
                flag=1
                break

    elif err_type in ['relocation']:

        for entry in interv_list:
            if entry[0]<=st_point and st_point-entry[0]<=flank and entry[1]>=end_point  and entry[1]-end_point<=flank:
                flag=1
                break
            elif end_point<entry[0] and entry[0]-end_point<=shift:
                if tool_name=='NucBreak':
                   flag=1
                   break
                else:
                    if entry[1]-entry[0]>15:
                        flag=1
                        break
                
            elif st_point>entry[1] and st_point-entry[1]<=shift:
                if tool_name=='NucBreak':
                   flag=1
                   break
                else:
                    if entry[1]-entry[0]>15:
                        flag=1
                        break
            elif st_point<=entry[0] and end_point>=entry[1]:
                if tool_name=='NucBreak':
                   flag=1
                   break
                else:
                    if entry[1]-entry[0]>15:
                        flag=1
                        break

    elif err_type in ['struct']:

        for entry in interv_list:
            if st_point-flank<=entry[0] and end_point+flank>=entry[1]:
                if entry[0]<=st_point and entry[1]>=end_point:

                    if tool_name=='NucBreak':
                       flag=1
                       break
                    else:
                        if entry[1]-entry[0]>15:
                            flag=1
                            break
                elif entry[1]<st_point and entry[1]+shift>st_point:
                    if tool_name=='NucBreak':
                       flag=1
                       break
                    else:
                        if entry[1]-entry[0]>15:
                            flag=1
                            break
                elif entry[0]>st_point and entry[0]<=end_point:
                    if tool_name=='NucBreak':
                       flag=1
                       break
                    else:
                        if entry[1]-entry[0]>15:
                            flag=1
                            break
                elif entry[0]>end_point and entry[0]-shift<=end_point:
                    if tool_name=='NucBreak':
                       flag=1
                       break
                    else:
                        if entry[1]-entry[0]>15:
                            flag=1
                            break
                    
                    
    return flag

   

def FILTER_LOCAL_ERRORS(local_1_dict,nucbreak_1_dict,nucbreak_2_dict ,pilon_local_1_dict,pilon_local_2_dict):

    for cont_name in local_1_dict.keys():
        
        for i in range(len(local_1_dict[cont_name])):
            local_1_dict[cont_name][i].append(-1)
            err_entry=local_1_dict[cont_name][i]

            cont_st=err_entry[0]
            cont_end=err_entry[1]
            err_type=err_entry[2]

            ref_name=err_entry[5]
            ref_st=err_entry[6]
            ref_end=err_entry[7]

            flank_ref=300
            shift_ref=5

            if err_type in ['deletion']:
                if ref_end-ref_st<15:
                    flank1=10
                    shift1=5
                    flank2=10
                    shift2=0
 
                else:
                    flank1=200#15
                    shift1=5
                    flank2=15
                    shift2=0

            elif err_type in ['substitution']:
                    flank1=0
                    shift1=0
                    flank2=0
                    shift2=0

                    
            elif err_type in ['insertion']:
                if cont_end-cont_st<15:
                    flank1=10
                    shift1=0
                    flank2=10
                    shift2=5
                else:
                    flank1=200
                    shift1=0
                    flank2=150
                    shift2=5
                    
            elif err_type in ['collapsed_repeat']:
                    flank1=300
                    shift1=0+1
                    flank2=250+1
                    shift2=0+1

            elif err_type in ['collapsed_tandem_repeat']:
                    flank1=300+1
                    shift1=0+1
                    flank2=250+1
                    shift2=0+1

            elif err_type in ['duplication']:
                    flank1=300
                    shift1=5+1
                    flank2=15+1
                    shift2=0+1
            elif err_type in ['tandem_duplication']:
                    flank1=300
                    shift1=5+1
                    flank2=15+1
                    shift2=0+1
            else:
                flank1=200+1
                shift1=25+1
                flank2=200+1
                shift2=25+1

            if err_type in ['deletion']:
                flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'deletion','Pilon')

                flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                if ref_end-ref_st<15  and flag_ref==0:
                    flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank2, shift2,'struct','Pilon')
                
                flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'deletion','NucBreak')

                flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                if ref_end-ref_st<15  and flag_ref_2==0:
                    flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank2, shift2,'struct','NucBreak')

                

                if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,1,1,0],[1,0,1,1]]:
                    local_1_dict[cont_name][i][-1]=1

                elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                    local_1_dict[cont_name][i][-1]=0

            elif err_type in ['insertion','inserted_gap']:
                flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'insertion','Pilon')
                if flag_cont==0 and err_entry[4]==-1:
                    flag_cont=IS_COVERED(cont_st-err_entry[3],cont_end-err_entry[3],pilon_local_1_dict[cont_name],flank1, shift1,'insertion','Pilon')

                flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                if cont_end-cont_st<15  and flag_ref==0:
                    flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank2, shift2,'struct','Pilon')
                
                flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'insertion','NucBreak')
                if flag_cont_2==0:
                    flag_cont_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'insertion','NucBreak')

                    if flag_cont_2==0:
                        flag_cont_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'insertion','NucBreak')

                flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                if cont_end-cont_st<15  and flag_ref_2==0:    
                    flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank2, shift2,'struct','NucBreak')

                

                if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0]]:
                    local_1_dict[cont_name][i][-1]=1

                elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                    local_1_dict[cont_name][i][-1]=0

            elif err_type in ['substitution','gap']:
                flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'substitution','Pilon')

                flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                if cont_end-cont_st<15  and flag_ref==0:
                    flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank2, shift2,'struct','Pilon')
                
                flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'substitution','NucBreak')

                flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                if cont_end-cont_st<15  and flag_ref_2==0:
                    flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank2, shift2,'struct','NucBreak')

                

                if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0]]:
                    local_1_dict[cont_name][i][-1]=1

                elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                    local_1_dict[cont_name][i][-1]=0

                       
            elif err_type in ['collapsed_repeat']:
                colrep_len_list=err_entry[8].split('_')
                

                if len(colrep_len_list)>4:
                    colrep_len=int(colrep_len_list[5])
                    ref_st_new=int(colrep_len_list[6])
                    ref_end_new=int(colrep_len_list[7])
                else:
                    colrep_len=err_entry[3]
                    ref_st_new=ref_st
                    ref_end_new=ref_end

                flag_cont=IS_COVERED(cont_st-colrep_len,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'collapsed_repeat','Pilon')
                if flag_cont==0:
                    flag_cont=IS_COVERED(cont_st-colrep_len,cont_st-colrep_len,pilon_local_1_dict[cont_name],flank1, shift1,'deletion','Pilon')
                    if flag_cont==0:
                        flag_cont=IS_COVERED(cont_st+1,cont_end+colrep_len,pilon_local_1_dict[cont_name],flank1, shift1,'collapsed_repeat','Pilon')
                    

                flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                flag_cont_2=IS_COVERED(cont_st+1,cont_end+colrep_len,nucbreak_1_dict[cont_name],flank1, shift1,'collapsed_repeat','NucBreak')

                flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0]]:
                    local_1_dict[cont_name][i][-1]=1

                elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                    local_1_dict[cont_name][i][-1]=0

            elif err_type in ['collapsed_tandem_repeat']:
                colrep_len=int(err_entry[3])
                

                flag_cont=IS_COVERED(cont_st-colrep_len,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'collapsed_repeat','Pilon')
                if flag_cont==0:
                    flag_cont=IS_COVERED(cont_st,cont_end+colrep_len,pilon_local_1_dict[cont_name],flank1, shift1,'collapsed_repeat','Pilon')
                flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                flag_cont_2=IS_COVERED(cont_st,cont_end+colrep_len,nucbreak_1_dict[cont_name],flank1, shift1,'collapsed_repeat','NucBreak')
                if flag_cont_2==0:
                    IS_COVERED(cont_st-colrep_len,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'collapsed_repeat','NucBreak')
                flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0]]:
                    local_1_dict[cont_name][i][-1]=1

                elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                    local_1_dict[cont_name][i][-1]=0

            elif err_type in ['tandem_duplication']:
                flag_cont=0
                flag_ref=0
                flag_cont_2=0
                flag_ref_2=0

                flag_cont=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'duplication','Pilon')
                if flag_cont==0:
                    flag_cont=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'duplication','Pilon')
                    
                flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                flag_cont_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'duplication','NucBreak')
                if flag_cont_2==0:
                    flag_cont_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'duplication','NucBreak')
                    
                flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0]]:
                    local_1_dict[cont_name][i][-1]=1

                elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                    local_1_dict[cont_name][i][-1]=0

                

            elif err_type in ['duplication']:
                colrep_len_list=err_entry[8].split('_')
                

                if len(colrep_len_list)>4:
                    colrep_len=int(colrep_len_list[5])
                else:
                    colrep_len=-1
                    
                
                flag_ref=0
               
                flag_ref_2=0

                if colrep_len==-1:
                    flag_cont=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'duplication','Pilon')


                    flag_cont_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'duplication','NucBreak')

                else:
                    flag_cont=IS_COVERED(cont_st,cont_end-colrep_len,pilon_local_1_dict[cont_name],flank1, shift1,'duplication','Pilon')
                    if flag_cont==0:
                        flag_cont=IS_COVERED(cont_st-colrep_len,cont_end-colrep_len,pilon_local_1_dict[cont_name],flank1, shift1,'duplication','Pilon')


                    flag_cont_2=IS_COVERED(cont_st,cont_end-colrep_len,nucbreak_1_dict[cont_name],flank1, shift1,'duplication','NucBreak')

                flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak') 

                if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0]]:
                    local_1_dict[cont_name][i][-1]=1

                elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                    local_1_dict[cont_name][i][-1]=0



           
           
           
                                            
         
            
#---------------------------------------------------------------------------------
def FILTER_STRUCT_ERRORS(struct_1_dict,nucbreak_1_dict,nucbreak_2_dict ,pilon_local_1_dict,pilon_local_2_dict, asmb_1_dict, asmb_2_dict):

    for cont_name in struct_1_dict.keys():
        
        for i in range(len(struct_1_dict[cont_name])):
            struct_1_dict[cont_name][i].append(-1)
            err_entry=struct_1_dict[cont_name][i]

            flank1=300+1
            shift1=5+1
            flank2=300+1
            shift2=0+1

            flank_ref=300
            shift_ref=0

            if err_entry[0].startswith('translocation') or err_entry[0].startswith('relocation'):

                cont_st=err_entry[1]
                cont_end=err_entry[2]

                ref_seq_1=err_entry[3]
                end_r_1=err_entry[4]
                ref_seq_2=err_entry[5]
                st_r_2=err_entry[6]

                err_type=err_entry[0]

                if end_r_1>50 and end_r_1<len(asmb_2_dict[ref_seq_1])-50 and st_r_2>50 and st_r_2<len(asmb_2_dict[ref_seq_2])-50:
                

                   
                    flag_overlap=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                    if flag_overlap==0:
                        flag_overl_st=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        flag_overl_end=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        if flag_overl_st==1 or flag_overl_end==1:
                            flag_overlap=1

                    flag_ref_1=IS_COVERED(end_r_1,end_r_1,pilon_local_2_dict[ref_seq_1],flank_ref, shift_ref,'struct','Pilon')
                    flag_ref_2=IS_COVERED(st_r_2,st_r_2,pilon_local_2_dict[ref_seq_2],flank_ref, shift_ref,'struct','Pilon')

                    if flag_ref_1==0 and flag_ref_2==0:
                        flag_ref=0
                    else:
                        flag_ref=1


                    flag_overlap_nb=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                    if flag_overlap_nb==0:
                        flag_overl_st_nb=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        flag_overl_end_nb=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        if flag_overl_st_nb==1 or flag_overl_end_nb==1:
                            flag_overlap_nb=1



                    flag_ref_1_nb=IS_COVERED(end_r_1,end_r_1,nucbreak_2_dict[ref_seq_1],flank_ref, shift_ref,'struct','NucBreak')
                    flag_ref_2_nb=IS_COVERED(st_r_2,st_r_2,nucbreak_2_dict[ref_seq_2],flank_ref, shift_ref,'struct','NucBreak')

                    if flag_ref_1_nb==0 and flag_ref_2_nb==0:
                        flag_ref_nb=0
                    else:
                        flag_ref_nb=1

                    if [flag_overlap,flag_ref,flag_overlap_nb,flag_ref_nb] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                        struct_1_dict[cont_name][i][-1]=1

                    elif [flag_overlap,flag_ref,flag_overlap_nb,flag_ref_nb] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                        struct_1_dict[cont_name][i][-1]=0


            elif err_entry[0].startswith('inversion') or (err_entry[0].startswith('reshuff') and err_entry[6]==1):
                cont_st=err_entry[1]
                cont_end=err_entry[2]
                ref_name=err_entry[3]
                ref_st=err_entry[4]
                ref_end=err_entry[5]

                err_type=err_entry[0]

                    
                if cont_st==1:
                    if ref_end!=len(asmb_2_dict[ref_name]):
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_end,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_end,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=3 # yes, end

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0

                elif cont_end==len(asmb_1_dict[cont_name]):
                    if ref_st!=1:
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_st,ref_st,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_st,ref_st,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=2 #yes, st

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0
                else:
                    if ref_st==1 and ref_end!=len(asmb_2_dict[ref_name]):

                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_end,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_end,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=3 # yes, end

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0

                    elif ref_st!=1 and ref_end==len(asmb_2_dict[ref_name]):
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_st,ref_st,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_st,ref_st,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=2 #yes, st

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0
    

                    else:
                        
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont_st=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                            flag_cont_end=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                            if flag_cont_st==1 and flag_cont_end==1:
                                flag_cont=1


                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref_1=IS_COVERED(ref_st,ref_st,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                            flag_ref_2=IS_COVERED(ref_end,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                            if flag_ref_1==0 and flag_ref_2==0:
                                flag_ref=0
                            else:
                                flag_ref=1
                            


                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_st_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                            flag_cont_end_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                            if flag_cont_st_2==1 and flag_cont_end_2==1:
                                flag_cont_2=1

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_1_2=IS_COVERED(ref_st,ref_st,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                            flag_ref_2_2=IS_COVERED(ref_end,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                            if flag_ref_1_2==0 and flag_ref_2_2==0:
                                flag_ref_2=0
                            else:
                                flag_ref_2=1
             
                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=4 #yes , both st and end

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0


                            
                            
            elif (err_entry[0].startswith('reshuff') and err_entry[6]==-1):
                cont_st=err_entry[1]
                cont_end=err_entry[2]
                ref_name=err_entry[3]
                ref_st=err_entry[4]
                ref_end=err_entry[5]

                err_type=err_entry[0]

                
                    
                if cont_st==1:
                    if ref_st!=1:
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_st,ref_st,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_st,ref_st,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=3 #yes, end
                            

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0

                elif cont_end==len(asmb_1_dict[cont_name]):
                    if ref_end!=len(asmb_2_dict[ref_name]):
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_end,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_end,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=2 # yes, st

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0
                else:
                    if ref_st==1 and ref_end!=len(asmb_2_dict[ref_name]):

                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_end,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_end,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=2 # yes, st

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0

                    elif ref_st!=1 and ref_end==len(asmb_2_dict[ref_name]):
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref=IS_COVERED(ref_st,ref_st,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_2=IS_COVERED(ref_st,ref_st,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=3 #yes, end

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0
    

                    else:
                        
                        flag_cont=IS_COVERED(cont_st,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                        if flag_cont==0:
                            flag_cont_st=IS_COVERED(cont_st,cont_st,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')
                            flag_cont_end=IS_COVERED(cont_end,cont_end,pilon_local_1_dict[cont_name],flank1, shift1,'relocation','Pilon')

                            if flag_cont_st==1 and flag_cont_end==1:
                                flag_cont=1


                        flag_ref=IS_COVERED(ref_st,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                        if flag_ref==0:
                            flag_ref_1=IS_COVERED(ref_st,ref_st,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')
                            flag_ref_2=IS_COVERED(ref_end,ref_end,pilon_local_2_dict[ref_name],flank_ref, shift_ref,'struct','Pilon')

                            if flag_ref_1==0 and flag_ref_2==0:
                                flag_ref=0
                            else:
                                flag_ref=1
                            


                        flag_cont_2=IS_COVERED(cont_st,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                        if flag_cont_2==0:
                            flag_cont_st_2=IS_COVERED(cont_st,cont_st,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')
                            flag_cont_end_2=IS_COVERED(cont_end,cont_end,nucbreak_1_dict[cont_name],flank1, shift1,'relocation','NucBreak')

                            if flag_cont_st_2==1 and flag_cont_end_2==1:
                                flag_cont_2=1

                        flag_ref_2=IS_COVERED(ref_st,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                        if flag_ref_2==0:
                            flag_ref_1_2=IS_COVERED(ref_st,ref_st,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')
                            flag_ref_2_2=IS_COVERED(ref_end,ref_end,nucbreak_2_dict[ref_name],flank_ref, shift_ref,'struct','NucBreak')

                            if flag_ref_1_2==0 and flag_ref_2_2==0:
                                flag_ref_2=0
                            else:
                                flag_ref_2=1
             
                        if [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,1,0], [1,0,0,0],[1,0,1,0],[1,0,1,1],[1,1,1,0],  [0,1,1,0]]:
                            struct_1_dict[cont_name][i][-1]=4 #yes , both st and end

                        elif [flag_cont,flag_ref,flag_cont_2,flag_ref_2] in [[0,0,0,1], [0,1,0,0],[0,1,0,1],[0,1,1,1],[1,1,0,1]]:
                            struct_1_dict[cont_name][i][-1]=0

    

#--------------------------------------------------------------

def CORRECT_LOCAL_ERRORS(asmb_1_dict, asmb_2_dict, local_1_dict, struct_1_dict, asmb_1_name_list):


    err_list=[]
    new_asmb_dict={}
    corrected_diff_dict={}
    struct_modif_dict={}


    for cont_name in asmb_1_name_list:
        corrected_diff_dict[cont_name]=[]
        struct_modif_dict[cont_name]=[]
        
        for entry in struct_1_dict[cont_name]:
            if entry[0]=='inversion' and entry[8]>1:
                flag=0
                inv_st=entry[1]
                inv_end=entry[2]

                for en in struct_1_dict[cont_name]:
                    if en[0].startswith('resh') and en[8]>1:
                        if inv_st==en[1] and inv_end==en[2]:
                            flag=1
                            break
                if flag==0:
                    new_seq=asmb_1_dict[cont_name][:inv_st-1-1 +1]+general.COMPL_STRING(asmb_1_dict[cont_name][inv_st-1: inv_end-1 +1 ])+asmb_1_dict[cont_name][inv_end-1+1:]

                    asmb_1_dict[cont_name]=new_seq
                    entry[8]=-2

                    struct_modif_dict[cont_name].append(['inversion', inv_st, inv_end, entry[7], entry[0]])

                    

      
        cur_ind=1

        for err_entry in local_1_dict[cont_name]:
            if err_entry[9]==1:
                err_list.append(err_entry)

        for err_entry in struct_1_dict[cont_name]:
            if err_entry[-1]==1:
                err_list.append([err_entry[1]])
                for enr in err_entry:
                    err_list[-1].append(enr)

            elif err_entry[-1]==2:
                err_list.append([err_entry[1]])
                for enr in err_entry:
                    err_list[-1].append(enr)
                err_list[-1][3]=err_list[-1][2]

                
            elif err_entry[-1]==3:
                err_list.append([err_entry[2]+1])
                for enr in err_entry:
                    err_list[-1].append(enr)
                err_list[-1][3]=err_list[-1][3]+1
                err_list[-1][2]=err_list[-1][3]


            elif err_entry[-1]==4:
                err_list.append([err_entry[1]])
                for enr in err_entry:
                    err_list[-1].append(enr)
                err_list[-1][3]=err_list[-1][2]


                err_list.append([err_entry[2]+1])
                for enr in err_entry:
                    err_list[-1].append(enr)
                err_list[-1][3]=err_list[-1][3]+1
                err_list[-1][2]=err_list[-1][3]


       
        err_list=sorted(err_list,key=lambda inter:inter[0], reverse=False )


        cont_ind=1
        if err_list!=[]:
            seq_new=''
            cur_pos=0

            for err in err_list:
                        if err[1] in ['relocation', 'translocation']:
                            struct_modif_dict[cont_name].append(['breakpoint', err[2], err[3], err[8], err[1]])
                            
                            if cur_pos<err[2]:
                                seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:err[2] -1+1]
                                cur_pos=err[2]
                            else:
                                cur_pos=max(cur_pos,err[2])

                            if seq_new!='':
                                new_asmb_dict[cont_name+'_'+str(cont_ind)+'_new']=seq_new
                                cont_ind+=1
                                seq_new=''

                        elif err[1] in ['relocation-overlap', 'translocation-overlap']:
                            struct_modif_dict[cont_name].append(['breakpoint', err[2], err[3], err[8], err[1]])
                            
                            if cur_pos<err[3]:
                                seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:err[3] -1+1]
                                cur_pos=max(cur_pos, err[2]-1)
                           
                            if seq_new!='':
                                new_asmb_dict[cont_name+'_'+str(cont_ind)+'_new']=seq_new
                                cont_ind+=1
                                seq_new=''

                        elif err[1] in ['relocation-insertion', 'translocation-insertion','translocation-insertion_ATGCN', 'translocation-inserted_gap','relocation-insertion_ATGCN', 'relocation-inserted_gap']:
                            struct_modif_dict[cont_name].append(['breakpoint', err[2], err[3], err[8], err[1]])
                            
                            if cur_pos<err[2]-1:
                                seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:err[2]-1 -1+1]
                                cur_pos=err[3]
                            else:
                                cur_pos=max(cur_pos, err[3])

                            if seq_new!='':
                                new_asmb_dict[cont_name+'_'+str(cont_ind)+'_new']=seq_new
                                cont_ind+=1
                                seq_new=''

                        elif str(err[1]).startswith('inversion') or str(err[1]).startswith('reshuffling'):
                            struct_modif_dict[cont_name].append(['breakpoint', err[2], err[3], err[8], err[1]])
                            
                            if cur_pos<err[2]-1:
                                seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:err[2]-1 -1+1]
                                cur_pos=err[2]-1
                            else:
                                cur_pos=max(cur_pos,err[2]-1)

                            if seq_new!='':
                                new_asmb_dict[cont_name+'_'+str(cont_ind)+'_new']=seq_new
                                cont_ind+=1
                                seq_new=''

                        else:
                            
                            if err[2] in ['deletion', 'collapsed_repeat', 'collapsed_tandem_repeat']:
                                if cur_pos!=err[0]:
                                    seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:err[0] -1+1]
                                    cur_pos=err[0]

                                if err[4]==1:
                                    seq_new+=asmb_2_dict[err[5]][err[6] -1:err[7] -1+1]
                                    corrected_diff_dict[cont_name].append([err, '.',asmb_2_dict[err[5]][err[6] -1:err[7] -1+1] ])
                                else:
                                    seq_new+=general.COMPL_STRING(asmb_2_dict[err[5]][err[6] -1:err[7] -1+1])
                                    corrected_diff_dict[cont_name].append([err, '.',general.COMPL_STRING(asmb_2_dict[err[5]][err[6] -1:err[7] -1+1]) ])
                                    
                            elif err[2] in ['insertion', 'tandem_duplication','duplication', 'unaligned_beginning', 'unaligned_end', 'inserted_gap']:
                                if cur_pos!=err[0]-1:
                                    seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:err[0]-1 -1+1]
                                    cur_pos=err[0]-1

                                corrected_diff_dict[cont_name].append([err,asmb_1_dict[cont_name][err[0] -1:err[1]-1  +1 ],'.' ])

                                cur_pos=err[1]
                                
                            elif err[2] in ['substitution','gap']:
                                if cur_pos!=err[0]-1:
                                    seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:err[0]-1 -1+1]
                                    cur_pos=err[0]-1

                                if err[4]==1:
                                    seq_new+=asmb_2_dict[err[5]][err[6] -1:err[7] -1+1]
                                    corrected_diff_dict[cont_name].append([err,asmb_1_dict[cont_name][err[0] -1:err[1]-1  +1 ],asmb_2_dict[err[5]][err[6] -1:err[7] -1+1] ])
                                else:
                                    seq_new+=general.COMPL_STRING(asmb_2_dict[err[5]][err[6] -1:err[7] -1+1])
                                    corrected_diff_dict[cont_name].append([err,asmb_1_dict[cont_name][err[0] -1:err[1]-1  +1 ],general.COMPL_STRING(asmb_2_dict[err[5]][err[6] -1:err[7] -1+1]) ])

                                cur_pos=err[1]
                            

            if cur_pos!=len(asmb_1_dict[cont_name]):
                seq_new+=asmb_1_dict[cont_name][cur_pos+1  -1:len(asmb_1_dict[cont_name]) -1+1]

            if cont_ind==1:
                new_asmb_dict[cont_name+'_new']=seq_new
            else:
                new_asmb_dict[cont_name+'_'+str(cont_ind)+'_new']=seq_new

            for i in range(len(err_list)):
                err_list.pop(0)
    
        else:
            new_asmb_dict[cont_name+'_new']=asmb_1_dict[cont_name]

        
    return new_asmb_dict, corrected_diff_dict, struct_modif_dict



def CORRECT_ERRORS(nucbreak_1_dict, nucbreak_2_dict, pilon_local_1_dict, pilon_local_2_dict, local_1_dict,struct_1_dict,asmb_1_dict, asmb_2_dict, asmb_1_name_list, working_dir,prefix):
    


    FILTER_LOCAL_ERRORS(local_1_dict,nucbreak_1_dict,nucbreak_2_dict ,pilon_local_1_dict,pilon_local_2_dict)

    FILTER_STRUCT_ERRORS(struct_1_dict,nucbreak_1_dict,nucbreak_2_dict ,pilon_local_1_dict,pilon_local_2_dict, asmb_1_dict, asmb_2_dict)

    new_asmb_dict,corrected_diff_dict, struct_modif_dict=CORRECT_LOCAL_ERRORS(asmb_1_dict, asmb_2_dict, local_1_dict, struct_1_dict,asmb_1_name_list)

    general.WRITE_FASTA_FILE(working_dir+prefix+'_nucmerge_asmb.fasta',new_asmb_dict)

    general.GENERATE_GFF_OUTPUT(corrected_diff_dict,working_dir, prefix,asmb_1_dict, struct_modif_dict)


    shutil.rmtree(working_dir+'NucDiff_temp')
    if os.path.exists(working_dir+'temp_1.fasta'):
        os.remove(working_dir+'temp_1.fasta')
    if os.path.exists(working_dir+'temp_2.fasta'):
        os.remove(working_dir+'temp_2.fasta')    
