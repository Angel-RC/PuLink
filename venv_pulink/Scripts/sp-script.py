#!C:\Users\Chicote\Desktop\proyectos\PuLink\venv_pulink\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'sp==1.1.0','console_scripts','sp'
__requires__ = 'sp==1.1.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('sp==1.1.0', 'console_scripts', 'sp')()
    )
