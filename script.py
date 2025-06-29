import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
from collections import defaultdict
from datetime import datetime, timedelta

def read_filters_from_csv(file_path):
    filters_dict = defaultdict(list)
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            center = row['center']
            filter_value = row['filter']
            filters_dict[center].append(filter_value)
    return dict(filters_dict)

def read_logs_in_date_range(start_date, end_date):
    date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
    all_data = pd.DataFrame()

    for single_date in date_range:
        file_name = f'incron_log_{single_date.strftime("%Y-%m-%d")}'
        if os.path.isfile(file_name):
            df = pd.read_csv(file_name, header=None, names=['File_ID', 'Timestamp'])
            df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
            all_data = pd.concat([all_data, df], ignore_index=True)

    return all_data

def filter_data(data, filters_dict):
    filtered_data = data.copy()
    filtered_data['Center'] = filtered_data['File_ID'].apply(lambda x: next((key for key, values in filters_dict.items() if any(val in x for val in values)), None))
    return filtered_data.dropna(subset=['Center'])

def generate_plots(filtered_data, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    summary_stats = []
    centers = filtered_data['Center'].unique()

    for center in centers:
        center_data = filtered_data[filtered_data['Center'] == center]
        daily_counts = center_data.groupby('Date').size().reset_index(name='Count')

        # Debugging: Print the intermediate data
        print(f"Center: {center}")
        print(daily_counts)

        plt.figure(figsize=(12, 6))
        plt.bar(daily_counts['Date'].astype(str), daily_counts['Count'], width=0.8)
        plt.xlabel('Date')
        plt.ylabel('Count')
        plt.title(f'Log Counts for {center}')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plot_file = os.path.join(output_dir, f'{center}_barplot.png')
        plt.savefig(plot_file)
        plt.close()

        total_count = daily_counts['Count'].sum()
        summary_stats.append({'Center': center, 'Total Count': total_count, 'Days Counted': len(daily_counts)})

    stats_df = pd.DataFrame(summary_stats)
    stats_df.to_csv(os.path.join(output_dir, 'statistics_summary.csv'), index=False)

def main():
    parser = argparse.ArgumentParser(description='Process log files for a date range.')
    parser.add_argument('start_date', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('end_date', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('filters_csv', type=str, help='Path to the CSV file with filters')
    parser.add_argument('output_dir', type=str, help='Directory to save the plots and summary statistics')

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d')

    filters_dict = read_filters_from_csv(args.filters_csv)
    logs_data = read_logs_in_date_range(start_date, end_date)

    # Debugging: Print the logs data
    print("Logs Data:")
    print(logs_data.head())

    filtered_data = filter_data(logs_data, filters_dict)

    # Debugging: Print the filtered data
    print("Filtered Data:")
    print(filtered_data.head())

    generate_plots(filtered_data, args.output_dir)

if __name__ == "__main__":
    main()

