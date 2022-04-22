import nrrd
import argparse
import numpy as np
import os
import pickle
import radiomics
import pandas as pd

patients_dir="/nv/vol141/phys_nrf/Emery/dataset/"
ct_name="ct_img.nrrd"

parser = argparse.ArgumentParser()
parser.add_argument('patient', type=str, help='Initials of the patient')
args = parser.parse_args()
extractor = radiomics.featureextractor.RadiomicsFeatureExtractor()

dataFrames={}
mask_timesteps={}

try:
	timesteps=next(os.walk(patients_dir+args.patient))[1]
except:
	print("Couldn't find patient directory at",patients_dir+args.patient)
	exit(1)

for timestep in timesteps:
	data=dict()
	mask_radiomics=dict()
	timestep_dir=patients_dir+args.patient+"/"+timestep+"/"

	#Read raw image
	try:
		data['ct_img']=nrrd.read(timestep_dir+ct_name)[0]
	except Exception as e:
		print("Couldn't find nrrd file at",timestep_dir+ct_name)
		continue

	print("Formatting timestep",timestep)

	
	#Read masks and radiomics
	for mask_file in os.listdir(timestep_dir+"masks"):
		if mask_file.endswith(".nrrd"):
			print("Applying mask",mask_file)
			mask=nrrd.read(timestep_dir+"masks/"+mask_file)[0]
			data["mask_"+mask_file[:-5]]=mask
			radiomicFeatures=extractor.execute(timestep_dir+"ct_img.nrrd", timestep_dir+"masks/"+mask_file)
			mask_radiomics["mask_"+mask_file[:-5]]=radiomicFeatures

			df=pd.DataFrame.from_dict({i:str(radiomicFeatures[i]) for i in radiomicFeatures}, orient='index')
			if not mask_file[:-5] in dataFrames:
				dataFrames[mask_file[:-5]] = [df]
				mask_timesteps[mask_file[:-5]]=[timestep]
			else:
				dataFrames[mask_file[:-5]].append(df)
				mask_timesteps[mask_file[:-5]].append(timestep)

	with open(timestep_dir+"Raw_CT.pickle",'wb') as file:
		pickle.dump(data, file)
	print("Saved scan to",timestep_dir+"Raw_CT.pickle")
	with open(timestep_dir+"Mask_Radiomics.pickle",'wb') as file:
		pickle.dump(mask_radiomics, file)
	print("Saved radiomics to",timestep_dir+"Mask_Radiomics.pickle")

	
#Create CSV
for mask in dataFrames:
	dataFrames[mask] = pd.concat(dataFrames[mask], axis=1)
	dataFrames[mask].columns = mask_timesteps[mask]
	with open(patients_dir+args.patient+"/"+mask+".csv",'w') as file:
		file.write(dataFrames[mask].to_csv())
	print("Saved mask radiomic data to csv.")
