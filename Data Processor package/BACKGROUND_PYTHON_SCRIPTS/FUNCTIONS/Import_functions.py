# This file contains the functions that load and clean the data


# Import statement
import pandas as pd


# Function to load the GNSS data from a file
def load_data(file_path):
    try:
        # Define the columns for the DataFrame
        columns = [
            'GPST', 'latitude(deg)', 'longitude(deg)', 'height(m)', 'Q', 'ns', 'sdn(m)',
            'sde(m)', 'sdu(m)', 'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)', 'ratio'
        ]

        # Load the data immutably
        data = pd.read_csv(file_path, sep='\s+', comment='%', header=None, names=columns)
        data['no.'] = range(1, len(data) + 1)

        return data  # Return the loaded data
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the file: {e}")


# Function to rearrange the data and drop unnecessary columns
def clean_data(data):
    new_order = [
        'GPST', 'no.', 'latitude(deg)', 'longitude(deg)', 'height(m)', 'Q', 'ns', 'sdn(m)',
        'sde(m)', 'sdu(m)', 'sdne(m)', 'sdeu(m)', 'sdun(m)', 'age(s)', 'ratio'
    ]

    data = data.reindex(columns=new_order)
    data_cleaned = data.drop(columns=['ns', 'sdn(m)', 'sde(m)', 'sdu(m)', 'sdne(m)', 'sdeu(m)', 'sdun(m)', 
                                      'age(s)', 'ratio'])
    return data_cleaned