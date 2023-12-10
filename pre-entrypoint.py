#!/usr/bin/env python3
import os
import tempfile
import pathlib


os.environ.update({
    'GITHUB_WORKSPACE': '/Users/allan/Documents/action-jinja',
    'GITHUB_STATE': 'state.env',
    'GITHUB_STEP_SUMMARY': 'summary.md',
    'INPUT_template': '.github/templates/job-summary.md.jinja',
    'INPUT_template-format': 'file',
    'INPUT_variables': '{\n  \"jobs\": 1,\n  \"steps\": [\"a\", \"b\", \"c\"]\n}',
    'INPUT_variables-format': 'json',
    'INPUT_output': 'GITHUB_STEP_SUMMARY',
    'INPUT_output-format': 'env',
})


GITHUB_WORKSPACE = os.environ['GITHUB_WORKSPACE']
WORKDIR = pathlib.Path(
    tempfile.mkdtemp(prefix='.', dir=GITHUB_WORKSPACE),
)

def generate_state():
    # Process `template`/`template-format` -> `template`
    template = os.environ['INPUT_template']
    template_format = os.environ['INPUT_template-format']

    if template_format in {'string'}:
        template_file = WORKDIR.joinpath('template.jinja')
        template_file.write_text(template)
        template = str(template_file.relative_to(GITHUB_WORKSPACE))

    yield 'template', template


    # Process `variables`/`variables-format` -> `variables`
    variables = os.environ['INPUT_variables']
    variables_format = os.environ['INPUT_variables-format']

    if not variables_format.endswith('-file'):
        variables_format = variables_format.rstrip('-file')
        variables_file = WORKDIR.joinpath(f'variables.{variables_format}')
        variables_file.write_text(variables)
        variables = str(variables_file.relative_to(GITHUB_WORKSPACE))        

    yield 'format', variables_format
    yield 'variables', variables


    # Process `output`/`output-format` -> `output`
    output = os.environ['INPUT_output']
    output_format = os.environ['INPUT_output-format']

    if output_format in {'env'}:
        output = os.environ[output]

    yield 'outfile', output


with open(os.environ['GITHUB_STATE'], 'a') as GITHUB_STATE:
    for key, value in generate_state():
        print(f'{key}={value}', file=GITHUB_STATE)
