# Usage Examples

This document provides practical examples of how to use the biomedical signal visualization tools.

## Quick Start

### 1. Basic Usage
```bash
# Install dependencies
pip install -r requirements.txt

# Run basic visualization
python plot_signals.py
```

### 2. Advanced Features
```bash
# Run with advanced options
python plot_signals_advanced.py --help
```

## Command Examples

### Channel Selection
```bash
# Show only specific EEG channels
python plot_signals_advanced.py --eeg Fz,Cz,Pz

# Show only left ECG channel
python plot_signals_advanced.py --ecg X1:LEOG

# Combine specific EEG and ECG channels
python plot_signals_advanced.py --eeg Fz,Cz,F3,F4 --ecg X1:LEOG,X2:REOG
```

### Normalization Options
```bash
# Z-score normalization (mean=0, std=1)
python plot_signals_advanced.py --normalize zscore

# Min-max normalization (range 0-1)
python plot_signals_advanced.py --normalize minmax

# Convert EEG from µV to mV
python plot_signals_advanced.py --normalize unit_convert
```

### Export and Analysis
```bash
# Export without displaying
python plot_signals_advanced.py --export --no-show

# Show channel statistics
python plot_signals_advanced.py --stats

# Export with statistics
python plot_signals_advanced.py --export --stats
```

### Hide Channels
```bash
# Hide CM channel
python plot_signals_advanced.py --no-cm

# Focus only on EEG (no ECG, no CM)
python plot_signals_advanced.py --ecg "" --no-cm
```

## Interactive Features

### In the Browser
1. **Zoom**: Mouse wheel or zoom buttons
2. **Pan**: Click and drag
3. **Range Selection**: Use buttons (1s, 5s, 10s, 30s, All)
4. **Channel Toggle**: Click legend items
5. **Export**: Use camera icon in toolbar
6. **Range Slider**: Bottom panel for navigation

### Hover Information
- Hover over any point to see detailed values
- Shows time, channel name, and signal value
- Unified hover mode displays all channels at cursor position

## File Outputs

### HTML Files
- Interactive plots that open in browser
- Retain all interactive features
- Can be shared or embedded

### PNG Export
- High-resolution images (2400x1400 pixels)
- Perfect for reports and presentations
- Accessible via toolbar camera icon

## Troubleshooting

### Common Issues

1. **"File not found"**
   ```bash
   # Check file exists
   dir "EEG and ECG data_02_raw.csv"
   
   # Use full path
   python plot_signals.py "C:\full\path\to\file.csv"
   ```

2. **Import errors**
   ```bash
   # Reinstall packages
   pip install --upgrade pandas plotly numpy
   ```

3. **Plot not showing**
   ```bash
   # Export to HTML instead
   python plot_signals.py --export --no-show
   # Then open the HTML file manually
   ```

### Performance Tips

1. **Large datasets**: Use channel selection to reduce data
   ```bash
   python plot_signals_advanced.py --eeg Fz,Cz,Pz
   ```

2. **Memory issues**: Export without displaying
   ```bash
   python plot_signals_advanced.py --export --no-show
   ```

3. **Slow rendering**: Hide CM channel
   ```bash
   python plot_signals_advanced.py --no-cm
   ```

## Advanced Usage Patterns

### Research Workflow
```bash
# 1. Quick overview
python plot_signals.py

# 2. Focus on specific channels
python plot_signals_advanced.py --eeg Fz,Cz --ecg X1:LEOG --stats

# 3. Compare normalized vs raw
python plot_signals_advanced.py --normalize zscore --export
python plot_signals_advanced.py --export --no-show

# 4. Create publication-ready figures
# Use toolbar export with high DPI settings
```

### Clinical Analysis
```bash
# 1. Full montage view
python plot_signals_advanced.py --eeg Fp1,Fp2,F3,F4,Fz,C3,C4,Cz,P3,P4,Pz,O1,O2

# 2. ECG analysis
python plot_signals_advanced.py --ecg X1:LEOG,X2:REOG --no-cm

# 3. Export for documentation
python plot_signals_advanced.py --export --stats
```

### Educational Use
```bash
# 1. Run demonstrations
python demo_features.py

# 2. Show different normalizations
python plot_signals_advanced.py --normalize zscore --export
python plot_signals_advanced.py --normalize minmax --export

# 3. Channel-specific analysis
python plot_signals_advanced.py --eeg Fz --stats
```

## Batch Processing

### Multiple Files
```bash
# Process multiple files (create a batch script)
for %%f in (*.csv) do (
    python plot_signals_advanced.py "%%f" --export --no-show
)
```

### Automated Reports
```bash
# Generate statistics for all channels
python plot_signals_advanced.py --stats > channel_stats.txt

# Export multiple views
python plot_signals_advanced.py --eeg Fz,Cz,Pz --export --no-show
python plot_signals_advanced.py --ecg X1:LEOG,X2:REOG --export --no-show
```

## Integration Examples

### Jupyter Notebook
```python
from plot_signals_advanced import BiomedicalSignalVisualizer

# Load data
viz = BiomedicalSignalVisualizer('EEG and ECG data_02_raw.csv')
viz.load_data()
viz.preprocess_data()

# Create plot
fig = viz.create_interactive_plot(selected_eeg=['Fz', 'Cz'])
fig.show()

# Get statistics
stats = viz.get_channel_statistics()
print(stats)
```

### Python Script Integration
```python
import sys
sys.path.append('.')
from plot_signals_advanced import BiomedicalSignalVisualizer

def analyze_signals(file_path):
    viz = BiomedicalSignalVisualizer(file_path)
    viz.load_data()
    viz.preprocess_data()
    
    # Your analysis code here
    stats = viz.get_channel_statistics()
    
    # Create visualization
    fig = viz.create_interactive_plot()
    return fig, stats
```
