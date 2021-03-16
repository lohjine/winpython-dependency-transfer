# Winpython Dependency Transfer

Winpython's portability is awesome, but might make upgrading it hard. This diffs the requirements so you can install all your installed libs on the new Winpython.

## Usage

Run pip freeze for both Winpython for requirements.txt.

python pip_compare.py OLDREQUIREMENTSTXT NEWREQUIREMENTSTXT

Prints: Comparison between all libraries

Outputs:
    - requirements_withversion.txt - Missing requirements with version from old requirements
    - requirements_withoutversion.txt - Missing requirements without version
    - requirements_diff.txt