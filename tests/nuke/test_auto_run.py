import os
import sys
from unittest.mock import patch
from nuclear import nuke


def test_auto_run_registers_atexit():
    """Verify nuke.init() registers atexit when auto_run=True (and running as main)."""
    class Config:
        dry: bool = False

    main_mod = type('main_module', (), {'Config': Config, '__spec__': None})

    with patch('atexit.register') as mock_register:
        with patch.dict(sys.modules, {'__main__': main_mod}):
            with patch.object(sys, 'argv', ['nukefile.py']):
                with patch.dict(os.environ, {'NUKE_TESTING': '0'}):
                    nuke.init(auto_run=True)
                    assert mock_register.called
                    assert mock_register.call_args[0][0] == nuke.run


def test_auto_run_no_atexit_when_disabled():
    """Verify nuke.init() does not register atexit when auto_run=False."""
    with patch('atexit.register') as mock_register:
        with patch.object(sys, 'argv', ['nukefile.py']):
            with patch.dict(os.environ, {'NUKE_TESTING': '0'}):
                nuke.init(auto_run=False)
                assert not mock_register.called