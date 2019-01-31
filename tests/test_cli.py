import json
import os
import subprocess
import sys

from mro_migrator import cli
import pytest


@pytest.mark.skipif(sys.platform == "darwin", reason="there is no MRO on osx")
def test_convert_env(testing_workdir):
    env_path = os.path.join(testing_workdir, 'env')
    args = ['conda', 'create', '-yp', env_path, 'mro-base', 'r-essentials']
    subprocess.check_call(args)

    args = ['conda', 'list', '--json', '-p', env_path]
    output = subprocess.check_output(args)
    env_list_output = json.loads(output)
    assert any(_['name'] == 'mro-base' for _ in env_list_output)

    removed_packages = cli.main(env_path)
    args = ['conda', 'list', '--json', '-p', env_path]
    output = subprocess.check_output(args)
    env_list_output = json.loads(output)
    assert any(_['name'] == 'mro-base' for _ in env_list_output)
    assert "mro-base" in removed_packages

    removed_packages = cli.main(env_path, execute=True)
    args = ['conda', 'list', '--json', '-p', env_path]
    output = subprocess.check_output(args)
    env_list_output = json.loads(output)
    assert not any(_['name'] == 'mro-base' for _ in env_list_output)
    assert any(_['name'] == 'r-base' for _ in env_list_output)
    assert "mro-base" in removed_packages
