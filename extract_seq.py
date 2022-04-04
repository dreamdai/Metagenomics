import sys
from Bio import SwissProt
'''
f_in: input uniprot data file name
f_out: output filename for the combined fasta
header: entry name, taxonomy id, length, weight, CRC32 value
'''
f_in = sys.argv[1]
f_out = sys.argv[2]
with open(f_out, 'w') as f:
    for record in SwissProt.parse(open(f_in)):
        f.write('>'+record.entry_name+' | '+','.join(record.taxonomy_id)+' | '+' | '.join(map(str, record.seqinfo))+'\n')
        f.write(record.sequence+'\n')
