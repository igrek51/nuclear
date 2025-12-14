#!/usr/bin/env python
# !Turn off default shebang!

#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "nuclear",
# ]
# ///
from pathlib import Path

from nuclear import nuke, logger, shell


class Config:
    dry: bool = False
    bluey_sources: list[str] = [
        'S03/S03E13 Bluey - Podaj Paczkę.mkv',
        'S01/S01E48 Bluey - Dokuczanie.mkv',
        'S02/S02E42 Bluey - Kibel.mkv',
    ]
    bluey_offset: int = 200


config: Config = nuke.load_config(Config)  # loads .config.yaml or default
sh = nuke.sh(raw_output=True, print_log=True, dry=config.dry)  # generates logger.debug or shell(raw_output=True) caller based on --dry


def push():
    sh << f"echo 'hello world, offset={config.bluey_offset}'"


def bluey():
    sources: list[Path] = nuke.validate_sources(config.bluey_sources)  # convert to Path, check duplicates, existing files
    for i, f in enumerate(sources):

        filename = f.stem[7:]
        target = f'storytales/{config.bluey_offset + i} {filename}.mp3'
        if Path(target).exists():
            logger.debug('target already exists - skipping', target=target)
            continue
    
        sh(
            f'ffmpeg -i "{f.absolute()}"'
            f' -map 0:a:1'  # From input #0 select audio stream index #1 (second)
            f' -ss 00:00:25'
            f' -filter:a "pan=stereo|FL < 1.0*FL + 0.707*FC + 0.707*BL|FR < 1.0*FR + 0.707*FC + 0.707*BR,'  # downmix 5.1 to stereo
            f'aresample=matrix_encoding=dplii,'  # Dolby Pro Logic II matrix
            f'dynaudnorm=maxgain=50:framelen=400:gausssize=15"'  # Dynamic Audio Normalizer
            f' -ac 2 -q:a 0'  # output 2 channels, variable bitrate
            f' "{target}"'
        )


if __name__ == '__main__':
    nuke.run()
