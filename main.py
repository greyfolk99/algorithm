import datetime
import os
import re
import urllib.request
import json

username = 'greyfolk99'
repository = 'algorithm'
repository_path = "https://github.com/{username}/{repository}".format(username=username, repository=repository)

def get_values_from_last_line(directory, regex="r'@([\w-]+)'"):
    values = []
    with open(directory, 'r', encoding='utf-8') as f:
        last_line = f.read().strip().split('\n')[-1]
        for value in re.finditer(regex, last_line):
            values.append(value.group(1).replace('-', ' ').title())
    return values

def get_child_dirs(path) -> list:
    return [child for child in os.scandir(path)]


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


# markdown lines grouped by platform, with links of subdir in repository
def items_grouped_by_category(root_dir: str, category_dict: dict):
    lines = []
    category_names = sorted(category_dict.keys())
    for category in category_names:
        lines.append(f'> {category} :\n')
        item_list = category_dict[category]
        for item in item_list:
            title = item.replace('-', ' ').title()
            lines.append(
                f'- [{title}]({repository_path}/tree/main/{root_dir}/{category.lower().replace(" ", "%20")}/{item.replace(" ", "%20")})\n')
    return '  '.join(lines)


# generate formatted readme
def generate_readme(paragraphs):
    enter = '\n'

    return f'''
# Algorithm Study Note  

_This README is automatically generated._  

Each README files in subdirectories (note, problems) can have tags that starts with '@' to annotate the content.  

```
ex) @stack @singly-linked-list @sliding-window  
```
{enter.join([paragraph for paragraph in paragraphs])}
'''

def save_tag_count(readme_path, tag_dict):
    with open(readme_path, 'r', encoding='utf-8') as f:
        last_line = f.read().strip().split('\n')[-1]
        for tag in re.finditer(r'@([\w-]+)', last_line):
            tag_name = tag.group(1).lower()
        tag_dict[tag_name] = tag_dict.get(tag_name, 0) + 1


# main method
def main():
    # data collection
    problems_root = '.\\problems'
    notes_root = '.\\notes'
    platform_problem_dict = {}  # { platform : [titles] }
    tag_dict = {}  # { tag : score }
    notes = []
    for platform_dir in get_child_dirs(problems_root):
        platform_name = platform_dir.name
        platform_problem_dict[platform_name] = []
        for problem_dir in get_child_dirs(platform_dir.path):
            readme_path = os.path.join(problem_dir.path, 'README.md')
            platform_problem_dict[platform_name].append(problem_dir.name)
            save_tag_count(readme_path, tag_dict)
    for snippet_dir in get_child_dirs(notes_root):
        notes.append(snippet_dir.name)
        readme_path = os.path.join(snippet_dir.path, 'README.md')
        save_tag_count(readme_path, tag_dict)

    # generate markdown
    enter = '\n'
    stack_score_table = f'''
### Day {get_total_committed_day()}  
| Algorithms |      Stack      |
|-----------|------------------|
{enter.join(
        [f"| {tag.replace('-', ' ').title()} | {'■' * score} |"
         for tag, score in dict(sorted(tag_dict.items(), key=lambda item: item[1], reverse=True)).items()])}
'''

    problem_paragraph = f'''
### Problem List  
{items_grouped_by_category('problems', platform_problem_dict)}  
'''

    note_paragraph = f'''
### Notes
{enter.join([f'- [{note}]({repository_path}/tree/main/notes/{note.replace(" ", "%20")})' for note in notes])}
'''

    with open('README.md', 'w', encoding='utf-8') as f:
        paragraphs = [
            stack_score_table,
            problem_paragraph,
            note_paragraph
        ]
        f.write(generate_readme(paragraphs))

    # push to git
    os.system('git pull')
    os.system('git add .')
    os.system(f'git commit -m "Day {get_total_committed_day()} Update"')
    os.system('git push origin main')

main()

