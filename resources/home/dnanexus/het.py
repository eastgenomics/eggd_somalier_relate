import pandas as pd
import argparse

def parse_args():
    """Parse through arguements
    

    Returns:
        args: Variable that you can extract relevant
        arguements inputs needed
    """
    # Read in arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-i', '--input_data',
        help='default cutoff is >= 45',
        required=False
        )

    parser.add_argument(
        '-F', '--Female_cutoff',
        help='default cutoff is >= 45',
        required=False
        )

    parser.add_argument(
        '-M', '--Male_cutoff',
        help='default cutoff is <= 1',
        required=False
        )

    args = parser.parse_args()

    return args


def get_cutoffs(args):
    """Pulls out thresholds from arguments

    Args:
        args (variable): Contains all input arguments

    Returns:
        f_cuttoff (int): female het calls threshold
        m_cuttoff (int): male het calls threshold
    """
    # If cutoffs are provided use those else use default cutoffs F = 45 and M = 1

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
    
    # Need to convert to int as its str so far
    f_cutoff = int(f_cutoff)
    m_cutoff = int(m_cutoff)

    return f_cutoff, m_cutoff


def Predict_Sex(data, f_cutoff, m_cutoff):
    """Predicts sex on data provided based on given / default thresholds

    Args:
        data (panda data frame): output from {sample}.somalier.samples.tsv
        f_cutoff (int): from -F input provided as arg
        m_cutoff (int): from -M input provided as arg

    Returns:
        data (pandas data frame): Updates dataframe 
        including predicted sex column
    """
    PredictedSex = []
    x_het = list(data.X_het)

    for x in x_het:
        if x >= f_cutoff:
            PredictedSex.append("female")
        elif x <= m_cutoff:
            PredictedSex.append("male")
        else:
            PredictedSex.append("unknown")

    Predicted_Sex = pd.DataFrame({'Predicted_Sex': PredictedSex})

    data2 = pd.concat([data, Predicted_Sex], axis=1)

    return data2


def main():

    args = parse_args()

    data = pd.read_csv(args.input_data, sep='\t')

    f_cutoff, m_cutoff = get_cutoffs(args)

    data2 = Predict_Sex(data, f_cutoff, m_cutoff)

    # replace over existing file
    data2.to_csv(args.input_data, sep='\t', index=False, header =True)


if __name__ == "__main__":

    main()
