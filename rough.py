import pandas as pd
from datetime import datetime

class PreprocessingManager:
    """
    A class to manage preprocessing of customer data linking due dates and associate assignments.

    Attributes:
    customer_due_dates (pd.DataFrame): DataFrame containing customer IDs and their due dates.
    customer_associates (pd.DataFrame): DataFrame linking customer IDs to associates.

    Methods:
    process(): Processes input data to prepare it for workload management.
    """
    def __init__(self, customer_due_dates: pd.DataFrame, customer_associates: pd.DataFrame):
        """
        Initializes the PreprocessingManager with customer due dates and associate assignments.
        """
        self.customer_due_dates = customer_due_dates
        self.customer_associates = customer_associates

    def process(self) -> (dict, pd.DataFrame):
        """
        Processes the input DataFrames to merge and create a dictionary mapping associates to their daily work item arrivals.

        Returns:
        tuple: A tuple containing a dictionary with associate names as keys and dictionaries of day offsets with work item counts as values,
               and the merged DataFrame with additional 'day_offset' column.
        """
        # Merge the two dataframes on the customer_id field
        merged_data = pd.merge(self.customer_due_dates, self.customer_associates, on='customer_id')
        
        # Convert 'due_date' from string to datetime and calculate the number of days from today
        base_date = datetime.today().date()
        merged_data['due_date'] = pd.to_datetime(merged_data['due_date']).dt.date
        merged_data['day_offset'] = (merged_data['due_date'] - base_date).days
        
        # Group by 'associate_name' and count occurrences per 'day_offset'
        associate_arrivals = {}
        for name, group in merged_data.groupby('associate_name'):
            daily_arrivals = group['day_offset'].value_counts().to_dict()
            associate_arrivals[name] = daily_arrivals
        
        return associate_arrivals, merged_data





import json

class WorkloadManager:
    """
    A class to manage workload assignments based on the processing results.

    Attributes:
    associates (dict): Dictionary containing associate details.
    completion_rate (int): Universal completion rate for all associates.
    average_unknown (int): Universal average of unexpected work items.
    planning_horizon (int): Number of days to plan ahead.

    Methods:
    can_assign_new_item(associate_name, arrival_dates): Checks if a new work item can be assigned to an associate.
    """
    def __init__(self, associates: dict, config_path: str):
        """
        Initializes the WorkloadManager with associate details and configuration settings.
        
        Parameters:
        associates (dict): Dictionary with keys as associate names and values as their details.
        config_path (str): Path to the JSON configuration file.
        """
        self.associates = associates
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.completion_rate = config["completion_rate"]
        self.average_unknown = config["average_unknown"]
        self.planning_horizon = config["planning_horizon"]

    def can_assign_new_item(self, associate_name: str, arrival_dates: dict) -> bool:
        """
        Determines whether a new work item can be assigned to an associate without exceeding their capacity.

        Parameters:
        associate_name (str): Name of the associate.
        arrival_dates (dict): Dictionary with days as keys and number of arriving items as values.

        Returns:
        bool: True if the item can be assigned, False otherwise.
        """
        associate = self.associates[associate_name]
        future_workload = associate['current_workload'] + 1
        for day in range(self.planning_horizon):
            new_items_today = arrival_dates.get(day, 0)
            future_workload = min(future_workload - self.completion_rate + new_items_today + self.average_unknown,
                                  associate['capacity'])
            if future_workload > associate['capacity']:
                return False
        return True




from preprocessing_manager import PreprocessingManager
from workload_manager import WorkloadManager
import pandas as pd

class ProgramExecutor:
    """
    Class to execute the entire program by integrating preprocessing and workload management.

    Methods:
    execute(): Executes the preprocessing and assignment and returns results.
    """
    def __init__(self, customer_due_dates: pd.DataFrame, customer_associates: pd.DataFrame, associates: dict, config_path: str):
        """
        Initializes ProgramExecutor with necessary data and configurations.

        Parameters:
        customer_due_dates (pd.DataFrame): DataFrame with customer IDs and due dates.
        customer_associates (pd.DataFrame): DataFrame mapping customers to associates.
        associates (dict): Dictionary with associate workload details.
        config_path (str): Path to configuration file.
        """
        self.preprocessing_manager = PreprocessingManager(customer_due_dates, customer_associates)
        self.workload_manager = WorkloadManager(associates, config_path)

    def execute(self) -> pd.DataFrame:
        """
        Executes the workload assignment process and returns the assignment results.

        Returns:
        pd.DataFrame: DataFrame containing assignment results with customer details and assignment status.
        """
        associate_arrivals, merged_data = self.preprocessing_manager.process()
        merged_data['assigned'] = False
        for associate, arrivals in associate_arrivals.items():
            if self.workload_manager.can_assign_new_item(associate, arrivals):
                merged_data.loc[merged_data['associate_name'] == associate, 'assigned'] = True
        return merged_data[['customer_id', 'due_date', 'associate_name', 'assigned']]



from program_executor import ProgramExecutor
import pandas as pd

# Example Usage
customer_due_dates = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5, 6],
    'due_date': ['2023-11-25', '2023-11-26', '2023-11-25', '2023-11-27', '2023-11-26', '2023-11-27']
})
customer_associates = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5, 6],
    'associate_name': ['John Doe', 'John Doe', 'Jane Smith', 'Jane Smith', 'John Doe', 'Jane Smith']
})
associates = {
    "John Doe": {"current_workload": 10, "capacity": 15},
    "Jane Smith": {"current_workload": 5, "capacity": 10}
}

executor = ProgramExecutor(customer_due_dates, customer_associates, associates, 'config.json')
results_df = executor.execute()
print(results_df)
