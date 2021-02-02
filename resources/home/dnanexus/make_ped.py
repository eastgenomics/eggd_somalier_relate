import pandas as pd
import argparse


def parse_args():
    """Allow arguments from the command line to be given.
    Array of somalier files is needed but
    Reported sex file is not always required

    Returns:
        args: Variable that you can extract relevant
        arguements inputs needed
    """

    parser = argparse.ArgumentParser(
        description='Process an array of somalier files.'
        )

    parser.add_argument(
        '-a', '--array',
        nargs='+',
        required=True,
        help='an array of somalier files'
        )

    args = parser.parse_args()

    print("Inputs are: ", args.array)

    return args


def get_sampleID(args):
    """
    Gets the sampleID from the {sampleID}.somalier files inputted into app.
    """
    samplesID = []

    for a in args.array:
        samplesID.append(a.split(".")[0])

    return samplesID


def known_sex(samplesID):
    """Produce a ped file where sex is extracted from filename

    Args:
        samplesID (list): list of sample names before somalier suffix

    Returns:
        pd dataframe: ped file dataframe
    """

    # Produce a ped file where all sex is known from filename

    # Filter from filenames
    field = samplesID[0].count("_")  # count number of fields there are
    sex_field_index = field - 1  # sex is always second last one in filename
    ReportedSex = [sample.split("_")[sex_field_index] for sample in samplesID]

    # Ped uses number instead of F/M So replace letter with number.
    # Sex code ('1' = male, '2' = female, '0' = unknown)
    ReportedSex = [s.replace('M', '1') for s in ReportedSex]
    ReportedSex = [s.replace('F', '2') for s in ReportedSex]
    ReportedSex = [s.replace('U', '0') for s in ReportedSex]
    print(ReportedSex)

    # sampleID needs to match what is on the vcf so take sampleID only
    samplesID = [sample.split("_")[0] for sample in samplesID]

    FamilyID = samplesID
    PaternalID = [0] * len(samplesID)
    MaternalID = [0] * len(samplesID)
    Sex = ReportedSex
    Phenotype = [-9] * len(samplesID)

    print("--------------Making PED FILE-----------")
    df = pd.DataFrame(
        list(zip(FamilyID, samplesID,  PaternalID,
                MaternalID, Sex, Phenotype)),
        columns=['FID', 'IID', 'PaternalID',
                'MaternalID', 'Sex', 'Phenotype'])
    print(df)

    return df


def main():
    """
    Main function to produce input sample's ped file.
    """
    args = parse_args()

    samplesID = get_sampleID(args)

    df = known_sex(samplesID)

    df.to_csv('Samples.ped', sep="\t", index=False, header=False)


if __name__ == "__main__":

    main()
