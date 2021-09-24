import pandas as pd
import argparse
import string

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

    ReportedSex = []

    # Filter from filenames
    for sample in samplesID:
        field = sample.count("-")  # count number of fields there are
        sex_field_index = field - 1  # sex of sample is always 2nd last
        sex_char = sample.split("-")[sex_field_index]
        # sometimes the sex last field is empty :( 
        # so replace blanks with U for Unknown
        if not sex_char:
            sex_char = 'U'
        ReportedSex.append(sex_char)

    # Need to include check that that the second last column in filename
    # only has phenotypic sex: F/M/U/N

    # check that its not the other identifier in there - we can
    # say value in list greater than one is not a phenotype sex identifier

    for letter in ReportedSex:
        if len(letter) != 1:
            raise Exception("Length of phenotypic sex is not one. "
                            "Length of provided phenotypic sex is {}. "
                            .format(len(letter)) + 
                            "Provided sex is: {}".format(letter))

    # fail if reported sex does includes letter other than F/M/N/U

    unexpected_sex_letters = []
    expected_sex = ['F', 'M', 'U', 'N']

    # string.ascii_uppercase has all the letters in cap in a string so need 
    # to seperate it. Whilst doing that, remove expected sex phenotypes
    for letter in string.ascii_uppercase:
        if letter not in expected_sex:
            unexpected_sex_letters.append(letter)

    # if any phenotypic sex letters is not as expected, raise an expection
    check =  any(item in unexpected_sex_letters for item in ReportedSex)
    if check is True:
        raise Exception("The filename sex phenotypes (non-duplicates) "
                        "{} contains unrecognised inputs. Expectations " 
                        "are: F, M, U, N ".format(list(set(ReportedSex))))    
    else :
        print("Correct sex phenotypes provided {}".format(ReportedSex))

    # Ped uses number instead of F/M So replace letter with number.
    # Sex code ('1' = male, '2' = female, '0' = unknown)
    # Normally ped files do not have unknown 'None' but need this for
    # cases where sample sex is not provided. '3' = None. 
    # relate2multiqc will reformat original_pedigree_sex to differentiate 
    # 0 = "unknown" and 3 = "none"
    ReportedSex = [s.replace('M', '1') for s in ReportedSex]
    ReportedSex = [s.replace('F', '2') for s in ReportedSex]
    ReportedSex = [s.replace('U', '0') for s in ReportedSex]
    ReportedSex = [s.replace('N', '3') for s in ReportedSex]
    print(ReportedSex)

    # Prepare each column of the ped file by creating lists
    FamilyID = samplesID
    PaternalID = [0] * len(samplesID)
    MaternalID = [0] * len(samplesID)
    Sex = ReportedSex
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
