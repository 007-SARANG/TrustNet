# Instagram Auto-Monitoring Configuration

# Add Instagram usernames (without @) to automatically monitor for image-caption mismatches
# Posts from these accounts will be analyzed every 15 minutes

MONITORED_ACCOUNTS = [
    'natgeo',          # National Geographic
    'nasa',            # NASA
    # 'bbcnews',       # BBC News
    # 'cnn',           # CNN
    # 'theonion',      # The Onion (satire - good for testing mismatches)
    
    # Add your custom accounts here:
    # 'username1',
    # 'username2',
]

# Monitoring Settings
CHECK_INTERVAL_MINUTES = 15  # How often to check for new posts (minimum 15 to avoid rate limits)
MAX_POSTS_PER_ACCOUNT = 5    # Number of recent posts to check per account
