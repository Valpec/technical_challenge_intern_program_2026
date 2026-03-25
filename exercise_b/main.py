"""
The Streaming Sevices's Lost Episodes Challenge
------------------------
This script reads a CSV file containing the catalog of series of a streaming service. It cleans and normalizes
the records, removes duplicates, and writes the results to a new CSV file.
A report with cleaning statistics is generated in the output folder.

Output:
    - output/cleaned_episodes.csv  → cleaned and deduplicated records
    - output/report.md             → cleaning statistics and deduplication strategy

Usage:
    python main.py
    → You will be prompted to enter the path to the input CSV file.

"""

import csv
import os
from utils import get_header_and_dialect
from cleaners import clean_row
from deduplicator import deduplicate_episodes
from models.episode import Episode
from models.report_stats import ReportStats


def get_io_streams(input_file, output_file):
    """
    Validates the input file and initializes CSV reader and writer objects.
    """
    if os.path.getsize(input_file) == 0:
        raise ValueError("The input file is empty.")
    # Get the header and dialect of the input file
    dialect, has_header = get_header_and_dialect(input_file)

    # Open the input and output files
    raw_file = open(input_file, 'r', encoding="utf-8", errors="replace")
    clean_file = open(output_file, 'w', encoding="utf-8", newline='')

    reader = csv.reader(raw_file, dialect=dialect)
    writer = csv.writer(clean_file)

    if has_header:
            next(reader) # Skip the header row if it has one

    return raw_file, clean_file, reader, writer

def process_rows(reader, writer, ):
     """
    Processes each row: cleans data, creates Episode objects, 
    removes duplicates, and writes the final output.
    """
     
     headers = ['SeriesName', 'SeasonNumber', 'EpisodeNumber', 'EpisodeTitle', 'AirDate']
     writer.writerow(headers)  # Write the headers to the output file
    # Create ReportStats object to keep track of the statistics of the cleaning process. This will be used to generate the report at the end.
     stats = ReportStats()
     episodes = []
     for row_list in reader:
            cleaned_data = clean_row(row_list, stats)
            # If the series name is missing or empty, skip the row
            if cleaned_data is None:
                continue    

            new_episode = Episode(*cleaned_data)
            episodes.append(new_episode)
            
     unique_episodes = deduplicate_episodes(episodes, stats)
     unique_episodes.sort(key=lambda ep: (ep.series_name, ep.season_number, ep.episode_number))
     for episode in unique_episodes: 
        # Write the cleaned data to the output file
        writer.writerow(episode.to_list())
        # Generate report
     stats.generate_report()

def main():
    """
    Entry point of the script. Handles user input and orchestrates the cleaning process.
    """
    # Input file path from the user
    input_file = input("Enter the path to the CSV file: ").strip()
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return
    # Output file saved to the 'output' folder
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Set the output path inside the 'output' folder
    output_file = os.path.join(output_dir, 'cleaned_episodes.csv')
    raw_f, clean_f, reader, writer = None, None, None, None

    try:
        raw_f, clean_f, reader, writer = get_io_streams(input_file, output_file)
        process_rows(reader, writer)
        print(f"Process completed successfully. Cleaned data saved to: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if raw_f:
            raw_f.close()
        if clean_f:
            clean_f.close()


if __name__ == "__main__":
    main()  