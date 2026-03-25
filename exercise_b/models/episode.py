class Episode:
    """
    Represents a single episode.
    Used to standardize data storage and facilitate 
    sorting and deduplication processes.
    """
    def __init__(self, series_name, season_number, episode_number, episode_title, air_date):
        self.series_name = series_name
        self.season_number = season_number
        self.episode_number = episode_number
        self.episode_title = episode_title
        self.air_date = air_date

    def to_list(self):
        """
        Converts the Episode object attributes into a list format 
        (used for writing the cleaned data back to a CSV file).
        """
        return [self.series_name, 
                self.season_number, 
                self.episode_number, 
                self.episode_title, 
                self.air_date]
    