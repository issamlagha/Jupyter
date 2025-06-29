import pandas as pd
import argparse
from datetime import datetime, timedelta

def process_file(file_path):
    df = pd.read_csv(file_path, delimiter=',', header=None, names=['Filename', 'Timestamp'])
    df[['File_ID', 'Center', 'Additional_Info', 'Number1', 'Number2', 'Number3']] = df['Filename'].str.split('_', expand=True)
    df = df.drop(columns=['Filename'])
    return df

def process_date_range(start_date, end_date):
    date_format = "%Y-%m-%d"
    start = datetime.strptime(start_date, date_format)
    end = datetime.strptime(end_date, date_format)
    
    all_data = []
    
    current_date = start
    while current_date <= end:
        file_name = f'incron_log_{current_date.strftime(date_format)}'
        try:
            df = process_file(file_name)
            all_data.append(df)
        except FileNotFoundError:
            print(f"File {file_name} not found.")
        current_date += timedelta(days=1)
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print(combined_df)
    else:
        print("No data processed.")

def main():
    parser = argparse.ArgumentParser(description="Process a range of log files.")
    parser.add_argument('start_date', type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument('end_date', type=str, help="End date in YYYY-MM-DD format")
    args = parser.parse_args()
    
    process_date_range(args.start_date, args.end_date)

if __name__ == "__main__":
    main()

