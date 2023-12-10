#!/usr/bin/env python3
import os
import tempfile
import pathlib


GITHUB_WORKSPACE = os.environ['GITHUB_WORKSPACE']
WORKDIR = pathlib.Path(
    tempfile.mkdtemp(prefix='.', dir=GITHUB_WORKSPACE),
)

def generate_state():
    # Process `template`/`template-format` -> `template`
    template = os.environ['INPUT_TEMPLATE']
    template_format = os.environ['INPUT_TEMPLATE-FORMAT']

    if template_format in {'string'}:
        template_file = WORKDIR.joinpath('template.jinja')
        template_file.write_text(template)
        template = str(template_file.relative_to(GITHUB_WORKSPACE))

    yield 'template', template
    yield 'template-format', template_format


    # Process `variables`/`variables-format` -> `variables`
    variables = os.environ['INPUT_VARIABLES']
    variables_format = os.environ['INPUT_VARIABLES-FORMAT']

    if not variables_format.endswith('-file'):
        variables_format = variables_format[:len('-file') - 1]
        variables_file = WORKDIR.joinpath(f'variables.{variables_format}')
        variables_file.write_text(variables)
        variables = str(variables_file.relative_to(GITHUB_WORKSPACE))

    yield 'variables', variables
    yield 'variables-format', variables_format


    # Process `output`/`output-format` -> `output`
    output_file = WORKDIR.joinpath(f'output')
    output = str(output_file.relative_to(GITHUB_WORKSPACE))
    yield 'output', output


with open(os.environ['GITHUB_OUTPUT'], 'a') as GITHUB_OUTPUT:
    for key, value in generate_state():
        print(f'{key}={value}', file=GITHUB_OUTPUT)
