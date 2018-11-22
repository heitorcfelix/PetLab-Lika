import pandas as pd
import numpy as np

def divide_cells(row, rows, problem_columns, non_problem_columns, columns):
    size = len(row[list(problem_columns)[0]])

    for i in range(size):
        new_row = []
        for column in columns:
            if column in problem_columns:
                new_row.append(row[column][i])
            else:
                new_row.append(row[column])
        rows.append(new_row)

def explode_cells(df, non_problem_columns, columns):
    problem_columns = set({})

    df_aux = df.copy()

    for column in columns:
        if column not in non_problem_columns:
           df_aux[column] = df[column].str.split(pat=';')
           problem_columns.add(column)

    rows = []
    df_aux.apply(lambda row: divide_cells(row, rows, problem_columns, non_problem_columns, columns), axis=1)

    return pd.DataFrame(rows, columns=columns)

def get_table_by_columns(original_df, columns):
    df = original_df[columns]
    return df

def main(file_dir, file_name):

    original_df = pd.read_csv(file_dir + file_name)
    #print(original_df.columns)

    # Working with Mutation_Taster table
    # Non-problem column - MutationTaster_converted_rankscore 
    mutation_taster_columns = ['genename', 'MutationTaster_AAE', 
                    'MutationTaster_model', 'MutationTaster_pred', 
                    'MutationTaster_converted_rankscore', 
                    'MutationTaster_score']
    mutation_taster_df = get_table_by_columns(original_df, mutation_taster_columns)
    #print(mutation_taster_df['MutationTaster_AAE'])
    non_problem_columns = {'genename', 'MutationTaster_converted_rankscore'}

    update_df = explode_cells(mutation_taster_df, non_problem_columns, mutation_taster_columns)
    update_df.to_csv('teste.csv')

main('data/filter_rs/', 'dbNSFP3.5a_variant.chrM.csv')
