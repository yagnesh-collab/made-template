import unittest
import os
from unittest.mock import patch

from pipeline import extract_zip, read_and_preprocess, save_to_csv_and_sql

class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = os.path.abspath('test_data')
        os.makedirs(self.test_data_dir, exist_ok=True)

    def tearDown(self):
        os.rmdir(self.test_data_dir)

    def test_data_pipeline(self):
        # Mock the Kaggle API and file download
        with patch('pipeline.KaggleApi') as mock_kaggle_api:  
            mock_api = mock_kaggle_api.return_value
            mock_api.authenticate.return_value = None
            mock_api.dataset_download_file.return_value = None

            print("Running the data pipeline...")
            # Call the pipeline
            os.system('python3 project/pipeline.py')
            print("Data pipeline execution complete.")

            # Check if the output files exist
            self.assertTrue(os.path.exists('data/co2_emission.csv'))
            self.assertTrue(os.path.exists('data/co2_emission.db'))
            self.assertTrue(os.path.exists('data/renewables_data.csv'))
            self.assertTrue(os.path.exists('data/renewables_data.db'))

if __name__ == '__main__':
    unittest.main()
