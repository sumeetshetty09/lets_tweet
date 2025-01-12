import os

# Define paths
paths = [
    'lets_tweet/management/__init__.py',
    'lets_tweet/management/commands/__init__.py'
]

# Create directories and files
for path in paths:
    os.makedirs(os.path.dirname(path), exist_ok=True)  # Create directories if not exist
    with open(path, 'w'):  # Create empty file
        pass

print("Directories and files created successfully.")
