# Chromecast Control & Fuzzing Toolkit

A research toolkit for Chromecast-like devices:
- Discover & enumerate devices
- Collect recon data (status, installed apps)
- Fuzz HTTP endpoints (`/setup/*`, `/apps/*`)
- Control media playback, volume, and apps

## Features
- JSON + log outputs (per device, per run)
- Passive + active fuzzing
- Multi-device control (auto-detect single/multiple)

## Usage
```bash
pip install -r requirements.txt
python main.py

