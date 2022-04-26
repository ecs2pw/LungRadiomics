# Process

These files are used to extract the radiomic features from a set of scans.  Much of this code was adapted from John Matter's work and wasn't written by me.  As such a lot of this code is very finicky and breaks easily.  I admit that I don't know what all of the called python files are used for, but below is a short list of instructions for how to use them on a patient.

This code expects the patient's files to be organized in the following file structure:
* XX [Patient's initials]
  * Pre
  * PreN1
  * PreN2
  * PreN[x for previous scan number x]

Within each of these folders should be all of the .dcm scan slices for each timestep, with file names starting with 'CT'.  Additionally in each folder should be a .dcm file containing the structure set for the scan with file name starting with 'struct_set'.

In order for the feature extraction to work as intended, the structure sets for each patient must be labeled somewhat specifically; the ITV and PTV should be named 'ITV' and 'PTV' respectively, while the random ROIs should be named 'Random_ITV' and 'Random_PTV'.  As far as I know capitalization should not matter here.

Assuming all of these things are set up correctly, running a patient should be as simple as calling `python run.py XX` with XX being the patients initials.  If everythings works (horray!) the program should write four .csv spreadsheets in the patient's directory, one for each of the IT, PTV, Random ITV, and random PTV.  These spreadsheets should have the name of each radiomic feature in the first collumn, the name of the scan (Pre, PreN1, ...) on each row, and the scan's corresponding feature value in every square in between.

Note that most code files are expecting to find the patient's in the directory /nv/vol141/phys_nrf/Emery/dataset, if your scans are somewhere else then you will need to go into each file and change the patients_dir variable accordingly.

