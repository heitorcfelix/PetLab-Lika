import pandas as pd
import os
import sys
from fuctions import *
        
def main(file_dir, file_name, filter_dir, percent_dir):

	dbNSFP_DIRECTORY = file_dir
	dbNSFP_FILENAME = file_name
	filterRS_DIRECTORY = filter_dir
	percent_DIRECTORY = percent_dir

	columns_to_filter = ["genename", "rs_dbSNP150", "hg19_pos(1-based)", "cds_strand", "codonpos", "codon_degeneracy",
		        "ref", "alt", "aaref", "aaalt", "aapos", "Ensembl_geneid", "Ensembl_transcriptid",
		        "Ensembl_proteinid", "Uniprot_acc_Polyphen2", "Transcript_id_VEST3", "SIFT_pred",
		        "Polyphen2_HDIV_pred", "Polyphen2_HVAR_pred", "LRT_pred", "MutationTaster_pred",
		        "MutationAssessor_pred", "FATHMM_pred", "PROVEAN_pred", "VEST3_score", "MetaSVM_pred",
		        "MetaLR_pred", "M-CAP_pred", "REVEL_score", "MutPred_score", "CADD_phred", "DANN_score",
		        "fathmm-MKL_coding_pred"]

	pd.set_option('display.max_columns', 300)
	
	#Read the dataset from a csv file
	df = pd.read_csv(dbNSFP_DIRECTORY + dbNSFP_FILENAME, sep='\t')
	

	#filter_columns_df = filter_by_columns(df, columns_to_filter)

	cell_filter_df = filter_by_cell_value(df, 'rs_dbSNP150')

	#info_df = get_df_percent(df, 80, 48)


	#info_df.to_csv(percent_DIRECTORY + dbNSFP_FILENAME + '.csv')
	cell_filter_df.to_csv(filterRS_DIRECTORY + dbNSFP_FILENAME + '.csv')


def filter_by_cell_value(df, cell_value):
	df = df.loc[df[cell_value] != '.']
	return df

def filter_by_columns(df, columns):
	df = df[columns]
	return columns

def get_df_percent(df, partition_num, cores_num):
	info_df = parallelize_information_rate(df, partition_num, cores_num)
	return info_df

if __name__ == "__main__":
	if len(sys.argv) < 5:
		print("ERROR: Missing parameters")
		print("USAGE: python3 py_code.py dbNSFP_DIRECTORY dbNSFP_FILENAME filterRS_DIRECTORY percent_DIRECTORY")
	else:
		main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
