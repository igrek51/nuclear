from pathlib import Path


def validate_sources(sources: list[str]) -> list[Path]:
    if len(sources) != len(set(sources)):
        dupes = [x for x in sources if sources.count(x) > 1]
        raise ValueError(f'duplicate sources: {dupes}')
    
    for source in sources:
        assert Path(source).exists(), f'source not found: {source}'

    return list(map(Path, sources))
