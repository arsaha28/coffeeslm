from coffee_slm.data import download as dl


def _source_file(tmp_path, size: int):
    src = tmp_path / "source.txt"
    src.write_bytes(bytes(i % 256 for i in range(size)))
    return src


def test_downloads_whole_file(tmp_path):
    src = _source_file(tmp_path, 3000)
    dest = tmp_path / "out" / "copy.txt"
    assert dl.download(src.as_uri(), dest) == 3000
    assert dest.read_bytes() == src.read_bytes()


def test_stops_at_max_bytes_across_chunks(tmp_path, monkeypatch):
    monkeypatch.setattr(dl, "CHUNK_SIZE", 100)  # force many small chunks
    src = _source_file(tmp_path, 3000)
    dest = tmp_path / "copy.txt"
    assert dl.download(src.as_uri(), dest, max_bytes=1050) == 1050
    assert dest.read_bytes() == src.read_bytes()[:1050]
