# Py-arn

# Requirements
You must have python 3.8.5 installed on your system
You must have install all python packages present in requirements.txt

# Script
You will find multiple script on this repo.

`compare_complementary_arn.py`
This script will compare the arn on complementary method with add space. Example:

Sequence1=ACGU

Sequence2=GGGC

AddSpace1=True

For this example, the char `_` represent a ` ` space.

ACGU compare to GGGC
None
C can imbricate G
None
None



_ACGU compare to GGGC
None
None
None
None



__ACGU compare to GGGC
None
None
None
G can imbricate C



`compare_loop_arn.py` 

`generate_permutations_arn.py`
This script will generate all possible of permutations of arn.
The file will contains data like this =>

A0C1G2U3
A0C1U3G2

These values describe nucleotides and original position in the arn.

`compare_position_arn.py`
This script will just compare the arn positions.

Example:

Sequence1=ACUGU
Sequence2=UGUAC

Size is same
A is different of U
C is different of G


# How-to use

To use script you can get help from command line with =>
`python compare_position_arn.py --help`

`python compare_loop_arn.py --help`

`python compare_complementary_arn.py --help`

`python generate_permutations_arn.py --help`

The script will be create/override a file named result.txt which it contains logs of the script.
You can see output of the script in standard output (terminal) if you use the `verbose` argument

