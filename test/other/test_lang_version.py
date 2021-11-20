import os
from gitfx.lang_version import get_version


LANG_VERSION = {'python': '3.8.0',   # pyenv
                'ruby': '2.6.0',     # rvm/rbenv
                'perl': '5.8.0',     # plenv
                'node': '16.2.0',    # nvm
                'php': '8.0.1'}      # phpenv


def assert_lang_version(lang):
    expected = LANG_VERSION.get(lang)
    version_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'versions')
    assert os.path.isdir(version_path)
    version = get_version(version_path, lang)
    print("VER: %s" % version)
    assert version == expected


def test_python_version():
    """Test Python version"""
    assert_lang_version('python')


def test_ruby_version():
    """Test Ruby version"""
    assert_lang_version('ruby')


def test_perl_version():
    """Test Perl version"""
    assert_lang_version('perl')


def test_node_version():
    """Test Node.js version"""
    assert_lang_version('node')


def test_php_version():
    assert_lang_version('php')
