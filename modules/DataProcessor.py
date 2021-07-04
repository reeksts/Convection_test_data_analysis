import os
import shutil


class DataProcessor:
	def __init__(self, sample_data):
		self.sample_data = sample_data

		self.source_directory_list = [
			'C:\\Users\\karlisr\\OneDrive\\ConvectionCell',
		]

		self.target_directory_list = [
			'C:\\Users\\karlisr\\OneDrive - NTNU\\2_PostDoc_NTNU\\20_convection_experiments\\'
			'01_measured_samples',
		]

		# child folder names:
		raw_data_folder = '01_raw_data'
		measurement_data_folder = '02_measurement_data'
		weight_measurements_folder = '03_weight_measurements'
		other_folder = '04_other'
		pics_folder = '05_pics'
		measurement_figures_folder = '05_measurement_figures'
		self.child_folders = [
			raw_data_folder,
			measurement_data_folder,
			weight_measurements_folder,
			other_folder,
			pics_folder,
			measurement_figures_folder
		]

	def directory_generator(self):
		# iterate over directories in OneDrive/ConvectionCell:

		for source_directory, target_directory in zip(self.source_directory_list, self.target_directory_list):
			for sample_folder in os.listdir(source_directory):

				# Generate sample parent directory:
				parent_directory = os.path.join(target_directory, sample_folder)
				if not os.path.exists(parent_directory):
					os.mkdir(parent_directory)

				# Generate child directories:
				for folder in self.child_folders:
					child_subdirectory = os.path.join(parent_directory, folder)
					if not os.path.exists(child_subdirectory):
						os.mkdir(child_subdirectory)

	def update_data(self):
		for source_directory, target_directory in zip(self.source_directory_list, self.target_directory_list):
			for root, dirs, files in os.walk(source_directory):
				for file in files:
					if len(file) != 0:
						# Getting sample name:
						sample_name = file.split('_')[0]

						# Check if the file exists, copy or replace:
						sample_folder_raw = os.path.join(
							target_directory, sample_name, '01_raw_data')
						sample_folder_csv = os.path.join(
							target_directory, sample_name, '02_measurement_data')

						if file not in os.listdir(sample_folder_raw):
							# Executed when new file is added
							shutil.copy(os.path.join(root, file), sample_folder_raw)
							# Should convert from .lvm to .csv here
							shutil.copy(os.path.join(sample_folder_raw, file), sample_folder_csv)
							name, ext = os.path.splitext(os.path.join(sample_folder_csv, file))
							os.rename(os.path.join(sample_folder_csv, file), name + '.csv')


						else:
							# Executed when file already exists
							src_mod_time = os.stat(os.path.join(root, file)).st_mtime
							trg_mod_time = os.stat(os.path.join(sample_folder_raw, file)).st_mtime
							if src_mod_time - trg_mod_time > 1:
								shutil.copy(os.path.join(root, file), sample_folder_raw)
								shutil.copy(os.path.join(sample_folder_raw, file), sample_folder_csv)
								# Updating csv version of the file:
								name, ext = os.path.splitext(os.path.join(sample_folder_csv, file))
								csv_name = file.split('.')[0] + '.csv'
								if csv_name not in os.listdir(sample_folder_csv):
									os.rename(os.path.join(sample_folder_csv, file), name + '.csv')
								else:
									os.remove(os.path.join(sample_folder_csv, csv_name))
									os.rename(os.path.join(sample_folder_csv, file), name + '.csv')


	def load_file(self):
		for sample in self.sample_data.samples:
			print(sample['sample_name'])