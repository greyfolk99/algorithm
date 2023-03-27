import os
import re
from collections import OrderedDict

# Define data
algorithms = {}
problem_list = []

# Define a regular expression to match the algorithm names in the last line of the README.md files
regex = r'@([\w-]+)'


# Define a recursive function to search for README.md files in subdirectories
def search_for_readme_files(directory):
    for platform_dir in os.scandir(directory):
        platform_name = platform_dir.name.capitalize()
        problem_list.append(f'> {platform_name} :\n')
        for problem_dir in os.scandir(platform_dir.path):
            title = problem_dir.name.replace('-', ' ').title()
            problem_path = os.path.join('.', 'notes', platform_dir.name, problem_dir.name)
            problem_list.append(f'- [{title}](https://github.com/greyfolk99/algorithm/{problem_dir.name})\n')
            readme_path = os.path.join(problem_dir.path, 'README.md')
            with open(readme_path, 'r', encoding='utf-8') as f:
                last_line = f.read().strip().split('\n')[-1]
                for match in re.finditer(regex, last_line):
                    algorithm_tag = match.group(1)
                    algorithms[algorithm_tag] = algorithms.get(algorithm_tag, 0) + 1


# Call the recursive function to search for README.md files in subdirectories
search_for_readme_files('.\\notes')

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
sorted_scores = dict(sorted(algorithms.items(), key=lambda item: item[1], reverse=True))
algorithm_stack_str = ''.join([f"| {algorithm} | {'■' * score} |\n" for algorithm, score in sorted_scores.items()])

# Generate the final output string
i = 1
readme = \
    f'''
# Algorithm Stacks Updater

- This collects all algorithm stacks by reading last lines of README.md files in subdirectories, that have prefixes of @

### Day {new_day}
| Algorithms |      Stack      |
|-----------|------------------|
{algorithm_stack_str}

### Problem List
{'  '.join(problem_list)}

'''

# Write the updated contents to the file
with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)


os.system('git pull origin main')
os.system(f'git add .')
os.system(f'git commit -m "Day {new_day} Update"')
os.system('git push origin main')
