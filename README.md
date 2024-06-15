# AtmosBridge - A Python Wrapper for the AtmosTools Package

Allows access to the functions in the AtmosTools C# package from Python.

## Setup

* Install the pythonnet package (`conda install -c conda-forge pythonnet`)
* Make sure you have dotnet 8.0 or later installed
* Download and build AtmosTools from https://github.com/sdeastham/AtmosTools
* Create a file in `$HOME/.config/atmostools` called `atmostools.conf` which contains the directory of your completed build - typically the AtmosTools subdirectory `bin/Release/net8.0` or `bin/Debug/net8.0` (see `example_atmostools.conf`)
* In Python, run `from atmosbridge import atmostools`

During import, atmosbridge will link to the C# files. From that point onwards, you can access the AtmosTools packages exactly like in C# - for example:

```
import numpy as np
from atmosbridge import atmostools
lhr_latlon = (51.4775,   -0.461389)
bos_latlon = (42.363056, -71.006389)
gc_result = atmostools.Geodesy.GreatCircleWaypointsByCount(lhr_latlon[1],lhr_latlon[0],bos_latlon[1],bos_latlon[0],101)
lons, lats, lengths = (gc_result.Item1, gc_result.Item2, gc_result.Item3)
print(f'Distance from Boston to London Heathrow: {np.sum(lengths):10.1f} km')
```

will give the result

```
Distance from Boston to London Heathrow:     5239.6 km
```

## Pitfalls

As you can see above, routines which return a tuple in C# can be slightly painful to unpack. You need to access the items explicitly as `Item1`, `Item2` and so on. You may also want to convert arrays which are returned to instead by numpy arrays, for example by running `lengths = np.asarray(gc_result.Item3)` in the above example.
