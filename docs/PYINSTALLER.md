# PyInstaller Compatibility

Clicycle v3.1+ includes built-in PyInstaller compatibility! No wrapper files needed.

## Usage

Just use Clicycle normally in your PyInstaller app:

```python
import clicycle as cc

cc.header("My App") 
cc.info("Works automatically in PyInstaller!")
```

## How It Works

Clicycle automatically detects frozen environments and gracefully handles the module interface initialization. If the normal `sys.modules` replacement fails (as it does in PyInstaller), Clicycle falls back to copying the interface methods directly to the module.

## Optional: Ensure Complete Package Inclusion

If you encounter missing component errors, add this to your `.spec` file:

```python
from PyInstaller.utils.hooks import collect_all

# Ensure all clicycle components are included
datas, binaries, hiddenimports = collect_all('clicycle')

a = Analysis(
    # ... your config ...
    hiddenimports=hiddenimports,
    datas=datas,
)
```

## Alternative: Direct Imports

If you prefer not to use the wrapper, import components directly:

```python
from clicycle import Clicycle
from clicycle.components.header import Header

cli = Clicycle()
header = Header(cli.theme, "My App")
cli.stream.render(header)
```

This approach works without any PyInstaller configuration changes.