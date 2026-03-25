import re
from utils import data_missing_empty_neg_nan, invalid_date, normalize_text, is_missing_or_empty, convert_to_date

def clean_row(row, stats):
    """
    Cleans a single row of data. Returns a cleaned list of values or None if the row should be discarded.
    Updates the stats object with counts of discarded and corrected entries.
    """

    stats.total_input_rec += 1
   # Check if the row has at least 5 columns
    if len(row) < 5:
        return None
    # Extract the relevant columns
    series_name, season_number, episode_number, episode_title, air_date = row[0], row[1], row[2], row[3], row[4]

    # Clean series name
    if is_missing_or_empty(series_name):
        stats.discarded_entries['no_series_name'] += 1
        return None
    else:
        series_name = normalize_text(series_name)
    
    # Clean season number
    if data_missing_empty_neg_nan(season_number):
        season_number = 0
        stats.corrected_entries['season_number'] += 1
    else:
        # For cases such as "1.0", "2.0". If it is a decimal like "1.5", it will be considered invalid and set to 0
        try:
            season_number = int(float(season_number))
        except ValueError:
            season_number = 0
            stats.corrected_entries['season_number'] += 1


    # Clean episode number
    if data_missing_empty_neg_nan(episode_number):
        episode_number = 0
        stats.corrected_entries['episode_number'] += 1
    else:
        try:
            episode_number = int(float(episode_number))
        except ValueError:
            episode_number = 0
            stats.corrected_entries['episode_number'] += 1

    # Clean  episode title
    if is_missing_or_empty(episode_title):
        episode_title = "Untitled Episode"
        stats.corrected_entries['episode_title'] += 1
    else:
        episode_title = normalize_text(episode_title)
    
    # Clean air date
    air_date_bool = invalid_date(air_date)
    if is_missing_or_empty(air_date) or air_date_bool:
        air_date = "Unknown"
        stats.corrected_entries['air_date'] += 1
    else:
        air_date = convert_to_date(air_date)

    #Check if air date, episode title and episode number are missing or empty, if so, skip the row
    if (air_date == "Unknown" and episode_title == "Untitled Episode" and episode_number == 0):
        stats.discarded_entries['missing_three_fields'] += 1
        return None

    cleaned = [series_name, season_number, episode_number, episode_title, air_date]

    return cleaned

