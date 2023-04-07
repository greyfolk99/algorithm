import os
import re
from collections import OrderedDict

def get_readme_dir(problem_dir:str):
    return os.path.join(problem_dir.path, 'README.md')

def get_last_line(dir:str):
    with open(dir, 'r', encoding='utf-8') as f:
        return f.read().strip().split('\n')[-1]

# problem_dict = { platform_name, [titles] }
# algorithm_dict = { algorithm_type, score }
def pre_process(directory, problem_dict:dict={}, algorithm_dict:dict={}):
    regex = r'@([\w-]+)'
    # platform
    for platform_dir in os.scandir(directory):
        platform_name = platform_dir.name.capitalize()
        # problems
        problem_titles = []
        for problem_dir in os.scandir(platform_dir.path):
            readme_dir = get_readme_dir(problem_dir)
            problem_title = problem_dir.name
            problem_titles.append(problem_title)
            last_line = get_last_line(readme_dir)
            # tags
            for tag in re.finditer(regex, last_line):
                algorithm_tag = tag.group(1)
                algorithm_dict[algorithm_tag] = algorithm_dict.get(algorithm_tag, 0) + 1
        problem_dict[platform_name] = problem_titles
    return algorithm_dict, problem_dict

# get last day that was recorded in README
def get_last_day(readme_dir:str):
    with open(readme_dir, 'r', encoding='utf-8') as f:
        file_contents = f.read()
    # Extract the current day number from the section header
    section_header_regex = r'## Day (\d+)'
    match = re.search(section_header_regex, file_contents)
    if match:
        last_day = int(match.group(1))
    else:
        last_day = 1
    return last_day

# markdown lines of rows of present with '■' as many as 'score'
def stack_rows(algorithm_dict:dict):
    sorted_scores = dict(sorted(algorithm_dict.items(), key=lambda item: item[1], reverse=True))
    return '\n'.join([f"| {algorithm_name} | {'■' * score} |" for algorithm_name, score in sorted_scores.items()])

# markdown lines grouped by platform, with links of subdir in repository
def problem_lines_grouped_by_platform(problem_dict:dict):
    line_list = []
    platform_keys = sorted(problem_dict.keys())
    for platform_name in platform_keys:
        line_list.append(f'> {platform_name} :\n')
        problem_list = problem_dict[platform_name]
        for problem in problem_list:
            title = problem.replace('-', ' ').title()
            line_list.append(f'- [{title}](https://github.com/greyfolk99/algorithm/tree/main/notes/{platform_name.lower()}/{problem.replace(" ","%20")})\n')
    return '  '.join(line_list)

# generate formatted readme
def readme(new_day:int, algorithm_dict:dict, problem_dict:dict):
    return \
    f'''
# Algorithm Stacks Updater  

This collects all algorithm stacks by reading last lines of README.md files in subdirectories, that have prefixes of '@'  

ex) @stack @singly-linked-list @sliding-window  
  
### Day {new_day}  
| Algorithms |      Stack      |
|-----------|------------------|
{stack_rows(algorithm_dict)}

### Problem List  
{problem_lines_grouped_by_platform(problem_dict)}  
'''

# main method
def main():
    # parse data from root directory ('.\\notes')
    algorithm_dict, problem_dict = pre_process('.\\notes')
    # get new day
    main_readme_dir = 'README.md'
    new_day = get_last_day(main_readme_dir) + 1
    # update main README file
    with open(main_readme_dir, 'w', encoding='utf-8') as f:
        f.write(readme(new_day, algorithm_dict, problem_dict))
    # push to git
    os.system('git pull origin main')
    os.system('git add .')
    os.system('git commit -m "Day {new_day} Update"')
    os.system('git push origin main')
main()