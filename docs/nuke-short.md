# 🚀 Nuke - Task Runner

*Nuke* is a lightweight task runner built into Nuclear for automating project tasks.
It serves as a replacement for Makefile.

Define tasks as simple Python functions in a `nukefile.py`:

```python
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

# see available tasks
nuke
./nukefile.py

# dry run mode
nuke push --dry

# override config parameters
nuke convert --src_path=/src/dump
```

See [Nuke documentation](https://igrek51.github.io/nuclear/nuke/) for detailed guide.
