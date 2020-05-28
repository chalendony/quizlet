import os
import sys

root_name, _, _ = __name__.partition('.')
root_module = sys.modules[root_name]
root_dir = os.path.dirname(root_module.__file__)

config_path = os.path.join(root_dir, 'configuration.py')
