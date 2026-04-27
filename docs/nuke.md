# Nuke - Simple Task Runner

**Nuke** is a lightweight task runner built into Nuclear that lets you define and run tasks as Python functions in a `nukefile.py` script.

It's perfect for:
- Running build, test, and deployment tasks
- Managing development workflows
- Quick automation scripts
- Managing project tasks with configuration

## Quick Start

Create a `nukefile.py` file with a few tasks:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "nuclear>=2.8.1",
# ]
# ///
from nuclear import nuke, logger

class Config:
    src_path: str = '/opt/dump'
    dst_path: str = '/media/user/DRIVE/'
    dry: bool = False

config, sh = nuke.init(Config)

def push():
    sh(f"rsync -avh --delete --size-only --info=progress2 '{src_path}/' '{dst_path}'")

def convert():
    sh(f'ffmpeg -i "{src_path}/input.mp4" "{dst_path}/audio.mp3"')

if __name__ == '__main__':
    nuke.run()
```

Run tasks from command line:
```bash
nuke push
# or
./nukefile.py push

# dry run mode
nuke push --dry

# override config parameters
nuke convert --src_path=/src/dump
```

List all available tasks:
```bash
nuke # in the same folder where nukefile.py is
./nukefile.py
```

## Configuration

### Minimal Configuration

For simple tasks with just the `dry` flag:

```python
from nuclear import nuke

config, sh = nuke.init()

def build():
    sh<<"gcc build.c"

if __name__ == '__main__':
    nuke.run()
```

### Custom Configuration

Extend `nuke.NukeConfig` to add custom configuration fields:

```python
from nuclear import nuke
from pathlib import Path

class Config(nuke.NukeConfig):
    output_dir: str = 'dist'
    num_workers: int = 4
    api_url: str = 'https://api.example.com'

config, sh = nuke.init(Config, raw_output=True, print_log=True)

def build():
    """Build project with custom output directory"""
    sh << f"make build OUTPUT={config.output_dir}"

def test():
    """Run tests with worker count"""
    sh << f"pytest -n {config.num_workers} tests/"
```

### Loading Configuration from Files

Nuke automatically loads configuration from `.config.yaml` in the current directory:

```yaml
output_dir: build
num_workers: 8
api_url: https://staging.example.com
dry: false
```

CLI arguments override file configuration:

```bash
./nukefile.py --output-dir=/tmp/build --num-workers=16 build
```

## Shell Runner

The shell runner (`sh`) from `nuke.init()` provides convenient methods for running shell commands:

### Basic Usage

```python
from nuclear import nuke

config, sh = nuke.init()

def deploy():
    # All these are equivalent ways to run shell commands:
    sh("make deploy")
    sh << "make deploy"
    sh / "make deploy"
```

### Shell Options

Pass options to `nuke.init()` to configure how commands are executed:

```python
config, sh = nuke.init(
    Config,
    raw_output=True,      # Let subprocess manage stdout/stderr
    print_log=True,       # Print log message before running command
    print_stdout=False,   # Print live stdout as it runs
    workdir=None,         # Set working directory
    independent=False,    # Run independent process
)
```

### Dry-Run Support

Tasks automatically support dry-run mode if your config has a `dry` field:

```python
class Config(nuke.NukeConfig):
    dry: bool = False

config, sh = nuke.init(Config)

def deploy():
    sh << "rsync -avh dist/ /srv/www/"
```

Run in dry-mode:
```bash
python nukefile.py --dry deploy
```

This will log the command without executing it.

## Task Dependencies
Just call the dependencies tasks explicitly and mark the funcions with `functools.cache`
to make sure they would run just once.
```python
from functools import cache

from nuclear import nuke

config, sh = nuke.init()

@cache
def clean():
    sh / "rm -rf dist/ build/"

@cache
def build():
    clean()
    sh / "make build"

@cache
def test():
    build()
    sh / "pytest tests/"

def deploy():
    test()
    sh / "rsync -avh dist/ /srv/www/"

if __name__ == '__main__':
    nuke.run()
```

When you run `python nukefile.py deploy`, it will automatically run:
1. `clean()` (dependency of build)
2. `build()` (dependency of test)
3. `test()` (dependency of deploy)
4. `deploy()` (requested task)

Each task runs only once, even if multiple tasks depend on it.

## Validating Sources

Use `nuke.validate_sources()` to validate and convert file paths:

```python
from pathlib import Path
from nuclear import nuke

class Config(nuke.NukeConfig):
    sources: list[str] = [
        '/path/to/file1.txt',
        '/path/to/file2.txt',
    ]

config, sh = nuke.init(Config)

def process():
    """Process source files"""
    files: list[Path] = nuke.validate_sources(config.sources)
    for f in files:
        logger.info(f'Processing {f}')
```

This function:
- Converts strings to `Path` objects
- Checks for duplicate entries
- Verifies files exist
- Raises helpful errors if anything is wrong

## Error Handling

Nuke tasks use Nuclear's error handling system. Catch specific errors with:

```python
from nuclear import nuke, CommandError, logger

config, sh = nuke.init()

def cleanup():
    """Cleanup (may fail if nothing exists)"""
    try:
        sh / "rm -rf /tmp/cache"
    except CommandError as e:
        logger.warn('Cleanup failed', error=str(e))

def deploy():
    sh / "make deploy"
```

## Logging

Use `logger` to output status messages:

```python
from nuclear import nuke, logger

config, sh = nuke.init()

def build():
    logger.info('Starting build', output_dir=config.output_dir)
    sh / "make build"
    logger.info('Build completed')
```

## Advanced Example

Here's a more complete example with multiple configs, dependencies, and features:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "nuclear>=2.8.1",
#   "unidecode",
# ]
# ///
from pathlib import Path
from nuclear import nuke, logger, CommandError
from unidecode import unidecode

class Config(nuke.NukeConfig):
    source_files: list[str] = [
        '/opt/dump/movies-series/Bluey/S01/S01E22.mkv',
    ]
    output_offset: int = 200
    output_dir: str = 'output'

config, sh = nuke.init(Config, raw_output=True, print_log=True)

def clean():
    """Remove output directory"""
    sh / f"rm -rf {config.output_dir}"

@nuke.depends('clean')
def prepare():
    """Create output directories"""
    sh / f"mkdir -p {config.output_dir}/stories {config.output_dir}/custom"

@nuke.depends('prepare')
def process_stories():
    """Process story audio files"""
    sources: list[Path] = nuke.validate_sources(config.source_files)
    
    for i, f in enumerate(sources):
        filename = unidecode(f.stem)
        output = f'{config.output_dir}/stories/{config.output_offset + i} {filename}.mp3'
        
        if Path(output).exists():
            logger.debug('File exists, skipping', file=output)
            continue
        
        logger.info('Processing', source=f.name, output=output)
        sh(
            f'ffmpeg -i "{f.absolute()}" '
            f'-map 0:a:1 '
            f'-ss 00:00:25 '
            f'-filter:a "aresample=matrix_encoding=dplii" '
            f'-ac 2 -q:a 0 '
            f'"{output}"'
        )

def sync_usb():
    """Sync to USB drive"""
    logger.info('Syncing to USB', dry=config.dry)
    sh / "rsync -avh --delete --size-only /opt/dump/output/ /media/usb/"

def format_drive():
    """Format and sort FAT partition"""
    try:
        partition = '/dev/sda1'
        input(f"Press enter to confirm formatting {partition}...")
        sh / f"sudo fsck.vfat -r {partition}"
        sh / f"sudo fatsort -n {partition}"
        logger.info('Drive formatted and sorted')
    except CommandError as e:
        logger.error('Format failed', error=str(e))

if __name__ == '__main__':
    nuke.run()
```

Usage:
```bash
# List all tasks
python nukefile.py

# Run a single task
python nukefile.py process_stories

# Run in dry-run mode
python nukefile.py --dry process_stories

# Override config values
python nukefile.py --output-offset=300 --output-dir=dist process_stories

# Run with dependencies
python nukefile.py sync_usb  # automatically runs prepare, process_stories first
```

## Tips & Tricks

### Making nukefile.py Executable

Add a shebang and make it executable:

```bash
chmod +x nukefile.py
./nukefile.py build
```

Or use `uv` to run with dependencies:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "nuclear>=2.8.1",
# ]
# ///
```

### Using External Dependencies

With `uv` inline script mode, you can add external dependencies:

```python
#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "nuclear>=2.8.1",
#   "unidecode",
#   "pyyaml",
# ]
# ///
from nuclear import nuke
from unidecode import unidecode
```

### Logging Command Output

Use `print_log=True` to see what commands are being executed:

```python
config, sh = nuke.init(Config, print_log=True)
```

### Capturing Command Output

The shell runner returns command output:

```python
version = sh / "python --version"
logger.info('Python version', version=version.strip())
```

### Task with Parameters from Config

Use configuration values in your tasks:

```python
class Config(nuke.NukeConfig):
    build_dir: str = 'dist'
    parallel_jobs: int = 4

config, sh = nuke.init(Config)

def test():
    """Run parallel tests"""
    sh / f"pytest -n {config.parallel_jobs} tests/"

def build():
    """Build with custom directory"""
    sh / f"make build OUTPUT={config.build_dir}"
```
