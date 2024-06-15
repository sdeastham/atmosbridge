import os
import pathlib
def load_dotnet(dotnet_root=None):
    # Adds the target dotnet version to the path
    if dotnet_root is None:
        home = pathlib.Path.home()
        dotnet_root = os.path.join(home,'.dotnet')
        assert os.path.isdir(dotnet_root), f'dotnet not found in default location {dotnet_root}'
    os.environ['DOTNET_ROOT'] = dotnet_root
    os.environ['PATH'] = os.path.join(dotnet_root,'tools') + os.pathsep + os.environ['PATH']

def init_bridge(atmos_tools_dir,mathnet_dll=None):
    if mathnet_dll is None:
        # Try to find the MathNet.Numerics dll automatically in the default location
        home = pathlib.Path.home()
        mathnet_dir = os.path.join(home,'.nuget','packages','mathnet.numerics')
        assert os.path.isdir(mathnet_dir), f'MathNet.Numerics directory not found at {mathnet_dir}'
        dll_name = 'MathNet.Numerics.dll'
        for root, dirs, files in os.walk(mathnet_dir):
            if dll_name in files:
                mathnet_dll = os.path.join(root,dll_name)
                break
        assert mathnet_dll is not None, f'Could not find {dll_name} anywhere in {mathnet_dir}'
    from pythonnet import load
    load("coreclr",runtime_config=os.path.abspath(os.path.join(atmos_tools_dir,'AtmosTools.runtimeconfig.json')))
    import clr
    f_dll = os.path.join(atmos_tools_dir,'AtmosTools.dll')
    clr.AddReference(os.path.abspath(f_dll))
    #clr.AddReference("C:/Users/sdeas/.nuget/packages/mathnet.numerics/5.0.0/lib/net6.0/MathNet.Numerics.dll")
    clr.AddReference(os.path.abspath(mathnet_dll))

import os
import pathlib
import configparser
config_file = os.path.join(pathlib.Path.home(),'.config','atmostools','atmostools.conf')
cfg = configparser.ConfigParser()
try:
    cfg.read(config_file)
    atmostools_dir = cfg['paths']['atmostools_dir']
except:
    print(f'Configuration file could not be read from {config_file}; check that it exists and contains bthe path to a completed AtmosTools build')
    raise
load_dotnet()
init_bridge(atmostools_dir)
from AtmosTools import *
