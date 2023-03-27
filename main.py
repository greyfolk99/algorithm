import os
import re
from datetime import datetime

# Define a dictionary to store the algorithm scores
scores = {}

# Define a regular expression to match the algorithm names in the last line of the README.md files
regex = r'@([\w-]+)'


# Define a recursive function to search for README.md files in subdirectories
def search_for_readme_files(directory):
    for entry in os.scandir(directory):
        if entry.is_file() and entry.name == 'README.md':
            with open(entry.path, 'r', encoding='utf-8') as f:
                last_line = f.read().strip().split('\n')[-1]
                for match in re.finditer(regex, last_line):
                    algorithm = match.group(1)
                    scores[algorithm] = scores.get(algorithm, 0) + 1
        elif entry.is_dir():
            search_for_readme_files(entry.path)


# Call the recursive function to search for README.md files in subdirectories
search_for_readme_files('.')

# Read the current contents of the file
with open('README.md', 'r', encoding='utf-8') as f:
    file_contents = f.read()

# Extract the current day number from the section header
section_header_regex = r'## Day (\d+)'
match = re.search(section_header_regex, file_contents)
if match:
    current_day = int(match.group(1))
else:
    current_day = 1
new_day = current_day + 1

# Sort the scores dictionary in descending order by value
sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
algorithm_scores_str = ''.join([f"| {algorithm} | {'■' * score} |\n" for algorithm, score in sorted_scores.items()])

# Generate the final output string
i = 1
readme = \
    f'''
# Algorithm Stacks Updater

Collects all algorithm stacks from the repositories with prefix of @

## Day {new_day}
| Algorithms | Stack |
|-----------|-------|
{algorithm_scores_str}
'''


# Write the updated contents to the file
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

os.system('git pull origin main')
os.system(f'git add .')
os.system(f'git commit -m "Day {new_day} Update"')
os.system('git push origin main')