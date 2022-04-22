import argparse, os, subprocess

patients_dir="/nv/vol141/phys_nrf/Emery/dataset/rider/"

parser = argparse.ArgumentParser()
parser.add_argument('patient', type=str, help='ID of the patient')
args = parser.parse_args()

patients = os.listdir(patients_dir+"Segs")
print(patients)
patient_name = "RIDER-"+args.patient


try:
	folders = sorted(os.listdir(patients_dir+"LungCT/"+patient_name))
except:
	print("Couldn't find patient directory at",patients_dir+"LungCT/"+args.patient)
	exit(1)

for folder in folders:
	print("Preprocessing","RIDER-"+args.patient+"/"+folder)
	subprocess.call(("./preprocess.sh", "RIDER-"+args.patient+"/"+folder))

#subprocess.call(("python", "get_numpy.py", args.patient))
