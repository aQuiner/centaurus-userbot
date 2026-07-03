## Dependency Imports

If your plugin or third-party script needs any external Python packages, please declare them at the very top of your file using the following format:

```python
# require: requests
```

Or, if your script depends on multiple packages:

```python
# require: requests, aiohttp, bs4
```

The loader will automatically detect this line and handle the required dependencies.

### Rules

* Place the `# require:` line before any imports.
* Separate multiple packages with commas.
* Use the package names exactly as they are installed with `pip`.
* If your script doesn't require any external libraries, simply omit this line.

### Examples

Single dependency:

```python
# require: httpx

import httpx
```

Multiple dependencies:

```python
# require: telethon, aiofiles, pillow

from telethon import TelegramClient
import aiofiles
from PIL import Image
```

That's it. Keep it clean and the loader will do the rest.
