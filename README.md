# pdf-resume-from-hugo-academic

A Python script that reads TOML and Markdown files used to generate a profile
page using Hugo. These files are used to assemble the content in a printable
PDF file if required.

I just did this as I have always wanted to have a way to automatically do both
tasks at the same time - writing my resum&eacute; and my personal website!

## Dependencies

- Hugo (http://gohugo.io/) and template hugo-academic
(http://themes.gohugo.io/academic/).
- Markdown (2.6.8)
- argparse (1.2.1)
- pdfkit (0.6.1)
- toml (0.9.2)
- wsgiref (0.1.2)

## Execution

For now, just install dependencies and run **get_toml.py**.

Note that for now most of the components added to the resum&eacute; are
hard-coded in the script. I will start decoupling these contents so the script
is more flexible in the future.

I have created some additional elements in TOML config and about.md files,
which currently are not displayed on the website, but help making the
resum&eacute; more informative.

### Labels added to config.toml

computer_skill_levels_labels = [
  'Beginner = (< 1 yr)',
  'Intermediate = (1-2 yrs)',
  'Advanced = (> 2 yrs)'
]

computer_skill_types = [
  'N/A',
  'Programming Languages',
  'DB Management Systems',
  'Operating Systems',
  'Cloud Service Providers',
  'Natural Language Understanding platforms'
]

computer_skill_levels = [
  'Beginner',
  'Intermediate',
  'Advanced'
]

### New fields in about.md

[interests]
  interests = []

[[work.company]]
  company = ""
  team = ""
  address = ""
  role = ""
  start-date = ""
  projects = [You can list projects from the content/project folder file names]


[[voluntary-work]]
  description = ""

[[computer-skills]]
  skill = ""
  type = 0
  level = 0
  competence = []
  details = ""

[[accountabilities]]
  concept = ""
  examples = [Include as many paragraphs as bullet points as required]
