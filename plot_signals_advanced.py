#!/usr/bin/env python3
"""
Advanced Biomedical Signal Processing Visualization Tool

Enhanced version with channel selection, normalization options, and additional
interactive features for comprehensive biomedical signal analysis.

Usage:
    python plot_signals_advanced.py [csv_file_path] [options]

Author: Generated for Quasar Coding Challenge
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import argparse
import sys
import os
from typing import List, Dict, Tuple


class BiomedicalSignalVisualizer:
    """Advanced biomedical signal visualization with interactive features."""
    
    def __init__(self, csv_file: str):
        """Initialize the visualizer with data file."""
        self.csv_file = csv_file
        self.df = None
        self.time_series = None
        self.eeg_channels = []
        self.ecg_channels = []
        self.cm_channel = None
        self.df_clean = None
        
    def load_data(self) -> pd.DataFrame:
        """Load CSV data, skipping comment lines."""
        try:
            print(f"Loading data from: {self.csv_file}")
            self.df = pd.read_csv(self.csv_file, comment='#')
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            sys.exit(1)
    
    def preprocess_data(self) -> Tuple[List[str], List[str], str]:
        """Preprocess data and identify channels."""
        # Define columns to ignore
        ignore_cols = ["X3:", "Trigger", "Time_Offset", "ADC_Status", 
                       "ADC_Sequence", "Event", "Comments"]
        
        # Remove ignored columns
        self.df_clean = self.df.drop(columns=[c for c in ignore_cols if c in self.df.columns], errors='ignore')
        
        # Identify time column
        time_col = "Time" if "Time" in self.df_clean.columns else self.df_clean.columns[0]
        self.time_series = self.df_clean[time_col]
        
        # Identify channels
        self.eeg_channels = [c for c in self.df_clean.columns 
                           if c not in [time_col, "X1:LEOG", "X2:REOG", "CM"]]
        self.ecg_channels = [c for c in ["X1:LEOG", "X2:REOG"] if c in self.df_clean.columns]
        self.cm_channel = "CM" if "CM" in self.df_clean.columns else None
        
        print(f"EEG channels ({len(self.eeg_channels)}): {self.eeg_channels[:5]}...")
        print(f"ECG channels ({len(self.ecg_channels)}): {self.ecg_channels}")
        print(f"CM channel: {self.cm_channel}")
        
        return self.eeg_channels, self.ecg_channels, self.cm_channel
    
    def normalize_signals(self, method: str = 'zscore') -> pd.DataFrame:
        """Apply normalization to signals."""
        df_norm = self.df_clean.copy()
        
        if method == 'zscore':
            # Z-score normalization
            for channel in self.eeg_channels + self.ecg_channels:
                if channel in df_norm.columns:
                    df_norm[channel] = (df_norm[channel] - df_norm[channel].mean()) / df_norm[channel].std()
        elif method == 'minmax':
            # Min-max normalization
            for channel in self.eeg_channels + self.ecg_channels:
                if channel in df_norm.columns:
                    min_val, max_val = df_norm[channel].min(), df_norm[channel].max()
                    df_norm[channel] = (df_norm[channel] - min_val) / (max_val - min_val)
        elif method == 'unit_convert':
            # Convert µV to mV for EEG channels
            for channel in self.eeg_channels:
                if channel in df_norm.columns:
                    df_norm[channel] = df_norm[channel] / 1000.0
        
        return df_norm
    
    def create_interactive_plot(self, 
                              selected_eeg: List[str] = None,
                              selected_ecg: List[str] = None,
                              show_cm: bool = True,
                              normalize: str = None) -> go.Figure:
        """Create interactive visualization with advanced features."""
        
        # Use selected channels or all channels
        eeg_to_plot = selected_eeg if selected_eeg else self.eeg_channels
        ecg_to_plot = selected_ecg if selected_ecg else self.ecg_channels
        
        # Apply normalization if requested
        df_to_plot = self.normalize_signals(normalize) if normalize else self.df_clean
        
        # Create subplot
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]],
            subplot_titles=("Advanced Biomedical Signal Visualization",)
        )
        
        # Color palettes
        colors_eeg = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                      '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
                      '#c49c94', '#f7b6d3', '#c7c7c7', '#dbdb8d', '#9edae5',
                      '#393b79', '#ff7f0e']
        
        colors_ecg = ['#ff6b6b', '#4ecdc4']
        
        # Add EEG traces
        for i, channel in enumerate(eeg_to_plot):
            if channel in df_to_plot.columns:
                color = colors_eeg[i % len(colors_eeg)]
                y_axis = 'y' if not normalize else 'y1'
                
                fig.add_trace(
                    go.Scatter(
                        x=self.time_series,
                        y=df_to_plot[channel],
                        mode='lines',
                        name=f"EEG: {channel}",
                        line=dict(color=color, width=1),
                        hovertemplate=f"<b>{channel}</b><br>" +
                                     "Time: %{x:.3f}s<br>" +
                                     "Value: %{y:.2f}<br>" +
                                     "<extra></extra>"
                    ),
                    secondary_y=False
                )
        
        # Add ECG traces
        for i, channel in enumerate(ecg_to_plot):
            if channel in df_to_plot.columns:
                color = colors_ecg[i % len(colors_ecg)]
                fig.add_trace(
                    go.Scatter(
                        x=self.time_series,
                        y=df_to_plot[channel],
                        mode='lines',
                        name=f"ECG: {channel}",
                        line=dict(color=color, width=2),
                        hovertemplate=f"<b>{channel}</b><br>" +
                                     "Time: %{x:.3f}s<br>" +
                                     "Value: %{y:.2f}<br>" +
                                     "<extra></extra>"
                    ),
                    secondary_y=True
                )
        
        # Add CM trace
        if show_cm and self.cm_channel and self.cm_channel in df_to_plot.columns:
            fig.add_trace(
                go.Scatter(
                    x=self.time_series,
                    y=df_to_plot[self.cm_channel],
                    mode='lines',
                    name=f"CM: {self.cm_channel}",
                    line=dict(color='#ff9f43', width=1.5),
                    yaxis='y3',
                    hovertemplate=f"<b>{self.cm_channel}</b><br>" +
                                 "Time: %{x:.3f}s<br>" +
                                 "Value: %{y:.2f}<br>" +
                                 "<extra></extra>"
                ),
                secondary_y=False
            )
        
        # Update layout
        title_suffix = f" (Normalized: {normalize})" if normalize else ""
        fig.update_layout(
            title={
                'text': f"Interactive Biomedical Signal Visualization{title_suffix}<br>" +
                       "<sub>EEG | ECG | CM Reference</sub>",
                'x': 0.5,
                'font': {'size': 16}
            },
            xaxis=dict(
                title="Time (seconds)",
                rangeslider=dict(visible=True),
                type="linear"
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10)
            ),
            height=700,
            showlegend=True,
            hovermode='x unified'
        )
        
        # Configure y-axes
        y_title = "EEG (µV)" if not normalize else f"EEG ({normalize})"
        fig.update_yaxes(
            title_text=y_title,
            secondary_y=False,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray'
        )
        
        ecg_title = "ECG (mV)" if not normalize else f"ECG ({normalize})"
        fig.update_yaxes(
            title_text=ecg_title,
            secondary_y=True,
            showgrid=False,
            side="right"
        )
        
        # Add third y-axis for CM if it exists
        if show_cm and self.cm_channel:
            cm_title = "CM (µV)" if not normalize else f"CM ({normalize})"
            fig.update_layout(
                yaxis3=dict(
                    title=cm_title,
                    overlaying="y",
                    side="right",
                    position=0.95,
                    showgrid=False
                )
            )
        
        # Add range selector and export features
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1s", step="second", stepmode="backward"),
                        dict(count=5, label="5s", step="second", stepmode="backward"),
                        dict(count=10, label="10s", step="second", stepmode="backward"),
                        dict(count=30, label="30s", step="second", stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            ),
            config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToAdd': ['drawline', 'eraseshape'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'biomedical_signals_advanced',
                    'height': 700,
                    'width': 1200,
                    'scale': 2
                }
            }
        )
        
        return fig
    
    def export_plot(self, fig: go.Figure, filename: str = "biomedical_signals_advanced.html"):
        """Export plot to HTML file."""
        try:
            fig.write_html(filename)
            print(f"Plot exported to: {filename}")
        except Exception as e:
            print(f"Error exporting plot: {e}")
    
    def get_channel_statistics(self) -> Dict:
        """Get basic statistics for all channels."""
        stats = {}
        
        for channel in self.eeg_channels + self.ecg_channels:
            if channel in self.df_clean.columns:
                data = self.df_clean[channel]
                stats[channel] = {
                    'mean': data.mean(),
                    'std': data.std(),
                    'min': data.min(),
                    'max': data.max(),
                    'range': data.max() - data.min()
                }
        
        return stats
    
    def print_statistics(self):
        """Print channel statistics."""
        stats = self.get_channel_statistics()
        
        print("\n" + "="*60)
        print("CHANNEL STATISTICS")
        print("="*60)
        
        for channel, stat in stats.items():
            print(f"\n{channel}:")
            print(f"  Mean: {stat['mean']:.2f}")
            print(f"  Std:  {stat['std']:.2f}")
            print(f"  Range: {stat['min']:.2f} to {stat['max']:.2f}")
            print(f"  Span: {stat['range']:.2f}")


def main():
    """Main function with advanced options."""
    parser = argparse.ArgumentParser(
        description='Advanced Biomedical Signal Visualization Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python plot_signals_advanced.py                                    # Basic usage
  python plot_signals_advanced.py data.csv --eeg Fz,Cz,Pz          # Select specific EEG channels
  python plot_signals_advanced.py --normalize zscore                # Z-score normalization
  python plot_signals_advanced.py --export --stats                  # Export and show statistics
  python plot_signals_advanced.py --no-cm --ecg X1:LEOG             # Hide CM, select ECG channel
        """
    )
    
    parser.add_argument('csv_file', nargs='?', default='EEG and ECG data_02_raw.csv',
                       help='Path to CSV file (default: EEG and ECG data_02_raw.csv)')
    parser.add_argument('--eeg', type=str,
                       help='Comma-separated EEG channels to display (e.g., Fz,Cz,Pz)')
    parser.add_argument('--ecg', type=str,
                       help='Comma-separated ECG channels to display (e.g., X1:LEOG,X2:REOG)')
    parser.add_argument('--no-cm', action='store_true',
                       help='Hide CM channel')
    parser.add_argument('--normalize', choices=['zscore', 'minmax', 'unit_convert'],
                       help='Apply normalization: zscore, minmax, or unit_convert (µV to mV)')
    parser.add_argument('--export', action='store_true',
                       help='Export plot as HTML file')
    parser.add_argument('--no-show', action='store_true',
                       help='Do not display plot in browser')
    parser.add_argument('--stats', action='store_true',
                       help='Display channel statistics')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.csv_file):
        print(f"Error: File '{args.csv_file}' not found.")
        sys.exit(1)
    
    # Initialize visualizer
    visualizer = BiomedicalSignalVisualizer(args.csv_file)
    
    # Load and preprocess data
    visualizer.load_data()
    visualizer.preprocess_data()
    
    # Parse channel selections
    selected_eeg = args.eeg.split(',') if args.eeg else None
    selected_ecg = args.ecg.split(',') if args.ecg else None
    
    # Validate selected channels
    if selected_eeg:
        invalid_eeg = [ch for ch in selected_eeg if ch not in visualizer.eeg_channels]
        if invalid_eeg:
            print(f"Warning: Invalid EEG channels: {invalid_eeg}")
            selected_eeg = [ch for ch in selected_eeg if ch in visualizer.eeg_channels]
    
    if selected_ecg:
        invalid_ecg = [ch for ch in selected_ecg if ch not in visualizer.ecg_channels]
        if invalid_ecg:
            print(f"Warning: Invalid ECG channels: {invalid_ecg}")
            selected_ecg = [ch for ch in selected_ecg if ch in visualizer.ecg_channels]
    
    # Show statistics if requested
    if args.stats:
        visualizer.print_statistics()
    
    # Create plot
    print("\nCreating advanced interactive visualization...")
    fig = visualizer.create_interactive_plot(
        selected_eeg=selected_eeg,
        selected_ecg=selected_ecg,
        show_cm=not args.no_cm,
        normalize=args.normalize
    )
    
    # Export if requested
    if args.export:
        output_file = "biomedical_signals_advanced.html"
        visualizer.export_plot(fig, output_file)
    
    # Show plot unless --no-show is specified
    if not args.no_show:
        print("Displaying interactive plot...")
        fig.show()
    else:
        print("Plot created successfully. Use --no-show=False to display.")
    
    print("\nAdvanced Features Available:")
    print("- Channel selection with --eeg and --ecg options")
    print("- Normalization options: zscore, minmax, unit_convert")
    print("- Statistics display with --stats")
    print("- Enhanced hover information")
    print("- CM channel toggle with --no-cm")
    print("- Export functionality with --export")
    
    return fig


if __name__ == "__main__":
    main()
