import os
import sys
import zlib
from typing import Optional

from nuclear.sublog import log
from nuclear.utils.files import script_real_path
from nuclear.shell.shell_utils import shell


def install_bash(app_name: str):
    """
    Install script link in /usr/bin/{app_name}
    and create bash autocompletion script
    """
    app_path: str = script_real_path()
    assert os.path.isfile(app_path)

    if os.geteuid() != 0:
        log.warn("gaining root privileges in order to install script")

    # ensure script is executable
    if not os.access(app_path, os.X_OK):
        log.info(f'making script executable')
        shell(f'chmod +x {app_path}')

    # creating /usr/bin/ link
    usr_bin_executable: str = f'/usr/bin/{app_name}'
    if os.path.exists(usr_bin_executable) or os.path.islink(usr_bin_executable):
        log.warn(f'file {usr_bin_executable} already exists - skipping.')
    else:
        log.info(f'creating link: {usr_bin_executable} -> {app_path}')
        shell(f'sudo ln -s {app_path} {usr_bin_executable}')

    log.info(f'Link installed in {usr_bin_executable}. Please restart your shell.')
    install_autocomplete(app_name)


def install_autocomplete(app_name: Optional[str]):
    """
    Create bash autocompletion script
    """
    if os.geteuid() != 0:
        log.warn("gaining root privileges in order to install autocompletion script")

    if not app_name:
        app_name = shell_command_name()

    completion_script_path: str = f'/etc/bash_completion.d/nuclear_{app_name}.sh'
    app_hash: int = zlib.adler32(app_name.encode('utf-8'))
    # function should be unique across bash env
    function_name: str = f'_autocomplete_{app_hash}'
    shell(f"""cat << 'EOF' | sudo tee {completion_script_path}
#!/bin/bash
{function_name}() {{
    IFS=$'\n'
    COMPREPLY=($({app_name} --autocomplete "${{COMP_LINE}}" ${{COMP_CWORD}}))
}}
complete -o filenames -F {function_name} {app_name}
EOF
""")
    log.info(f'Autocompleter has been installed in {completion_script_path} for command "{app_name}". '
             f'Please restart your shell.')


def shell_command_name():
    _, command = os.path.split(sys.argv[0])
    return command
