import os

from cliglue.utils.files import script_real_path
from cliglue.utils.output import warn, info
from cliglue.utils.shell import shell


def bash_install(app_name: str):
    """
    Install script link in /usr/bin/{app_name}
    and create bash autocompletion script
    """
    app_bin_path = script_real_path()
    assert os.path.isfile(app_bin_path)

    # ensure script is executable
    if not os.access(app_bin_path, os.X_OK):
        info(f'making script executable')
        shell(f'sudo chmod +x {app_bin_path}')

    # creating /usr/bin/ link
    usr_bin_executable: str = f'/usr/bin/{app_name}'
    if os.path.exists(usr_bin_executable):
        warn(f'file {usr_bin_executable} already exists - skipping.')
    else:
        script_path: str = script_real_path()
        info(f'creating link: {usr_bin_executable} -> {script_path}')
        shell(f'sudo ln -s {script_path} {usr_bin_executable}')

    # bash autocompletion install
    script_path: str = f'/etc/bash_completion.d/cliglue_{app_name}.sh'
    app_hash: int = hash(app_name) % (10 ** 8)
    function_name: str = f'_autocomplete_{app_hash}'  # should be unique across bash env
    shell(f"""cat << 'EOF' | sudo tee {script_path}
#!/bin/bash
{function_name}() {{
COMPREPLY=( $({app_name} --bash-autocomplete "${{COMP_LINE}}") )
}}
complete -F {function_name} {app_name}
EOF
""")
    info(f'Autocompleter has been installed in {script_path}. Please restart your shell.')
