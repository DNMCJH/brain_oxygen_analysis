# brain_oxygen_analysis

Real-time fNIRS (functional Near-Infrared Spectroscopy) brain oxygen analysis system.

End-to-end pipeline: from head-mounted sensors through MCU preprocessing to RK3588 NPU inference via Transformer networks.

## System Architecture

```
Sensors + Light Sources (730nm / 850nm)
        │
        ▼
    ADC (SPI) → MCU (frame packaging) → UART → RK3588 (Linux + NPU)
                                                  ├─ Pipeline 1: Frame parsing
                                                  ├─ Pipeline 2: Light → HbO/HbR
                                                  └─ Pipeline 3: Transformer inference
```

## Current Status

- **Phase 1 — Offline Analysis**: Done. Dual-wavelength signal demux tool working.
- **Phase 2 — MCU Firmware**: Not started. Hardware ready.
- **Phase 3 — RK3588 Data Pipeline**: Not started. Transformer network verified on NPU.
- **Phase 4 — Integration**: Pending Phase 2+3.

See [docs/system_report.md](docs/system_report.md) for full project status.

## Phase 1: Offline Signal Separation Tool

Detects interleaved dual-wavelength signals in raw fNIRS channels, separates them into independent wavelength components, and outputs clean data.

```bash
pip install -r requirements.txt
python -m src.main path/to/data.xlsx
```

Options:
- `-o <dir>` — custom output directory
- `--no-figures` — skip figure generation

See [docs/report.md](docs/report.md) for detailed analysis findings.

## Project Structure

```
brain_oxygen_analysis/
├── src/
│   ├── config.py       # Hardware config: channel layout, source mapping
│   ├── loader.py       # Excel data loader
│   ├── demux.py        # Dual-wavelength signal demultiplexing
│   ├── visualize.py    # Heatmap, time series, demux comparison plots
│   └── main.py         # CLI entry + process() API
├── docs/
│   ├── report.md       # Data analysis report (Chinese)
│   └── system_report.md # System status report (Chinese)
├── Data.xlsx           # Raw measurement data
├── requirements.txt
└── output/             # Auto-generated on run
```

## License

MIT
