import pandas as pd
from ..models import Patient

def run():
    # reading the csv storing it as a df
    csv = '/Users/rachelwolde/Desktop/FYP/FYP_REPO/FinalYearProject/Patient_tabular_data (1).csv'
    df = pd.read_csv(csv)

    # Iterating through the df and for each df value creating a Patient model instance 
    for index, row in df.iterrows():
        patient = Patient(
            PTID = row['PTID'],
            PTGENDER = row['PTGENDER'],
            PTRACCAT = row['PTRACCAT'],
            FHQSIBAD = row['FHQSIBAD'],
            DIAGNOSIS = row['DIAGNOSIS'],
            DXDDUE= row['DXDDUE'],
            GENOTYPE = row['GENOTYPE'],
            MMSCORE = row['MMSCORE'],
            AGE = row['Age']

        )
        patient.save()