# NucMerge manual

<br><br>
## 1 Introduction
NucMerge improves genome assembly accuracy by incorporating information derived from an alternative assembly and paired-end Illumina reads from the same genome. It corrects insertion, deletion, substitution, and inversion errors and locates inter- and intra-chromosomal rearrangement errors. The tool is described in the manuscript mentioned in Section 6.




<br><br>
## 2 Prerequisites
NucMerge can be run on Linux and Mac OS. 

Tools that should be preinstalled and added to the PATH before running NucMerge:

* Pilon (https://github.com/broadinstitute/pilon)
* BWA (https://sourceforge.net/projects/bio-bwa/)
* SAMtools (https://github.com/samtools/samtools)
* Bowtie2 (https://sourceforge.net/projects/bowtie-bio/files/bowtie2/)
* MUMmer (http://sourceforge.net/projects/mummer/ )
* the Biopython package (http://biopython.org/wiki/Download)
* NucDiff (https://github.com/uio-cels/NucDiff)

NucBreak (https://github.com/uio-bmi/NucBreak) is provided together with NucMerge. 

NucMerge was tested using Python 2.7, Pilon v1.22, NucDiff v2.0.2, NucBreak v1.0, bwa v0.7.5, samtools v.1.3.1, bowtie2 2.2.9, and MUMmer 3.23.


<br><br>
## 3 Installation

Clone the NucMerge github repository using the following command:

```
git clone --recursive https://github.com/uio-bmi/NucMerge.git
 
```

<br><br>
## 4 Running
### 4.1 Command line syntax and input arguments
To run NucMerge, run `nucmerge.py` with valid input arguments:

```
python nucmerge.py [-h] [--proc [int]] [--version]
                   Target_assembly.fasta Query_assembly.fasta PE_reads_1.fastq PE_reads_2.fastq Output_dir Prefix

```

Positional arguments:

* **Target_assembly.fasta** - Fasta file with the target assembly
* **Query_assembly.fasta** - Fasta file with the query assembly
* **PE_reads_1.fastq** - Fastq file with the first part of paired-end reads. They are supposed to be forward-oriented.
* **PE_reads_2.fastq** - Fastq file with the second part of paired-end reads. They are supposed to be reverse-oriented.
* **Output_dir** - Path to the directory where all intermediate and final results will be stored
* **Prefix** - Name that will be added to all generated files

Optional arguments:

* **-h, --help** - show this help message and exit
* **--proc** - Number of processes to be used. It is advised to use 5 processes. [5]
* **--version** - show program's version number and exit

### 4.2 Running examples
A running example with the NucMerge predefined parameter values:

```
python nucmerge.py my_target_asmb.fasta my_query_asmb.fasta my_pe_reads_1.fastq my_pe_reads_2.fastq my_output_dir my_prefix
```

A running example with the introduced --proc parameter value:

```
python nucmerge.py --proc 1 my_target_asmb.fasta my_query_asmb.fasta my_pe_reads_1.fastq my_pe_reads_2.fastq my_output_dir my_prefix
```

<br><br>
## 5 NucMerge output
NucMerge stores the output results produced by NucDiff, NucBreak, and Pilon in the following directories:
* Nucdiff - `<output_dir>/NucDiff`
* NucBreak run with the target assembly - `<output_dir>/NucBreak_1`
* NucBreak run with the query assembly - `<output_dir>/NucBreak_2`
* Pilon run with the target assembly - `<output_dir>/Pilon_1`
* Pilon run with the query assembly - `<output_dir>/Pilon_2`  

NucMerge produces the following files stored in `<output_dir>`:

* &lsaquo;Prefix&rsaquo;_local_differences.gff
* &lsaquo;Prefix&rsaquo;_structural_differences.gff
* &lsaquo;Prefix&rsaquo;_nucmerge_asmb.fasta


### 5.1 &lsaquo;Prefix&rsaquo;_local_differences.gff
The file contains information about the different types of insertion, deletion, and substitution errors detected in the target assembly. 

The following information is contained in the file:

* **column 1** - Name of the target assembly sequence
* **column 2** - NucMerge version used
* **column 3** - Sequence Ontology accession number 
* **column 4** - Error start
* **column 5** - Error end
* **column 6,7,8** - Score/strand/phase fields are not used
* **column 9, ID** - Identification name of an error
* **column 9, ID_nucdiff** - Error's ID assigned by NucDiff. If ID_nucdiff starts with SNP, information about the error can be found in query_snps.gff, else it can be found in query_struct.gff. 
* **column 9, Name** - Error type as it is detected by NucDiff compared to the query assembly
* **column 9, old_len** - Length of an errorneous fragment in the target assembly
* **column 9, new_len** - Length of an erroneous frgament after correction in the resulted assembly
* **column 9, old_seq** - Errorneous fragment sequence in the target assembly
* **column 9, new_seq** - Errorneous fragment sequence after correction in the resulted assembly


The description of the query_snps.gff and query_struct.gff files produced by NucDiff and all possible error types can be found at https://github.com/uio-cels/NucDiff/wiki.

The &lsaquo;Prefix&rsaquo;_local_differences.gff file example:
```
##gff-version 3
##sequence-region	NODE_1	1	273095
NODE_1	NucMerge_v1.0	SO:1000002	27951	27951	.	.	.	ID=LD_1;ID_nucdiff=SNP_4;Name=substitution;old_len=1;new_len=1;old_seq=C;new_seq=G;color=#42C042
NODE_1	NucMerge_v1.0	SO:0000667	129759	129759	.	.	.	ID=LD_2;ID_nucdiff=SNP_11;Name=insertion;old_len=1;new_len=0;old_seq=G;new_seq=.;color=#EE0000
NODE_1	NucMerge_v1.0	SO:0000667	233592	233601	.	.	.	ID=LD_3;ID_nucdiff=SNP_27;Name=inserted_gap;old_len=10;new_len=0;old_seq=NNNNNNNNNN;new_seq=.;color=#EE0000
##sequence-region	NODE_2	1	211125
NODE_2	NucMerge_v1.0	SO:1000035	139350	139382	.	.	.	ID=LD_4;ID_nucdiff=SV_21;Name=duplication;old_len=33;new_len=0;old_seq=CCCGGGAGCATAGATAACTATGTGACCGGGGTG;new_seq=.;color=#EE0000
NODE_2	NucMerge_v1.0	SO:0000159	173435	173435	.	.	.	ID=LD_5;ID_nucdiff=SV_33;Name=collapsed_tandem_repeat;old_len=0;new_len=20;old_seq=.;new_seq=AGCCAGCGGCTGTTTGTCAG;color=#0000EE
...
```


### 5.2 &lsaquo;Prefix&rsaquo;_structural_differences.gff
The file contains information about inversion errors and structural breakpoints corresponding to inter- and intra-chromosomal rearrangement errors detected in the target assembly.

The following information is contained in the file:

* **column 1** - Name of the target assembly sequence
* **column 2** - NucMerge version used
* **column 3** - Sequence Ontology accession number 
* **column 4** - Error start
* **column 5** - Error end
* **column 6,7,8** - Score/strand/phase fields are not used
* **column 9, ID** - Identification name of an error
* **column 9, Name** - Iversion or breakpoint 
* **column 9, ID_nucdiff** - Error's ID assigned by NucDiff. Information about the error can be found in query_struct.gff. 
* **column 9, Type_nucdiff** - The type of an error detected by NucDiff.  The real error type can differ from the given one. 


The description of the query_struct.gff file produced by NucDiff and all possible error types can be found at https://github.com/uio-cels/NucDiff/wiki.

The &lsaquo;Prefix&rsaquo;_structural_differences.gff file example:
```
##gff-version 3
##sequence-region	NODE_1	1	617
NODE_1	NucMerge_v1.0	SO:0000699	331	430	.	.	.	ID=SD_1;Name=breakpoint;ID_nucdiff=SV_149;Type_nucdiff=translocation-inserted_gap;color=#0000EE
##sequence-region	NODE_2	1	4763
NODE_2	NucMerge_v1.0	SO:0000699	4478	4478	.	.	.	ID=SD_2;Name=breakpoint;ID_nucdiff=SV_174;Type_nucdiff=reshuffling-part_1_gr_0;color=#0000EE
##sequence-region	NODE_3	1	208973
NODE_3	NucMerge_v1.0	SO:1000036	418	1022	.	.	.	ID=SD_3;Name=inversion;ID_nucdiff=SV_317;Type_nucdiff=inversion;color=#EE0000
NODE_3	NucMerge_v1.0	SO:0000699	71741	71926	.	.	.	ID=SD_4;Name=breakpoint;ID_nucdiff=SV_2577;Type_nucdiff=translocation-inserted_gap;color=#0000EE
NODE_3	NucMerge_v1.0	SO:0000699	110857	110857	.	.	.	ID=SD_5;Name=breakpoint;ID_nucdiff=SV_2629;Type_nucdiff=reshuffling-part_2_gr_1;color=#0000EE
NODE_3	NucMerge_v1.0	SO:0000699	110857	110857	.	.	.	ID=SD_6;Name=breakpoint;ID_nucdiff=SV_2630;Type_nucdiff=inversion;color=#0000EE
...
```


### 5.3 &lsaquo;Prefix&rsaquo;_nucmerge_asmb.fasta

The file contains the resulted assembly obtained from the target assembly by (1) correcting inversion errors and errors listed in &lsaquo;Prefix&rsaquo;_local_differences.gff and (2) splitting target assembly sequences in the regions contained breakpoints from &lsaquo;Prefix&rsaquo;_structural_differences.gff. 



### 6 Citing NucMerge

To cite your use of NucMerge in your publication :

Khelik K., et al. NucMerge: Genome assembly quality improvement assisted by alternative assemblies and paired-end Illumina reads. (in preparation)
