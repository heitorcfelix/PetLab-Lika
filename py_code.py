import pandas as pd
import os
from fuctions import *
        
dbNSFP_DIRECTORY = "/bioinfo/dbNSFPv3.5a/"
dbNSFP_FILENAME = "dbNSFP3.5a_variant.chrM"

COLUMN_NAMES = ["genename", "rs_dbSNP150", "hg19_pos(1-based)", "cds_strand", "codonpos", "codon_degeneracy",
                "ref", "alt", "aaref", "aaalt", "aapos", "Ensembl_geneid", "Ensembl_transcriptid",
                "Ensembl_proteinid", "Uniprot_acc_Polyphen2", "Transcript_id_VEST3", "SIFT_pred",
                "Polyphen2_HDIV_pred", "Polyphen2_HVAR_pred", "LRT_pred", "MutationTaster_pred",
                "MutationAssessor_pred", "FATHMM_pred", "PROVEAN_pred", "VEST3_score", "MetaSVM_pred",
                "MetaLR_pred", "M-CAP_pred", "REVEL_score", "MutPred_score", "CADD_phred", "DANN_score",
                "fathmm-MKL_coding_pred"]

pd.set_option('display.max_columns', 300)

df = pd.read_csv(dbNSFP_DIRECTORY + dbNSFP_FILENAME, sep='\t')

#df = df[COLUMN_NAMES]

df = df.loc[df['rs_dbSNP150'] != '.']

info_df = parallelize_information_rate(df, 80, 48)

info_df.to_csv('Information Rate/' + dbNSFP_FILENAME + '.csv')