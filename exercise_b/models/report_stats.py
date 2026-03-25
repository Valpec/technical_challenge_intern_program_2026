import os
class ReportStats:
    """
    Tracks and generates statistics for the data cleaning and deduplication process.
    """
    def __init__(self):
        self.total_input_rec = 0
        self.discarded_entries = {
            'no_series_name': 0,
            'missing_three_fields': 0,
        }
        self.corrected_entries = {
            'season_number': 0,
            'episode_number': 0,
            'episode_title': 0,
            'air_date': 0
        }
        self.duplicates = 0
    
    def total_discarded(self):
        """Returns the sum of all records that were removed from the dataset."""
        return sum(self.discarded_entries.values())
    
    def total_corrected(self):
        """Returns the sum of all records that were corrected in the dataset."""
        return sum(self.corrected_entries.values())

    def total_output_rec(self):
        """Calculates the final records"""
        return self.total_input_rec - self.total_discarded() - self.duplicates
    
    def generate_report(self):
        # Create output directory if it doesn't exist
        output_dir = 'output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_path = os.path.join(output_dir, 'report.md')
        image_path = '../assets/deduplication.jpeg'
        print("Generating report...")
        lines = [
            "# Data Cleaning Report",
            "",
            "## Summary",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Total input records     | {self.total_input_rec} |",
            f"| Total output records    | {self.total_output_rec()} |",
            f"| Discarded entries       | {self.total_discarded()} |",
            f"| Corrected entries       | {self.total_corrected()} |",
            f"| Duplicates detected     | {self.duplicates} |",
            "",
            "## Corrections Breakdown",
            f"| Correction | Count |",
            f"|------------|-------|",
            f"| Air date replaced with Unknown       | {self.corrected_entries['air_date']} |",
            f"| Title replaced with Untitled Episode | {self.corrected_entries['episode_title']} |",
            f"| Season number corrected to 0         | {self.corrected_entries['season_number']} |",
            f"| Episode number corrected to 0        | {self.corrected_entries['episode_number']} |",
            "",
            "## Discarded Episodes Breakdown",
            f"| Correction | Count |",
            f"|------------|-------|",
            f"| Missing or empty series name         | {self.discarded_entries['no_series_name']} |",
            f"| Missing Episode Number, Episode Title, and Air Date | {self.discarded_entries['missing_three_fields']} |",
            "",
            "## Deduplication Strategy",
            "Episodes are considered duplicates when they share the same:",
           "- **Rule 1:** `(SeriesName, SeasonNumber, EpisodeNumber)`",
            "- **Rule 2:** `(SeriesName, 0, EpisodeNumber, EpisodeTitle)` (Season is unknown)",
            "- **Rule 3:** `(SeriesName, SeasonNumber, 0, EpisodeTitle)` (Episode number is unknown)",
            "",
            "When duplicates are found, the best record is kept using this priority:",
            "1. Valid air date over Unknown",
            "2. Known episode title over Untitled Episode",
            "3. Valid season and episode number over 0",
            "4. If still tied, the *first record encountered* in the file is kept",
            "",

            "### Implementation Logic",
            "To detect duplicates efficiently, we use a `key_to_index` dictionary that maps keys(applicable rules) to the best episode found so far:",
            "",
            "1. **Generate Keys:** For each normalized record, we generate the applicable keys (Rule 1, 2, or 3).",
            "2. **Lookup:** We check if any of these keys already exist in our dictionary.",
            "3. **Comparison:**",
            "   - **If New:** We add the episode to `unique_episodes` and map all its keys to the new index.",
            "   - **If Duplicate:** We compare the priority score of the new record with the existing one at the stored index. ",
            "       - If the new record is better, we replace the old one and update all associated keys. ",
            "       - If they are tied, we keep the existing one since it was encountered first in the file.",
            "",

            "### Practical Example",
            "#### Input records (normalized and cleaned):",
            "1. `dexter, 0, 1, living the dream, 2010-09-30` → **Added** (Index 0, Rule 2 — season is 0).",
            "2. `dexter, 1, 0, crocodile, 2006-02-04` → **Added** (Index 1, Rule 3 — episode is 0).",
            "3. `dexter, 0, 1, living the dream, 2010-09-30` → **Duplicate** of Index 0 (Rule 2 - season is 0).",
            "When Record 3 is encountered, it generates the same keys, identifies the conflict at Index 0, and since the scores are tied, the original record is kept.",
            "",
        
        
            f"![Explanation:]({image_path})"
        ]
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
        print(f"Report saved to {output_path}")

