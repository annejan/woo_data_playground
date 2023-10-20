import argparse
import pandas as pd

def combine_and_sort_csv(file_names, output_file):
    dataframes = []
    
    for file_name in file_names:
        df = pd.read_csv(file_name)
        dataframes.append(df)

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.groupby(['Text', 'Tag'])['Count'].sum().reset_index()
    combined_df = combined_df.sort_values(by='Count', ascending=False)
    combined_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combine and sort CSV files')
    parser.add_argument('input_files', nargs='+', help='Input CSV files to combine')
    parser.add_argument('--output', default='combined_and_sorted.csv', help='Output CSV file name (default: combined_and_sorted.csv)')

    args = parser.parse_args()
    combine_and_sort_csv(args.input_files, args.output)
