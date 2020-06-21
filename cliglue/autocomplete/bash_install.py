import os

from cliglue.utils.files import script_real_path
from cliglue.utils.output import warn, info
from cliglue.utils.shell import shell


def install_bash(app_name: str):
    """
    Install script link in /usr/bin/{app_name}
    and create bash autocompletion script
    """
    app_path: str = script_real_path()
    assert os.path.isfile(app_path)

    if os.geteuid() != 0:
        warn("you may need to have root privileges in order to install script")

    # ensure script is executable
    if not os.access(app_path, os.X_OK):
        info(f'making script executable')
        shell(f'chmod +x {app_path}')

    # creating /usr/bin/ link
    usr_bin_executable: str = f'/usr/bin/{app_name}'
    if os.path.exists(usr_bin_executable) or os.path.islink(usr_bin_executable):
        warn(f'file {usr_bin_executable} already exists - skipping.')
        if not os.path.exists(usr_bin_executable):
            warn(f'link {usr_bin_executable} is broken.')
    else:
        info(f'creating link: {usr_bin_executable} -> {app_path}')
        shell(f'ln -s {app_path} {usr_bin_executable}')

    install_autocomplete(app_name)


def install_autocomplete(app_name: str):
    """
    Create bash autocompletion script
    """
    if os.geteuid() != 0:
        warn("you may need to have root privileges in order to install autocompletion script")

    # bash autocompletion install
    completion_script_path: str = f'/etc/bash_completion.d/cliglue_{app_name}.sh'
    app_hash: int = hash(app_name) % (10 ** 8)
    # function should be unique across bash env
    function_name: str = f'_autocomplete_{app_hash}'
    shell(f"""cat << 'EOF' | tee {completion_script_path}
#!/bin/bash
{function_name}() {{
COMPREPLY=( $({app_name} --autocomplete "${{COMP_LINE}}" ${{COMP_CWORD}}) )
}}
complete -F {function_name} {app_name}
EOF
""")
    info(f'Autocompleter has been installed in {completion_script_path}. Please restart your shell.')
