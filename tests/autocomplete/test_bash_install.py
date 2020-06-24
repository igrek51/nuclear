import os
from pathlib import Path

from nuclear import *
from nuclear.utils.files import script_real_path
from nuclear.utils.shell import shell
from tests.asserts import MockIO


def test_bash_install_twice():
    app_name = 'nuclear_test_dupa123'

    with MockIO('--install-bash', 'nuclear_test_dupa123') as mockio:
        CliBuilder().run()
        assert 'Link installed' in mockio.output()
        assert 'Autocompleter has been installed' in mockio.output()
        assert os.path.islink(f'/usr/bin/{app_name}')
        assert os.path.realpath(f'/usr/bin/{app_name}') == script_real_path()
        assert os.path.exists(f'/etc/bash_completion.d/nuclear_{app_name}.sh')

    with MockIO('--install-bash', 'nuclear_test_dupa123') as mockio:
        CliBuilder().run()
        assert 'Link installed' in mockio.output()
        assert 'Autocompleter has been installed' in mockio.output()
        assert os.path.islink(f'/usr/bin/{app_name}')
        assert os.path.realpath(f'/usr/bin/{app_name}') == script_real_path()
        assert os.path.exists(f'/etc/bash_completion.d/nuclear_{app_name}.sh')

    shell(f'sudo rm -f /usr/bin/{app_name}')
    shell(f'sudo rm -f /etc/bash_completion.d/nuclear_{app_name}.sh')
    assert not os.path.exists(f'/usr/bin/{app_name}')
    assert not os.path.exists(f'/etc/bash_completion.d/nuclear_{app_name}.sh')


def test_autocomplete_install_explicit_name():
    app_name = 'nuclear_test_dupa123'

    with MockIO('--install-autocomplete', 'nuclear_test_dupa123') as mockio:
        CliBuilder().run()
        assert 'Autocompleter has been installed' in mockio.output()
        assert os.path.exists(f'/etc/bash_completion.d/nuclear_{app_name}.sh')
        completion_script = Path(f'/etc/bash_completion.d/nuclear_{app_name}.sh').read_text()
        assert '''COMPREPLY=($(nuclear_test_dupa123 --autocomplete "${COMP_LINE}" ${COMP_CWORD}))''' \
               in completion_script
        assert '''complete -o filenames -F _autocomplete_1446250409 nuclear_test_dupa123''' in completion_script

    shell(f'sudo rm -f /etc/bash_completion.d/nuclear_{app_name}.sh')
    assert not os.path.exists(f'/etc/bash_completion.d/nuclear_{app_name}.sh')


def test_autocomplete_install_implicit_name():
    app_name = 'glue'

    with MockIO('--install-autocomplete') as mockio:
        CliBuilder().run()
        assert 'Autocompleter has been installed' in mockio.output()
        assert os.path.exists(f'/etc/bash_completion.d/nuclear_{app_name}.sh')
        completion_script = Path(f'/etc/bash_completion.d/nuclear_{app_name}.sh').read_text()
        assert '''COMPREPLY=($(glue --autocomplete "${COMP_LINE}" ${COMP_CWORD}))''' in completion_script
        assert '''complete -o filenames -F _autocomplete_70451630 glue''' in completion_script

    shell(f'sudo rm -f /etc/bash_completion.d/nuclear_{app_name}.sh')
    assert not os.path.exists(f'/etc/bash_completion.d/nuclear_{app_name}.sh')
