import pandas as pd
import os
import logging
from .util import Constants

class DataLoader:
    def __init__(self):
        self.data_dir = Constants.DATA_DIRECTORY
        self.prefixes = Constants.FILE_PREFIXES
        self.open_work_items = None
        self.office_pod_mapping = None
        self.value_data = None
        self.historical_assignments = None

    def load_data(self):
        for key in self.prefixes:
            data = self._load_single_file(key)
            if data is not None:
                setattr(self, key, data)
                logging.info(f"{key} loaded successfully.")
            else:
                logging.warning(f"No data loaded for {key}.")

    def _load_single_file(self, key):
        prefix = self.prefixes.get(key)
        matching_files = [f for f in os.listdir(self.data_dir) if f.startswith(prefix) and f.endswith('.csv')]
        if len(matching_files) > 1:
            logging.error(f"Multiple files found with the prefix '{prefix}' in {self.data_dir}.")
            return None
        elif not matching_files:
            logging.warning(f"No file matching the prefix '{prefix}' was found in {self.data_dir}")
            return None

        full_path = os.path.join(self.data_dir, matching_files[0])
        try:
            return pd.read_csv(full_path)
        except Exception as e:
            logging.error(f"An error occurred while loading data from {full_path}: {e}")
            return None

    def check_advisor_assignments(self):
        if self.open_work_items is None or self.office_pod_mapping is None or self.value_data is None:
            logging.error("Required datasets are not loaded.")
            return
        
        # Assign gsp_type based on advisor presence
        self.open_work_items['gsp_type'] = self.open_work_items['advisor_id'].apply(
            lambda x: 'fc/vpfc' if x in self.office_pod_mapping['advisor'].values else 'imc'
        )

        # Merge customer values into open_work_items
        self.merge_customer_values()

        logging.info("Advisor assignments and customer values updated in open_work_items.")

    def merge_customer_values(self):
    """
    Merges customer value into open_work_items using the 'id' column from open_work_items
    and 'unique_id' from value_data. This method handles missing values by setting them to zero.
    """
    if 'id' not in self.open_work_items or 'unique_id' not in self.value_data:
        logging.error("Required columns for merging are not present in the dataframes.")
        return

    # Perform the merge operation using left join
    self.open_work_items = self.open_work_items.merge(
        self.value_data[['unique_id', 'customer_value']],
        left_on='id',
        right_on='unique_id',
        how='left'
    )

    # Optionally, handle missing values in 'customer_value' if necessary
    self.open_work_items['customer_value'].fillna(0, inplace=True)

    logging.info("Customer values successfully merged into open_work_items DataFrame.")

if __name__ == "__main__":
    from logging_config import setup_logging
    setup_logging()
    loader = DataLoader()
    loader.load_data()
    loader.check_advisor_assignments()
    # Optionally save the updated DataFrame
    loader.open_work_items.to_csv(os.path.join(loader.data_dir, 'updated_open_work_items.csv'), index=False)
    logging.info("Updated open_work_items saved.")


import logging
import os
from datetime import datetime

def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"assignment_engine_{timestamp}.log"
    log_file_path = os.path.join(log_dir, log_file_name)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
                        handlers=[
                            logging.FileHandler(log_file_path),
                            logging.StreamHandler()  # To output to the console as well
                        ])
    logging.info("Logging setup complete.")

class Constants:
    """
    A class to store all constant values, including file prefixes and the directory for data files.
    """
    DATA_DIRECTORY = 'data/'
    FILE_PREFIXES = {
        'open_work_items': 'open_work_items',
        'value_data': 'value_data',
        'office_pod_mapping': 'office_pod_mapping',
        'historical_assignments': 'historical_assignments'
    }
