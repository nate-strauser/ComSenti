import os
import sys

SENTIMENTS = {}

def init_plugins(expression):
    plugin_dir = (os.path.dirname(os.path.realpath(__file__)))
    plugin_files = [x[:-3] for x in os.listdir(plugin_dir) if x.endswith(".py")]
    sys.path.insert(0, plugin_dir)
    for plugin in plugin_files:
        mod = __import__(plugin)
        if hasattr(mod, "register"):
            mod.register(SENTIMENTS)
