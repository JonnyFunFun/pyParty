import os
import glob
import os


class PartyHooks():
    _hook_reg = {}
    
        
    @staticmethod
    def register(function, hook):
        if hook not in PartyHooks._hook_reg:
            PartyHooks._hook_reg[hook] = []
        PartyHooks._hook_reg[hook].append(function)
        
        
    @staticmethod
    def execute_hook(hook, *args, **kwargs):
        print("Hook execute - %s" % hook)
        if hook not in PartyHooks._hook_reg:
            return
        for function in PartyHooks._hook_reg[hook]:
            function(*args, **kwargs)
    
    
def pyparty_plugin_register(hook):
    def reg(func):
        PartyHooks.register(func, hook)
        return func
    return reg


modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules ]

