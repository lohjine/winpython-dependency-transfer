"""
Adapted from  https://gist.github.com/qgerome/202a70e19ec8fa0f259a

Usage: python pip_compare OLDREQUIREMENTSTXT NEWREQUIREMENTSTXT

Prints: Comparison between all libraries

Outputs:
    - requirements_withversion.txt - Missing requirements with version from old requirements
    - requirements_withoutversion.txt - Missing requirements without version
    - requirements_diff.txt
"""

import click
import itertools

def split_package(line):
    result = line.split('==')
    if not len(result) == 2:
        result = line.split('@')

        if not len(result) == 2:
            if line.startswith('-e'):
                # OK, I'll give a try but ONLY if you use the #egg in the end of the str
                result = line.split('#egg=')[1].split('-')
                result = '-'.join(result[:-1]), result[-1]
            else:
                raise Exception('Weird result of splitting: %s' % result)

    return map(lambda x: x.strip(), result)


def packages(freeze_f):
    for line in freeze_f.readlines():
        package, version = split_package(line)
        yield package, version


def merge_packages(*freezes):
    all_keys = set(itertools.chain(*[freeze.keys() for freeze in freezes]))

    for k in all_keys:
        versions = []
        for freeze in freezes:
            versions.append(freeze.get(k, None))  # Add the version for the package

        yield k, versions


def is_unique_value(l):
    """
    Checks if all elements in l are the same
    :param l: list of str
    """

    return not l or l.count(l[0]) == len(l)


def compare(old_packages, new_packages):
    """
    :type old_packages: dict
    :type new_packages: dict
    """
    requirements = dict(merge_packages(old_packages, new_packages))

    with_version = []
    without_version = []
    requirements_diff = []

    for package_name, versions in requirements.items():
        if not is_unique_value(versions):
            click.echo("{package}: {versions}".format(package=package_name, versions=versions))
            requirements_diff.append("{package}: {versions}".format(package=package_name, versions=versions)+'\n')
            if not versions[1]:
                without_version.append(package_name +'\n')
                with_version.append("{package}=={versions[0]}".format(package=package_name, versions=versions)+'\n')

    return with_version, without_version, requirements_diff

@click.command()
@click.argument("old", type=click.File('r'))
@click.argument("new", type=click.File('r'))
@click.option('-v', '--verbose', count=True)
def diff(old, new, verbose=False):
    click.echo("Diff between {0} and {1}".format(old, new))
    old_packages = dict(packages(old))
    new_packages = dict(packages(new))
    with_version, without_version, requirements_diff = compare(old_packages, new_packages)

    with open('requirements_withversion.txt', 'w') as f:
        f.writelines(with_version)
    with open('requirements_withoutversion.txt', 'w') as f:
        f.writelines(without_version)
    with open('requirements_diff.txt', 'w') as f:
        f.writelines(requirements_diff)


if __name__ == '__main__':
    diff()