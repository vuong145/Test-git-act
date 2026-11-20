"""Verify descriptive Ban 2 artifacts without importing hypothesis testing."""
from m2_common import load_foundation, path, read_json, require, digest, verify_hashes


def verified_multivariate():
    cfg, foundation = load_foundation()
    reports = path(cfg['outputs']['ban2']['reports'])
    pointer = read_json(reports / 'run_manifest.json')
    record = path(pointer['record'])
    require(record.is_relative_to(reports / 'runs'), 'Invalid branch record path')
    require(digest(record) == pointer['sha256'], 'Branch pointer changed')
    manifest = read_json(record)
    require(manifest['status'] == 'passed' and manifest['run_id'] == pointer['run_id'], 'Invalid run state')
    require(manifest['foundation_manifest_sha256'] == digest(path('Bao cao EDA/common/foundation_manifest.json')), 'Stale foundation')
    for key in ('inputs', 'code', 'configs', 'outputs'):
        verify_hashes(manifest[key])
    return cfg, foundation, record.parent, manifest
