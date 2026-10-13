#!/usr/bin/env python3
"""Simulation only: overwrites a bounded, explicitly named regular file."""
import argparse,csv,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
FILENAME='disposable_test_media.bin'
MAX_SIZE=1024*1024

def workspace_dir(name):
    base=Path(__file__).resolve().parents[1]
    target=(base/name).resolve()
    if target==base or base not in target.parents: raise ValueError('Workspace must be a subdirectory of the project')
    if target.is_symlink(): raise ValueError('Symlink workspace prohibited')
    return target

def media_path(folder):
    f=folder/FILENAME
    if f.is_symlink(): raise ValueError('Symlink media prohibited')
    return f

def init(folder,size):
    if not 1<=size<=1024: raise ValueError('Size must be 1..1024 KiB')
    folder.mkdir(parents=True,exist_ok=True)
    f=media_path(folder)
    with f.open('xb') as out: out.write(b'LAB_ONLY_NOT_REAL_MEDIA\n'*(size*1024//24+1))
    with f.open('r+b') as out: out.truncate(size*1024)
    return f

def sanitize(folder,operator):
    f=media_path(folder)
    if not f.is_file() or not 0<f.stat().st_size<=MAX_SIZE: raise ValueError('Missing or oversized demo file')
    size=f.stat().st_size
    with f.open('r+b',buffering=0) as out:
        out.write(bytes(size)); out.flush()
        import os; os.fsync(out.fileno())
    verified=verify(folder)
    record={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'asset_id':'DEMO-001','operator':operator,'method':'SIMULATED file overwrite','bytes':size,'verified_zero':verified,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()}
    with (folder/'custody.jsonl').open('a') as out: out.write(json.dumps(record)+'\n')
    return record

def verify(folder):
    f=media_path(folder)
    if not f.is_file() or not 0<f.stat().st_size<=MAX_SIZE: raise ValueError('Invalid demo file')
    return all(byte==0 for byte in f.read_bytes())

def main():
    p=argparse.ArgumentParser(description='Disposable file sanitization SIMULATION; never physical media')
    sub=p.add_subparsers(dest='action',required=True)
    for action in ('init','sanitize','verify'):
        q=sub.add_parser(action); q.add_argument('--workspace',required=True)
        if action=='init': q.add_argument('--size-kib',type=int,default=64)
        if action=='sanitize': q.add_argument('--operator',default='Lab Operator')
    a=p.parse_args(); folder=workspace_dir(a.workspace)
    if a.action=='init': print('Created:',init(folder,a.size_kib))
    elif a.action=='sanitize': print(json.dumps(sanitize(folder,a.operator),indent=2))
    else:
        good=verify(folder); print('PASS: all bytes zero' if good else 'FAIL: nonzero bytes remain'); raise SystemExit(0 if good else 1)
if __name__=='__main__': main()
