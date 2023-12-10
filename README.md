## Usage

```yaml
- uses: swaglive/action-jinja@main
  with:
    template: |-
      Hello {{ name }}
    variables: |-
      name: World

- uses: swaglive/action-jinja@main
  with:
    template-format: file
    template: .github/workflows/test/job-summary.md.jinja
    variables-format: json-file
    variables: .github/workflows/test/variables.json
```
