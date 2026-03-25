import csv
import re
import math
from datetime import datetime

# ------ from main.py ------ 
def get_header_and_dialect(file):
    """
    Analyzes the CSV file to detect its dialect and the presence of a header.
    """
    with open(file, 'r', encoding="utf-8", errors="replace") as f:  
        # Grab a sample of the file and detect header and dialect with Sniffer
        sample = f.read(4096)  
        sniffer = csv.Sniffer()
        try:
            has_header = sniffer.has_header(sample)
            first_line = sample.splitlines()[0].lower()
            if "seriesname" in first_line or "episodetitle" in first_line:
                has_header = True

            dialect = sniffer.sniff(sample)
        except csv.Error:
            # if sniffing fials, assume default dialect and header exists
            has_header = True
            dialect = csv.get_dialect('excel')
        # Reset the file pointer to the beginning of the file
        f.seek(0)

        return dialect, has_header


#--------- from cleaners.py ---------#
def data_missing_empty_neg_nan(value):
    """
    Checks if a numeric value (like Season or Episode number) is invalid.
    Invalid cases: missing, empty, negative or not a number.
    """
    # Check if value is None 
    if value is None or value.strip().lower() == "":
        return True
    # Check if value is a number and if it is negative, decimal or NaN
    try:
        num = float(value)
        if math.isnan(num) or num < 0:
            return True
        if num != int(num):
            return True
        return False
    except ValueError:
        return True
    
def invalid_date(value):
    """
    Validates if the provided string is a valid date within a logical range.
    Range: From the first TV show (1927) to the current year.
    """

    MIN_YEAR = 1927 # The year of the first TV show
    MAX_YEAR = datetime.now().year # The current year

    # Check if it is valid date in the format YYYY-MM-DD
    if value is None or value.strip() == "":
        return True
    try:
        fecha = datetime.strptime(value, '%Y-%m-%d')
        # Check if date is "0000-00-00", if the date is too long ago or greater than current year
        if fecha.year == 0 or fecha.month == 0 or fecha.day == 0:
            return True
        if fecha.year < MIN_YEAR or fecha.year > MAX_YEAR:
            return True
        return False
    except ValueError:
        return True

def convert_to_date(value):
    """
    Converts a valid date string into a date object.
    Returns None if conversion is not possible.
    """
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        return None

def normalize_text(text):
    """
    Standardizes text by converting to lowercase, removing special characters,
    and collapsing multiple spaces into one.
    """
    if text is None:
        return ""
    # Convert to lowercase, remove special characters and extra spaces   
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9áéíóúüñ\s]', '', text)
    return ' '.join(text.split())

def is_missing_or_empty(value):
    """
    Simple check to see if a string value is empty.
    """
    return value is None or value.strip() == ""
