import pandas as pd
import argparse

## Read data in

def parse_args():
    ## Read in arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input_data', help='default cutoff is >= 45', required=False)

    parser.add_argument('-F', '--Female_cutoff', help='default cutoff is >= 45', required=False)

    parser.add_argument('-M', '--Male_cutoff', help='default cutoff is <= 1', required=False)

    args = parser.parse_args()

    return args

def get_cutoffs(args):
    #If cutoffs are provided use those else use default cutoffs F = 45 and M = 1

    if args.Female_cutoff is None:
        print("Default female cutoff at >= 45 is used")
        f_cutoff = 45
    else:
        print("Female cutoff is " + args.Female_cutoff)
        f_cutoff = args.Female_cutoff


    if args.Male_cutoff is None:
        print("Default Male cutoff at <= 1 is used")
        m_cutoff = 1
    else:
        print("Male cutoff is " + args.Male_cutoff)
        m_cutoff = args.Male_cutoff
    
    f_cutoff = int(f_cutoff)
    m_cutoff = int(m_cutoff)

    return f_cutoff, m_cutoff

def Predict_Sex(data, f_cutoff, m_cutoff):
    # Predict sex based on thresholds
    PredictedSex = []
    x_het = list(data.X_het)

    for x in x_het:
        if x >= f_cutoff:
            PredictedSex.append("female")
        elif x <= m_cutoff:
            PredictedSex.append("male")
        else:
            PredictedSex.append("unknown")

    Predicted_Sex = pd.DataFrame({'Predicted_Sex':PredictedSex}) 
    
    data2 = pd.concat([data, Predicted_Sex], axis=1)
    
    data2.to_csv('somalier.samples.tsv', sep='\t',index=False, header =True) #replace over existing file


def main():

    args = parse_args()

    data = pd.read_csv(args.input_data, sep='\t')
    
    f_cutoff, m_cutoff = get_cutoffs(args)

    PredictedSex = Predict_Sex(data, f_cutoff, m_cutoff)


if __name__ == "__main__":

    main()
