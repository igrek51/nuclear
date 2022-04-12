import os

from nuclear.utils.files import script_real_path


def test_script_real_path():
    assert os.path.isfile(script_real_path())
    assert '/pytest.py' in script_real_path() or '/pytest/__main__.py' in script_real_path()
