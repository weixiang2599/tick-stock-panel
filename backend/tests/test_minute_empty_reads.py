from datetime import date, datetime

import polars as pl
import pytest

from app.tickflow.repository import DataStore, KlineRepository

DAY = date(2026, 11, 19)


def read(repo, kind, asset):
    if kind == 'single':
        return repo.get_minute('601857.SH', DAY, asset)
    if kind == 'batch':
        return repo.get_minute_batch(['601857.SH'], DAY, asset)
    return repo.get_minute_range(['601857.SH'], DAY, DAY, asset)


@pytest.mark.parametrize('asset', ['stock', 'etf'])
@pytest.mark.parametrize('kind', ['single', 'batch', 'range'])
def test_empty_reads_skip_parquet_and_see_later_writes(tmp_path, monkeypatch, asset, kind):
    repo = KlineRepository(DataStore(tmp_path))
    original = pl.scan_parquet
    calls = []

    def scan(*args, **kwargs):
        calls.append(args[0])
        return original(*args, **kwargs)

    monkeypatch.setattr(pl, 'scan_parquet', scan)
    assert read(repo, kind, asset).is_empty()
    assert calls == []
    root = tmp_path / ('kline_etf_minute' if asset == 'etf' else 'kline_minute')
    path = root / f'date={DAY}' / 'part.parquet'
    path.parent.mkdir(parents=True, exist_ok=True)
    pl.DataFrame({'symbol': ['601857.SH'], 'datetime': [datetime(2026, 11, 19, 9, 31)], 'close': [12.5]}).write_parquet(path)
    assert read(repo, kind, asset)['close'].to_list() == [12.5]
    assert len(calls) == 1


@pytest.mark.parametrize('kind', ['single', 'batch', 'range'])
def test_legacy_symbol_partitions_and_date_filters(tmp_path, kind):
    repo = KlineRepository(DataStore(tmp_path))
    path = tmp_path / 'kline_minute/symbol=601857.SH/part.parquet'
    path.parent.mkdir(parents=True)
    pl.DataFrame({'symbol': ['601857.SH'] * 2, 'datetime': [datetime(2026, 11, 18, 9, 31), datetime(2026, 11, 19, 9, 31)], 'close': [12.0, 12.5]}).write_parquet(path)
    assert read(repo, kind, 'stock')['close'].to_list() == [12.5]
