import pandas as pd
import argparse

# The ArgumentParser object will hold all the information necessary to parse the command line into Python data types.
parser = argparse.ArgumentParser(description='Process an array of somalier files.')

# Filling an ArgumentParser with information about program arguments is done by making calls to the add_argument() method. 
# Generally, these calls tell the ArgumentParser how to take the strings on the command line and turn them into objects.  
parser.add_argument('-a', '--array', nargs='+', required=True,
                    help='an array of somalier files')

args = parser.parse_args()
array = list(dict.values(vars(args)))[0] #vars removes the namespace data type into dictionary, pull out values using dict.values
print(array)

samplesID = []
for a in array:
    samplesID.append(a.split(".")[0])


FamilyID = samplesID
PaternalID = [0] * len(samplesID)
MaternalID = [0] * len(samplesID)
Sex = [-9] * len(samplesID)
Phenotype = [-9] * len(samplesID)

print("--------------Making PED FILE-----------")
df = pd.DataFrame(list(zip(FamilyID, samplesID,  PaternalID, MaternalID, Sex, Phenotype)), columns =['FID', 'IID', 'PaternalID', 'MaternalID','Sex', 'Phenotype'])
print(df)

df.to_csv('Samples.ped', sep='\t',index=False, header =False)
