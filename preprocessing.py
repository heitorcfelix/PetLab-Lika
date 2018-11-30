import pandas as pd
import sys
import numpy as np
import re

def divide_cells(row, rows, columns, problem_columns):
    
    list_problem_col = list(problem_columns)
    size = 1
    for col in list_problem_col:
        if isinstance(row[col], list):
            curr_size = len(row[col])
            size = curr_size if curr_size > size else size

    for i in range(size):
        new_row = []
        for column in columns:
            if column in problem_columns:
                if len(row[column]) == size:
                    new_row.append(row[column][i])
                elif len(row[column]) == 1:
                    new_row.append(row[column][0])
                else:
                    print("coluna ", column, " tem tamanho ", len(row[column]), " e o size máximo é ", size)
            else:
                new_row.append(row[column])
        rows.append(new_row)

def explode_cells(df, columns, problem_columns):
    #problem_columns = set({})

    df_aux = df.copy()

    list_problem_col = list(problem_columns)
    for column in list_problem_col:
        if df[column].dtype != object:
            problem_columns.remove(column)
        else:
            df_aux[column] = df[column].str.split(pat=';')

    rows = []
    df_aux.apply(lambda row: divide_cells(row, rows, columns, problem_columns), axis=1)

    return pd.DataFrame(rows, columns=columns)

def get_table_by_columns(original_df, columns):
    df = original_df[columns]
    return df

def main(file_dir, file_name, fixed_dir):

    original_df = pd.read_csv(file_dir + file_name)
    #print(original_df.columns)

    columns_table1 = ['#chr', 'pos(1-based)', 'ref', 'alt', 'aaref', 
                    'aaalt', 'rs_dbSNP150', 'hg19_pos(1-based)', 'genename', 
                    'cds_strand', 'refcodon', 'codonpos', 'codon_degeneracy', 
                    'Ancestral_allele', 'Ensembl_geneid', 'LRT_score', 
                    'LRT_converted_rankscore', 'LRT_pred', 
                    'MutationAssessor_score', 'MutationAssessor_score_rankscore', 
                    'MutationAssessor_pred', 'MetaSVM_score', 'MetaSVM_rankscore', 
                    'MetaSVM_pred', 'MetaLR_score', 'MetaLR_rankscore', 
                    'MetaLR_pred', 'M-CAP_score', 'M-CAP_rankscore', 'M-CAP_pred', 
                    'REVEL_score', 'REVEL_rankscore', 'MutPred_score', 
                    'MutPred_rankscore', 'CADD_raw', 'CADD_raw_rankscore', 
                    'CADD_phred', 'DANN_score', 'DANN_rankscore', 
                    'fathmm-MKL_coding_score', 'fathmm-MKL_coding_rankscore', 
                    'fathmm-MKL_coding_pred', 'Eigen-raw', 'Eigen-phred', 
                    'Eigen-PC-raw', 'Eigen-PC-phred', 'Eigen-PC-raw_rankscore', 
                    'GenoCanyon_score', 'GenoCanyon_score_rankscore', 'Interpro_domain']
    
    columns_table2 = ['rs_dbSNP150', 'genename', 'Ensembl_transcriptid', 
                    'MutationTaster_score', 'MutationTaster_converted_rankscore', 
                    'MutationTaster_pred']
    problem_columns_table2 = {'Ensembl_transcriptid', 'MutationTaster_score', 
                            'MutationTaster_pred'}
    
    columns_table3 = ['rs_dbSNP150', 'genename', 'Ensembl_proteinid', 'aapos', 
                    'SIFT_score', 'SIFT_converted_rankscore', 'SIFT_pred', 
                    'FATHMM_score', 'FATHMM_converted_rankscore', 'FATHMM_pred', 
                    'PROVEAN_score', 'PROVEAN_converted_rankscore', 'PROVEAN_pred']
    problem_columns_table3 = {'Ensembl_proteinid', 'aapos', 'SIFT_score', 'SIFT_pred', 
                            'FATHMM_score', 'FATHMM_pred', 'PROVEAN_score', 'PROVEAN_pred'}
    
    columns_table4 = ['rs_dbSNP150', 'genename', 'Uniprot_acc_Polyphen2', 
                    'Polyphen2_HDIV_score', 'Polyphen2_HDIV_rankscore', 
                    'Polyphen2_HDIV_pred', 'Polyphen2_HVAR_score', 
                    'Polyphen2_HVAR_rankscore', 'Polyphen2_HVAR_pred']
    
    columns_table5 = ['rs_dbSNP150', 'genename', 'Transcript_id_VEST3', 
                    'VEST3_score', 'VEST3_rankscore']
    problem_columns_table5 = {'Transcript_id_VEST3', 'VEST3_score'}
    
    columns_table6 = ['rs_dbSNP150', 'genename', 'integrated_fitCons_score', 
                    'integrated_fitCons_score_rankscore', 'GM12878_fitCons_score', 
                    'GM12878_fitCons_score_rankscore', 'H1-hESC_fitCons_score', 
                    'H1-hESC_fitCons_score_rankscore', 'HUVEC_fitCons_score', 
                    'HUVEC_fitCons_score_rankscore', 'GERP++_NR', 'GERP++_RS', 
                    'GERP++_RS_rankscore', 'phyloP100way_vertebrate', 
                    'phyloP100way_vertebrate_rankscore', 'phyloP20way_mammalian', 
                    'phyloP20way_mammalian_rankscore', 'phastCons100way_vertebrate', 
                    'phastCons100way_vertebrate_rankscore', 'phastCons20way_mammalian',
                    'phastCons20way_mammalian_rankscore', 'SiPhy_29way_pi', 
                    'SiPhy_29way_logOdds', 'SiPhy_29way_logOdds_rankscore']
                
    columns_table7 = ['rs_dbSNP150', 'genename', 'ExAC_AC', 'ExAC_AF', 'ExAC_Adj_AC', 
                    'ExAC_Adj_AF', 'ExAC_AFR_AC', 'ExAC_AFR_AF', 'ExAC_AMR_AC', 
                    'ExAC_AMR_AF', 'ExAC_EAS_AC', 'ExAC_EAS_AF', 'ExAC_FIN_AC', 
                    'ExAC_FIN_AF', 'ExAC_NFE_AC', 'ExAC_NFE_AF', 'ExAC_SAS_AC', 
                    'ExAC_SAS_AF', 'ExAC_nonTCGA_AC', 'ExAC_nonTCGA_AF', 
                    'ExAC_nonTCGA_Adj_AC', 'ExAC_nonTCGA_Adj_AF', 'ExAC_nonTCGA_AFR_AC', 
                    'ExAC_nonTCGA_AFR_AF', 'ExAC_nonTCGA_AMR_AC', 'ExAC_nonTCGA_AMR_AF',
                    'ExAC_nonTCGA_EAS_AC', 'ExAC_nonTCGA_EAS_AF', 'ExAC_nonTCGA_FIN_AC', 
                    'ExAC_nonTCGA_FIN_AF', 'ExAC_nonTCGA_NFE_AC', 'ExAC_nonTCGA_NFE_AF', 
                    'ExAC_nonTCGA_SAS_AC', 'ExAC_nonTCGA_SAS_AF', 'ExAC_nonpsych_AC', 
                    'ExAC_nonpsych_AF', 'ExAC_nonpsych_Adj_AC', 'ExAC_nonpsych_Adj_AF', 
                    'ExAC_nonpsych_AFR_AC', 'ExAC_nonpsych_AFR_AF', 'ExAC_nonpsych_AMR_AC', 
                    'ExAC_nonpsych_AMR_AF', 'ExAC_nonpsych_EAS_AC', 'ExAC_nonpsych_EAS_AF', 
                    'ExAC_nonpsych_FIN_AC', 'ExAC_nonpsych_FIN_AF', 'ExAC_nonpsych_NFE_AC', 
                    'ExAC_nonpsych_NFE_AF', 'ExAC_nonpsych_SAS_AC', 'ExAC_nonpsych_SAS_AF', 
                    'gnomAD_exomes_AC', 'gnomAD_exomes_AN', 'gnomAD_exomes_AF', 
                    'gnomAD_exomes_AFR_AC', 'gnomAD_exomes_AFR_AN', 'gnomAD_exomes_AFR_AF', 
                    'gnomAD_exomes_AMR_AC', 'gnomAD_exomes_AMR_AN', 'gnomAD_exomes_AMR_AF', 
                    'gnomAD_exomes_ASJ_AC', 'gnomAD_exomes_ASJ_AN', 'gnomAD_exomes_ASJ_AF', 
                    'gnomAD_exomes_EAS_AC', 'gnomAD_exomes_EAS_AN', 'gnomAD_exomes_EAS_AF', 
                    'gnomAD_exomes_FIN_AC', 'gnomAD_exomes_FIN_AN', 'gnomAD_exomes_FIN_AF', 
                    'gnomAD_exomes_NFE_AC', 'gnomAD_exomes_NFE_AN', 'gnomAD_exomes_NFE_AF', 
                    'gnomAD_exomes_SAS_AC', 'gnomAD_exomes_SAS_AN', 'gnomAD_exomes_SAS_AF', 
                    'gnomAD_exomes_OTH_AC', 'gnomAD_exomes_OTH_AN', 'gnomAD_exomes_OTH_AF']

    # Working with Mutation_Taster table
    # Non-problem column - MutationTaster_converted_rankscore 
    '''
    mutation_taster_columns = ['genename', 'MutationTaster_AAE', 
                    'MutationTaster_model', 'MutationTaster_pred', 
                    'MutationTaster_converted_rankscore', 
                    'MutationTaster_score']
    mutation_taster_df = get_table_by_columns(original_df, mutation_taster_columns)
    '''
    #print(mutation_taster_df['MutationTaster_AAE'])
    #non_problem_columns = {'genename', 'MutationTaster_converted_rankscore'}

    '''update_df = explode_cells(mutation_taster_df, mutation_taster_columns)
    update_df.to_csv(fixed_dir + file_name)'''

    table1_df = get_table_by_columns(original_df, columns_table1)
    table2_df = get_table_by_columns(original_df, columns_table2)
    table3_df = get_table_by_columns(original_df, columns_table3)
    table4_df = get_table_by_columns(original_df, columns_table4)
    table5_df = get_table_by_columns(original_df, columns_table5)
    table6_df = get_table_by_columns(original_df, columns_table6)
    table7_df = get_table_by_columns(original_df, columns_table7)
    
    fold_name = re.match(r'.*\.(chr[MYX0-9]*)\.csv',file_name).groups()[0]

    #update_df = explode_cells(table1_df, columns_table1)
    #update_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"1.csv")
    table1_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"1.csv")

    update_df = explode_cells(table2_df, columns_table2, problem_columns_table2)
    update_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"2.csv")

    update_df = explode_cells(table3_df, columns_table3, problem_columns_table3)
    update_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"3.csv")

    # update_df = explode_cells(table4_df, columns_table4)
    # update_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"4.csv")
    table4_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"4.csv")

    update_df = explode_cells(table5_df, columns_table5, problem_columns_table5)
    update_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"5.csv")

    table6_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"6.csv")
    table7_df.to_csv(fixed_dir + fold_name + "/" + fold_name+"7.csv")



def filter_columns(original_df, columns):
    df = original_df[columns]
    return df

def main2(file_dir, file_name, filter_col_dir):
    original_df = pd.read_csv(file_dir + file_name)

    columns = ['#chr', 'pos(1-based)', 'ref', 'alt', 'aaref', 'aaalt', 
            'rs_dbSNP150', 'hg19_pos(1-based)', 'genename', 'cds_strand', 
            'refcodon', 'codonpos', 'codon_degeneracy', 'Ancestral_allele', 
            'Ensembl_geneid', 'Ensembl_transcriptid', 'Ensembl_proteinid', 
            'aapos', 'SIFT_score', 'SIFT_converted_rankscore', 'SIFT_pred', 
            'Uniprot_acc_Polyphen2', 'Polyphen2_HDIV_score', 
            'Polyphen2_HDIV_rankscore', 'Polyphen2_HDIV_pred', 'Polyphen2_HVAR_score', 
            'Polyphen2_HVAR_rankscore', 'Polyphen2_HVAR_pred', 'LRT_score', 
            'LRT_converted_rankscore', 'LRT_pred', 'MutationTaster_score', 
            'MutationTaster_converted_rankscore', 'MutationTaster_pred', 
            'MutationAssessor_score', 'MutationAssessor_score_rankscore', 
            'MutationAssessor_pred', 'FATHMM_score', 'FATHMM_converted_rankscore', 
            'FATHMM_pred', 'PROVEAN_score', 'PROVEAN_converted_rankscore', 
            'PROVEAN_pred', 'Transcript_id_VEST3', 'VEST3_score', 'VEST3_rankscore', 
            'MetaSVM_score', 'MetaSVM_rankscore', 'MetaSVM_pred', 'MetaLR_score', 
            'MetaLR_rankscore', 'MetaLR_pred', 'M-CAP_score', 'M-CAP_rankscore', 
            'M-CAP_pred', 'REVEL_score', 'REVEL_rankscore', 'MutPred_score', 
            'MutPred_rankscore', 'CADD_raw', 'CADD_raw_rankscore', 'CADD_phred', 
            'DANN_score', 'DANN_rankscore', 'fathmm-MKL_coding_score', 
            'fathmm-MKL_coding_rankscore', 'fathmm-MKL_coding_pred', 'Eigen-raw', 
            'Eigen-phred', 'Eigen-PC-raw', 'Eigen-PC-phred', 'Eigen-PC-raw_rankscore', 
            'GenoCanyon_score', 'GenoCanyon_score_rankscore', 'integrated_fitCons_score', 
            'integrated_fitCons_score_rankscore', 'GM12878_fitCons_score', 
            'GM12878_fitCons_score_rankscore', 'H1-hESC_fitCons_score', 
            'H1-hESC_fitCons_score_rankscore', 'HUVEC_fitCons_score', 
            'HUVEC_fitCons_score_rankscore', 'GERP++_NR', 'GERP++_RS', 'GERP++_RS_rankscore', 
            'phyloP100way_vertebrate', 'phyloP100way_vertebrate_rankscore', 
            'phyloP20way_mammalian', 'phyloP20way_mammalian_rankscore', 
            'phastCons100way_vertebrate', 'phastCons100way_vertebrate_rankscore', 
            'phastCons20way_mammalian', 'phastCons20way_mammalian_rankscore', 
            'SiPhy_29way_pi', 'SiPhy_29way_logOdds', 'SiPhy_29way_logOdds_rankscore', 
            'ExAC_AC', 'ExAC_AF', 'ExAC_Adj_AC', 'ExAC_Adj_AF', 'ExAC_AFR_AC', 
            'ExAC_AFR_AF', 'ExAC_AMR_AC', 'ExAC_AMR_AF', 'ExAC_EAS_AC', 'ExAC_EAS_AF', 
            'ExAC_FIN_AC', 'ExAC_FIN_AF', 'ExAC_NFE_AC', 'ExAC_NFE_AF', 'ExAC_SAS_AC', 
            'ExAC_SAS_AF', 'ExAC_nonTCGA_AC', 'ExAC_nonTCGA_AF', 'ExAC_nonTCGA_Adj_AC', 
            'ExAC_nonTCGA_Adj_AF', 'ExAC_nonTCGA_AFR_AC', 'ExAC_nonTCGA_AFR_AF', 
            'ExAC_nonTCGA_AMR_AC', 'ExAC_nonTCGA_AMR_AF', 'ExAC_nonTCGA_EAS_AC', 
            'ExAC_nonTCGA_EAS_AF', 'ExAC_nonTCGA_FIN_AC', 'ExAC_nonTCGA_FIN_AF', 
            'ExAC_nonTCGA_NFE_AC', 'ExAC_nonTCGA_NFE_AF', 'ExAC_nonTCGA_SAS_AC', 
            'ExAC_nonTCGA_SAS_AF', 'ExAC_nonpsych_AC', 'ExAC_nonpsych_AF', 
            'ExAC_nonpsych_Adj_AC', 'ExAC_nonpsych_Adj_AF', 'ExAC_nonpsych_AFR_AC', 
            'ExAC_nonpsych_AFR_AF', 'ExAC_nonpsych_AMR_AC', 'ExAC_nonpsych_AMR_AF', 
            'ExAC_nonpsych_EAS_AC', 'ExAC_nonpsych_EAS_AF', 'ExAC_nonpsych_FIN_AC', 
            'ExAC_nonpsych_FIN_AF', 'ExAC_nonpsych_NFE_AC', 'ExAC_nonpsych_NFE_AF', 
            'ExAC_nonpsych_SAS_AC', 'ExAC_nonpsych_SAS_AF', 'gnomAD_exomes_AC', 
            'gnomAD_exomes_AN', 'gnomAD_exomes_AF', 'gnomAD_exomes_AFR_AC', 
            'gnomAD_exomes_AFR_AN', 'gnomAD_exomes_AFR_AF', 'gnomAD_exomes_AMR_AC', 
            'gnomAD_exomes_AMR_AN', 'gnomAD_exomes_AMR_AF', 'gnomAD_exomes_ASJ_AC', 
            'gnomAD_exomes_ASJ_AN', 'gnomAD_exomes_ASJ_AF', 'gnomAD_exomes_EAS_AC', 
            'gnomAD_exomes_EAS_AN', 'gnomAD_exomes_EAS_AF', 'gnomAD_exomes_FIN_AC', 
            'gnomAD_exomes_FIN_AN', 'gnomAD_exomes_FIN_AF', 'gnomAD_exomes_NFE_AC', 
            'gnomAD_exomes_NFE_AN', 'gnomAD_exomes_NFE_AF', 'gnomAD_exomes_SAS_AC', 
            'gnomAD_exomes_SAS_AN', 'gnomAD_exomes_SAS_AF', 'gnomAD_exomes_OTH_AC', 
            'gnomAD_exomes_OTH_AN', 'gnomAD_exomes_OTH_AF', 'Interpro_domain']

    new_df = filter_columns(original_df, columns)

    new_df.to_csv(filter_col_dir + file_name)


#main('data/filter_rs/', 'dbNSFP3.5a_variant.chrM.csv')

#main2('/bioinfo/dbNSFPv3.5a_data/filter_rs/', 'dbNSFP3.5a_variant.chr1.csv', '/bioinfo/dbNSFPv3.5a_data/filter_columns/')

if __name__ == "__main__":
	if len(sys.argv) < 4:
		print("ERROR: Missing parameters")
		print("USAGE: python3 py_code.py dbNSFP_DIRECTORY dbNSFP_FILENAME filter_columns_DIRECTORY")
	else:
		main(sys.argv[1],sys.argv[2],sys.argv[3])
