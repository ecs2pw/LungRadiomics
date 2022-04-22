import argparse, os, subprocess

patients_dir="/nv/vol141/phys_nrf/Emery/dataset/"

parser = argparse.ArgumentParser()
parser.add_argument('patient', type=str, help='Initials of the patient')
args = parser.parse_args()

try:
	timesteps = sorted(os.listdir(patients_dir+args.patient))
except:
	print("Couldn't find patient directory at",patients_dir+args.patient)
	exit(1)

for timestep in timesteps:
	print("Preprocessing",args.patient+"/"+timestep)
	subprocess.call(("./preprocess.sh", args.patient+"/"+timestep))

subprocess.call(("python", "get_numpy.py", args.patient))
