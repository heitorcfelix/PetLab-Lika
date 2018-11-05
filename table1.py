import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import os
from dash.dependencies import Input, Output

dbNSFP_DIRECTORY = "/bioinfo/dbNSFPv3.5a/"
COLUMN_NAMES = ["genename", "rs_dbSNP150", "hg19_pos(1-based)", "cds_strand", "codonpos", "codon_degeneracy",
                "ref", "alt", "aaref", "aaalt", "aapos", "Ensembl_geneid", "Ensembl_transcriptid",
                "Ensembl_proteinid", "Uniprot_acc_Polyphen2", "Transcript_id_VEST3", "SIFT_pred",
                "Polyphen2_HDIV_pred", "Polyphen2_HVAR_pred", "LRT_pred", "MutationTaster_pred",
                "MutationAssessor_pred", "FATHMM_pred", "PROVEAN_pred", "VEST3_score", "MetaSVM_pred",
                "MetaLR_pred", "M-CAP_pred", "REVEL_score", "MutPred_score", "CADD_phred", "DANN_score",
                "fathmm-MKL_coding_pred"]
pd.set_option('display.max_columns', 300)

df1 = pd.read_csv(dbNSFP_DIRECTORY + "dbNSFP3.5a_variant.chrM", sep='\t')
df1 = df1.loc[df1['rs_dbSNP150'] != '.']
df1 = df1.head(100)
df1 = df1[COLUMN_NAMES]
df2 = pd.read_csv(dbNSFP_DIRECTORY + "dbNSFP3.5a_variant.chrY", sep='\t')
df2 = df2.loc[df2['rs_dbSNP150'] != '.']
df2 = df2[COLUMN_NAMES]
df2 = df2.head(100)

def generate_table(filename):
    if(filename == "dbNSFP3.5a_variant.chrM"):
        df = df1
    else:
        df = df2
    return df.to_dict('records')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dropdown = [{"label": dbNSFP_file, "value": dbNSFP_file} for dbNSFP_file in os.listdir(dbNSFP_DIRECTORY) if "dbNSFP3.5a_variant.chr" in dbNSFP_file]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='dbNSFP'),
    dcc.Dropdown(
        options= sorted(dropdown, key=lambda k: k['label']),
        value='dbNSFP3.5a_variant.chrM',
	id='my-dropdown'
    ),
    dt.DataTable(
        rows = df1.to_dict('records'),
        columns = df1.columns,
        filterable = False,
        sortable = True,
        selected_row_indices = [],
        id='datatable'
    )
])

@app.callback(Output('datatable', 'rows'), [Input('my-dropdown', 'value')])
def update_table(value):
    return generate_table(value)

if __name__ == '__main__':
    app.run_server(debug=True)