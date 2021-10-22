import pandas as pd
import argparse
import re

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


def make_ped(samplesID):
    """Produce a ped file where sex is extracted from filename

    Args:
        samplesID (list): list of sample names before somalier suffix

    Returns:
        pd dataframe: ped file dataframe
    """

    # Produce a ped file where all sex is known from filename
    # Not all file names are same length, some filenames are longer so to
    # keep each field/length different, we need to loop over each sampleID

    reported_sex = []
    sex_pattern = re.compile("-[FMUN]?-EGG[0-9]{1,2}")

    # Filter from filenames
    for sample in samplesID:
        match = re.search(sex_pattern, sample)
        if match:
            sex_char = match.group(0).split('EGG')[0]
            if sex_char == "--":
                # missing identifier, set to N
                sex_char = "N"
            else:
                # real id, get middle character
                sex_char = sex_char.strip('-')
        else:
            # no match => name bad or not expected to have one
            sex_char = "N"

        reported_sex.append(sex_char)

    # Need to include check that that the second last column in filename
    # only has phenotypic sex: F/M/U/N
    # If it has another character, such as FHC in FH assays, then change
    # it to N (None)

    # check that its not the other identifier in there - we can
    # say value in list greater than one is not a phenotype sex identifier

    print("Checking values")

    for index, letter in enumerate(reported_sex):
        if len(letter) != 1:
            print("Length of phenotypic sex is not one. "
                "Length of provided phenotypic sex is {}. "
                 .format(len(letter)) + 
                "Provided sex is: {}".format(letter))
            reported_sex[index] = "N"

    print("Finished checking")
    print(reported_sex)

    # Ped uses number instead of F/M So replace letter with number.
    # Sex code ('0' = unknown, '1' = male, '2' = female, '3' = none)
    # Normally ped files do not have unknown 'None' but need this for
    # cases where sample sex is not provided. '3' = None.
    # relate2multiqc will reformat original_pedigree_sex to differentiate
    # 0 = "unknown" and 3 = "none"
    reported_sex = [s.replace('U', '0') for s in reported_sex]
    reported_sex = [s.replace('M', '1') for s in reported_sex]
    reported_sex = [s.replace('F', '2') for s in reported_sex]
    reported_sex = [s.replace('N', '3') for s in reported_sex]
    print(reported_sex)

    # Prepare each column of the ped file by creating lists
    FamilyID = samplesID
    PaternalID = [0] * len(samplesID)
    MaternalID = [0] * len(samplesID)
    Sex = reported_sex
    Phenotype = [-9] * len(samplesID)

    print("--------------Making PED FILE-----------")
    # Combine lists into a dataframe
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

    df = make_ped(samplesID)

    df.to_csv('Samples.ped', sep="\t", index=False, header=False)


if __name__ == "__main__":

    main()
