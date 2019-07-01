from cliglue.utils.files import *


def test_read_file():
    assert read_file('tests/utils/res/readme') == 'Readme\n123'


def test_save_file():
    save_file('tests/utils/res/saveme', 'dupa\n123')
    assert read_file('tests/utils/res/saveme') == 'dupa\n123'
    save_file('tests/utils/res/saveme', '')
    assert read_file('tests/utils/res/saveme') == ''


def test_list_dir():
    assert list_dir('tests/utils/res/listme') == ['afile', 'dir', 'zlast', 'zlastdir']


def test_workdir():
    workdir = get_workdir()
    set_workdir('/')
    assert get_workdir() == '/'
    set_workdir('/home/')
    assert get_workdir() == '/home'
    set_workdir(workdir)


def test_script_real_path():
    assert '/pytest.py' in script_real_path()


def test_file_exists():
    assert file_exists('tests/utils/res/readme')
    assert not file_exists('tests/utils/res/dupadupa')
