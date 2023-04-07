import datetime
import os
import re
import urllib.request
import json

username = 'greyfolk99'
repository = 'algorithm'
repository_path = f'https://github.com/{username}/{repository}'

data_structures = []
tag_regex = r'@([\w-]+)'
tag_dict = {}
problem_dict = {}

def get_readme_dir(dir:str):
    return os.path.join(dir.path, 'README.md')

def get_last_line(dir:str):
    with open(dir, 'r', encoding='utf-8') as f:
        return f.read().strip().split('\n')[-1]

def read_base(directory):
    # base
    for data_structure_dir in os.scandir(directory):
        data_structures.append(data_structure_dir.name)
        last_line = get_last_line(get_readme_dir(data_structure_dir))
        for tag in re.finditer(tag_regex, last_line):
            tag_name = tag.group(1)
        tag_dict[tag_name] = tag_dict.get(tag_name, 0) + 1

        
# problem_dict = { platform_name, [titles] }
# algorithm_dict = { algorithm_type, score }
def read_problems(directory):
    # platform
    for platform_dir in os.scandir(directory):
        platform_name = platform_dir.name
        # problems
        problem_titles = []
        for problem_dir in os.scandir(platform_dir.path):
            readme_dir = get_readme_dir(problem_dir)
            problem_title = problem_dir.name
            problem_titles.append(problem_title)
            last_line = get_last_line(readme_dir)
            # tags
            for tag in re.finditer(tag_regex, last_line):
                tag_name = tag.group(1)
                tag_dict[tag_name] = tag_dict.get(tag_name, 0) + 1
        problem_dict[platform_name] = problem_titles

# get last day that was recorded in README
def get_total_committed_day():
    # GitHub API를 이용하여 커밋 기록 가져오기
    url = f'https://api.github.com/repos/{username}/{repository}/commits'
    with urllib.request.urlopen(url) as response:
        html = response.read()

    # JSON 형식으로 반환된 응답 데이터 처리하기
    commits = json.loads(html)
    # 커밋한 날짜 목록 추출하기
    commit_dates = []
    for commit in commits:
        date_str = commit['commit']['author']['date']
        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ').date()
        commit_dates.append(date_obj)
    # 커밋한 총 날짜 수 구하기
    return len(set(commit_dates))

# markdown lines of rows of present with '■' as many as 'score'
def stack_rows():
    sorted_scores = dict(sorted(tag_dict.items(), key=lambda item: item[1], reverse=True))
    return '\n'.join([f"| {algorithm_name} | {'■' * score} |" for algorithm_name, score in sorted_scores.items()])

# markdown lines grouped by platform, with links of subdir in repository
def items(root_dir:str, item_list:list):
    line_list = []
    for item in item_list:
        title = item.replace('-', ' ').title()
        line_list.append(f'- [{title}]({repository_path}/tree/main/{root_dir}/{item.replace(" ","%20")})\n')
    return '  '.join(line_list)

# markdown lines grouped by platform, with links of subdir in repository
def items_grouped_by_category(root_dir:str, category_dict:dict):
    line_list = []
    category_names = sorted(category_dict.keys())
    for category in category_names:
        line_list.append(f'> {category} :\n')
        item_list = category_dict[category]
        for item in item_list:
            title = item.replace('-', ' ').title()
            line_list.append(f'- [{title}]({repository_path}/tree/main/{root_dir}/{category.lower().replace(" ","%20")}/{item.replace(" ","%20")})\n')
    return '  '.join(line_list)

# generate formatted readme
def readme(new_day:int):
    return \
    f'''
# Algorithm Stacks Updater  

This collects all algorithm stacks by reading last lines of README.md files in subdirectories, that have prefixes of '@'  

ex) @stack @singly-linked-list @sliding-window  

### Day {new_day}  
| Algorithms |      Stack      |
|-----------|------------------|
{stack_rows()}

### Data Structures
{items('base', data_structures)}

### Problem List  
{items_grouped_by_category('problems', problem_dict)}  
'''

# main method
def main():
    # parse data from root directory ('.\\notes')
    read_base('.\\base')
    read_problems('.\\problems')
    # get new day
    main_readme_dir = 'README.md'
    # update main README file
    with open(main_readme_dir, 'w', encoding='utf-8') as f:
        f.write(readme(get_total_committed_day()))
    # push to git
    os.system('git pull origin main')
    os.system('git add .')
    os.system(f'git commit -m "Day {get_total_committed_day()} Update"')
    os.system('git push origin main')
    
main()