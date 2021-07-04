from modules.DataProcessor import DataProcessor
from sample_data.SampleDataConvection import SampleDataConvection


def main():
	sample_data = SampleDataConvection()

	data_processor = DataProcessor(sample_data)
	data_processor.directory_generator()
	data_processor.update_data()

	data_processor.load_file()


if __name__ == "__main__":
	main()