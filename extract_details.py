import sys
from Bio import SwissProt
import pandas as pd
'''
f_in: input uniprot data file name
f_out: output filename for the combined fasta
'''
f_in = sys.argv[1]
f_out = sys.argv[2]

ID_list = []
GO_terms = []
EC = []
TaxID = []
GeneId = []
AC = []
Synonyms = []

for record in SwissProt.parse(open(f_in)):
    ID_list.append(record.entry_name)
    TaxID.append('|'.join(record.taxonomy_id))
    # Accession number, has multiple values, use '|' as sep. for each accession.
    AC.append('|'.join(record.accessions))
    # Synonymus
    try:
        tmp_syn = []
        if 'Synonyms' in record.gene_name:
            for n in record.gene_name.split(';'):
                if 'Synonyms' in n:
                    tmp_syn.append(n.split('=')[1])
            Synonyms.append('|'.join(tmp_syn))
        else:
            Synonyms.append('')
    except:
        Synonyms.append('')
    # EC number
    tmp_ec = []
    if 'EC=' in record.description:
        for d in record.description.split(';'):
            if 'EC=' in d:
                tmp_ec.append(d.split('=')[1])
        EC.append('|'.join(tmp_ec))
    else:
        EC.append('')
    # GO and GeneId in cross reference
    tmp_go = []
    tmp_geneID = []
    for cr in record.cross_references:
        if cr[0]=='GeneID':
            tmp_geneID.append(cr[1])
        elif cr[0] == 'GO':
            tmp_go.append(cr[1])
    GeneId.append('|'.join(tmp_geneID))
    GO_terms.append('|'.join(tmp_go))


# generate csv file using pandas
df = pd.DataFrame()

df['ID'] = ID_list
df['Accession'] = AC
df['Synonyms'] = Synonyms
df['GeneId'] = GeneId
df['EC_number'] = EC
df['TaxID'] = TaxID
df['GO_terms'] = GO_terms

# save as a csv file
df.to_csv(f_out)
