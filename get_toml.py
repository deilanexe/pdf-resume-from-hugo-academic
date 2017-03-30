import toml
from markdown import markdown
import pdfkit
from datetime import datetime
from os import listdir
from os.path import isfile, join

md_path = 'path/to/your/local/hugo/site'
toml_file = '{}/config.toml'.format(md_path)
pdf_file = 'path/to/output.pdf'
about_file = '{}/content/home/about.md'.format(md_path)
css_file = 'path/to/additional/style.css'


def split_file(input_file):
    toml_contents = ''
    markdown_contents = []
    is_toml = False
    md_line_tmp = ''
    with open(input_file, 'r') as conffile:
        for line in conffile:
            if line.startswith('+++'):
                is_toml = not is_toml
            elif is_toml:
                toml_contents += line
            else:
                if line.rstrip() == '':
                    if len(md_line_tmp) > 0:
                        markdown_contents.append(md_line_tmp)
                        md_line_tmp = ''
                else:
                    md_line_tmp += '{} '.format(line.rstrip())
    if len(md_line_tmp) > 0:
        markdown_contents.append(md_line_tmp)
    return toml_contents, markdown_contents


markdown_string = ''
publication_types = []
c_skills_labels = []
c_skills = []
skill_types = []
competences = []
with open(toml_file, 'r') as conffile:
    config = toml.loads(conffile.read())
    print config.keys()
    params = config.get('params', {})
    social = params.get('social', [])
    publication_types = params.get('publication_types', [])
    c_skills_labels = params.get('computer_skill_levels_labels', [])
    c_skills = params.get('computer_skill_levels', [])
    skill_types = params.get('computer_skill_types', [])
    competences = params.get('computer_skill_competence', [])
    github_link = ''
    for item in social:
        if item.get('icon', '') == 'github':
            github_link = item.get('link', "-")
            avatar = params.get('avatar')
            small_avatar = '_sm.'.join(avatar.split('.'))
markdown_string += """
| {}   | {}   |
| :--- | ---: |
| {}   | {}   |
| {}   | {}   |
| {}   | {}   |
| {}   | {}   |
| {}   | {}   |\n
""".format(
        '<h1>{}</h1>'.format(params.get('name')),
        '![portrait]({}/static/img/{})'.format(
                md_path, small_avatar
                ),
        '**birth date**', params.get('birthdate'),
        '**address**',
        params.get('address'), '**email**',
        params.get('email'),
        '**website**', params.get('website'),
        '**github**', github_link[len('//github.com/'):]
        )

toml_contents, md_contents = split_file(about_file)
print toml_contents
print md_contents
markdown_string += md_contents[1]
config = toml.loads(toml_contents)
print config.keys()

interests = config.get('interests', {}).get('interests', [])
if len(interests) > 0:
    count = 0
    markdown_string += '\n## Interests\n'
    for interest in interests:
        if count < 5:
            markdown_string += '{}, '.format(interest)
        count += 1
markdown_string = '{}{}'.format(markdown_string[:-2], '.\n')

markdown_string += '\n\n## Education\n'
education = config.get('education', {})
courses = education.get('courses', [])
for course in courses:
    description = course.get('description', None)
    markdown_string += '#### {} ({}) - {}\n\n{}'.format(
            course.get('course', ''), course.get('year', ''),
            course.get('institution', ''),
            '' if description is None else '  {}\n\n'.format(description)
            )
markdown_string += '\n'

markdown_string += '## Working Experience\n'
companies = config.get('work', {}).get('company', [])
for company in companies:
    markdown_string += '### {} ({} - {})\n\n{} | {}\n\n'.format(
            company.get('role'), company.get('start-date'),
            company.get('end-date', 'Present'), company.get('team'),
            company.get('company')
            )
    markdown_string += '#### Projects\n'
    projects = company.get('projects', [])
    for project in projects:
        project_toml, project_md = split_file(
                '{}/content/project/{}.md'.format(md_path, project)
                )
        print project_toml
        print project_md
        project_keys = toml.loads(project_toml)
        print project_keys
        project_link = project_keys.get('external_link')
        selected_sentences = project_md
        if 'relevant_paragraphs' in project_keys:
            selection = project_keys.get('relevant_paragraphs', [])
            print selection
            selected_sentences = []
            for item in selection:
                selected_sentences.append(project_md[item])
        markdown_string += '##### {}{}\n\n{}'.format(
                project_keys.get('title'),
                '' if len(project_link) == 0 else ' ({})'.format(project_link),
                '{}\n\n'.format('\n\n'.join(selected_sentences))
                )

markdown_string += '\n## Accountabilities\n\n'
accountabilities = config.get('accountabilities')
for accountability in accountabilities:
    examples = accountability.get('examples')
    examples_string = ''
    for example in examples:
        examples_string += '* {}\n'.format(example)
    print examples_string
    markdown_string += '##### {}\n{}\n'.format(
            accountability.get('concept'),
            examples_string
            )


markdown_string += '\n## Voluntary Work\n\n'
voluntary_works = config.get('voluntary-work')
for voluntary_work in voluntary_works:
    markdown_string += '* {}\n'.format(voluntary_work.get('description'))

markdown_string += '\n## Latest Publications\n\n'
markdown_string += '\n(only the last five publications are shown; refer to my website for the full list)\n\n'
publications_path = '{}/content/publication/'.format(md_path)
md_files = [f for f in listdir(publications_path) if isfile(
        join(publications_path, f)) and not f.startswith('_')
        ]
print md_files
publications = {}
for publication_file in md_files:
    pub_toml, pub_md = split_file(
            '{}{}'.format(publications_path, publication_file)
            )
    print pub_toml
    print pub_md
    pub_keys = toml.loads(pub_toml)
    pub_type = pub_keys.get('publication_types', ['0'])[0]
    print pub_type
    pub_date = datetime.strptime(pub_keys.get('date'), '%Y-%m-%d')
    print pub_date
    pub_details = '\n **{}**. {}. {}. ({}, {}). {}\n\n'.format(
            pub_keys.get('title'),
            '_{}_'.format('_, _'.join(pub_keys.get('authors', []))),
            pub_keys.get('publication'),
            publication_types[int(pub_type)],
            pub_date.year,
            pub_md[0]
            )
    publications[pub_date] = pub_details
sort_pub = sorted(publications.items(), key=lambda p: p[0], reverse=True)
counter = 0
for _, pub in sort_pub:
    if counter < 5:
        markdown_string += pub
    counter += 1

markdown_string += '\n## Computer Skills\n\n'
skills = config.get('computer-skills', [])
skillset = {}
for skill in skills:
    stype = str(skill.get('type', -1))
    comp_list = skill.get('competence', [])
    comp = ', '.join([competences[x] for x in comp_list])
    skill_string = '{} ({} | {})\n'.format(
            skill.get('skill', ''),
            c_skills[skill.get('level')],
            comp
            )
    print skill_string
    skill_list = skillset.get(stype, [])
    skill_list.append(skill_string)
    skillset[stype] = skill_list
sorted_skillset = sorted(skillset.items(), key=lambda p: p[0])
for skill_type, skills in sorted_skillset:
    stype_label = skill_types[int(skill_type)]
    markdown_string += '### {}\n\n'.format(stype_label)
    for skill in skills:
        markdown_string += '* {}'.format(skill)
    markdown_string += '\n'

today = datetime.today()
markdown_string += '\n#### Closing date: {}\n\n'.format(
        today.strftime('%b %d, %Y')
        )


print markdown_string
html_text = markdown(
        markdown_string, output_format='html4',
        extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.def_list'
                ]
        )
# print html_text
pdfkit.from_string(html_text, pdf_file, css=css_file)
