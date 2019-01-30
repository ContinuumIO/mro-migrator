from argparse import ArgumentParser
import os
import subprocess
import sys
import tempfile
from fnmatch import fnmatch

from six import string_types
import yaml


def get_env_specs(env_path, out_path):
    subprocess.check_call(['conda', 'env', 'export', '-p', env_path, '-f', out_path])


def remove_pkgs(env_path, pkg_list):
    args = ['conda', 'remove', '-yp', env_path]
    args.extend(pkg_list)
    subprocess.check_call(args)


def install_pkgs(env_path, pkg_list):
    args = ['conda', 'install', '-yp', env_path]
    args.extend(pkg_list)
    subprocess.check_call(args)


def ensure_list(arg):
    if (isinstance(arg, string_types) or not hasattr(arg, '__iter__')):
        if arg is not None:
            arg = [arg]
        else:
            arg = []
    return arg


mro_only_packages = [
    'mro*',
    '_r-mutex',
    'r-checkpoint',
    'r-deployrrserve',
    'r-matrixcalc',
    'r-microsoftr',
    '*mrclient*',
    'r-mro',
    'r-revo*',
    'r-runit'
]

if sys.platform == 'win32':
    mro_only_packages.extend(['r-rmysql', 'r-sf'])


if __name__ == "__main__":
    parser = ArgumentParser(description="Tool to migrate MRO environments to use Anaconda R")
    parser.add_argument("env_path")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    tmpdir = tempfile.gettempdir()
    out_file = os.path.join(tmpdir, 'dumped_env.yml')
    get_env_specs(args.env_path, out_file)
    with open(out_file) as f:
        env_specs = yaml.load(f)

    additions = ['r-base']
    removals = []
    for spec in env_specs['dependencies']:
        name, version, build_string = spec.split('=')
        if any(fnmatch(name, pattern) for pattern in mro_only_packages):
            removals.append(name)
        elif build_string.startswith('mro'):
            removals.append(name)
            additions.append(name)
    remove_pkgs(args.env_path, removals)
    install_pkgs(args.env_path, additions)
