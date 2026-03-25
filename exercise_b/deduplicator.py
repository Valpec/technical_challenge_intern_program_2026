def episode_score(episode):
    """
    Calculate a score for the episode based on priority of fields
    The score is used to determine which episode to keep when duplicates are found.
    
    Priority: Valid Air Date > Specific Title > Known Season/Episode.
    """ 
    score = 0
    if episode.air_date != "Unknown":
        score += 3
    if episode.episode_title != "Untitled Episode":
        score += 2
    if episode.episode_number != 0 and episode.season_number != 0:
        score += 1
    return score


def get_duplicate_keys(episode):
    """
    Generates identifying keys based on predefined rules to detect duplicates.
    """
    ser_name = episode.series_name 
    seas_num = episode.season_number
    e_num = episode.episode_number
    e_title = episode.episode_title

    keys = []
    if seas_num != 0 and e_num != 0:
        # Rule 1: (SeriesName_normalized, SeasonNumber, EpisodeNumber)
        keys.append((ser_name, seas_num, e_num))
    
    elif seas_num == 0 and e_num != 0:
        # Rule 2: (SeriesName_normalized, 0, EpisodeNumber, EpisodeTitle)
        keys.append((ser_name, 0, e_num, e_title))
    
    elif e_num == 0 and seas_num != 0:
        # Rule 3: (SeriesName_normalized, SeasonNumber, 0, EpisodeTitle)
        keys.append((ser_name, seas_num, 0, e_title))
 
    return keys


def deduplicate_episodes(episodes, stats):
    """
    Processes a list of episodes to remove duplicates and keep only the highest-quality records.
    """
    # Dictionary to store each episode key and its index in the unique_episodes array. This allows us to quickly find duplicates and update them if we find a better episode. 
    key_to_index = {} 
    # Array, stores the best episodes found so far.
    unique_episodes = []

    for episode in episodes:
        # Generate the keys for the episode based on the rules set in the problem statement.
        keys = get_duplicate_keys(episode)

        # Check if any key already exists in the key_to_index dictionary. If it does, it means it is a duplicate. 
        existing_index = None
        for key in keys:
            if key in key_to_index:
                existing_index = key_to_index[key]
                break
        if existing_index is None:
            # No duplicate found, add as new
            idx = len(unique_episodes)
            unique_episodes.append(episode)
            for key in keys:
                key_to_index[key] = idx
        else:
            # Duplicate found, compare scores
            stats.duplicates += 1
            existing_episode = unique_episodes[existing_index]
            if episode_score(episode) > episode_score(existing_episode):
                unique_episodes[existing_index] = episode
                for key in keys:
                    key_to_index[key] = existing_index

    return unique_episodes