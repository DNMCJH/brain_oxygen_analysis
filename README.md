# brain_oxygen_analysis

Automated signal separation tool for dual-wavelength fNIRS brain oxygen data.

Detects interleaved dual-wavelength signals in raw fNIRS channels, separates them into independent wavelength components, and outputs clean data for downstream analysis.

## Quick Start

```bash
pip install -r requirements.txt
python -m src.main path/to/data.xlsx
```

See [docs/report.md](docs/report.md) for detailed analysis and findings.
