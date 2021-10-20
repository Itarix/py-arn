# Py-arn

This project was created for iGEM team of GO Paris Saclay 2021.
This tools was used to compare miARN (or ARN).

The project has been uploaded on github because Igem's rule. (FYI. the repo for igem 2021 https://github.com/igemsoftware2021/GO_Paris_Saclay_2021).

If you want other version or want ask/add feature, you can create an issue or PR in this actual repo.

# Requirements

You must have python 3.8.5 installed on your system.
You must have install all python packages present in requirements.txt

# Script

You will find multiple script on this repo.

`complementary_arn.py`
This script will compare the arn on complementary method while adding space. Example:

Sequence1=ACGU

Sequence2=GGGC

AddSpace1=True

For this example, the char `_` represent a ` ` space.

ACGU compare to GGGC None C can imbricate G None None

_ACGU compare to GGGC None None None None

__ACGU compare to GGGC None None None G can imbricate C

`loop_arn.py`
This script will compare the arn and check if the arns can loop together:

`hairpin.py`
This script will calcul the hairpin of the arn.

`generate_permutations_arn.py`

/!\ BETA.
This script will generate all possible of permutations of arn. The file will contains data like this =>

A0C1G2U3 A0C1U3G2

These values describe nucleotides and original position in the arn.

WARNING: Don't use for data size higher than 15.
AGGUCAUCGUCUA is size 13. It will generate 13! possibilities.

More than 15 can take multiples days to process.
More than 20 can take multiples years to process.

`position_arn.py`
This script will just compare the arn positions.

Example:

Sequence1=ACUGU Sequence2=UGUAC

Size is same A is different of U C is different of G

# How-to use

To use script you can get help from command line with =>
`python pyarn/comparison/position_arn.py --help`

`python pyarn/comparison/loop_arn.py --help`

`python pyarn/comparison/complementary_arn.py --help`

`python pyarn/comparison/generate_permutations_arn.py --help`

`python pyarn/comparison/hairpin.py --help`

The script will be create/override a file named result.txt which it contains logs of the script. You can see output of
the script in standard output (terminal) if you use the `verbose` argument

# GUI

To use a GUI, you must launch web server.
To launch this server :

`python pyarn/web/server.py`

Then you can go on `http://127.0.0.1:5000/` with your web browser and GUI work.
