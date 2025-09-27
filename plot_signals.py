#!/usr/bin/env python3
"""
Biomedical Signal Processing Visualization Tool

This script loads EEG and ECG data from CSV files and creates interactive
visualizations using Plotly. It handles proper scaling for different signal
types and provides interactive features for data exploration.

Usage:
    python plot_signals.py [csv_file_path]

Author: Generated for Quasar Coding Challenge
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import argparse
import sys
import os


def load_data(file_path):
    """
    Load CSV data, skipping comment lines starting with '#'.
    
    Args:
        file_path (str): Path to the CSV file
        
    Returns:
        pandas.DataFrame: Loaded data with proper column headers
    """
    try:
        print(f"Loading data from: {file_path}")
        df = pd.read_csv(file_path, comment='#')
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


def preprocess_data(df):
    """
    Preprocess the data by identifying channels and cleaning unnecessary columns.
    
    Args:
        df (pandas.DataFrame): Raw data
        
    Returns:
        tuple: (time_series, eeg_channels, ecg_channels, cm_channel, df_clean)
    """
    # Define columns to ignore
    ignore_cols = ["X3:", "Trigger", "Time_Offset", "ADC_Status", 
                   "ADC_Sequence", "Event", "Comments"]
    
    # Remove ignored columns if they exist
    df_clean = df.drop(columns=[c for c in ignore_cols if c in df.columns], errors='ignore')
    
    # Identify time column
    time_col = "Time" if "Time" in df_clean.columns else df_clean.columns[0]
    time_series = df_clean[time_col]
    
    # Define EEG channels (all channels except time, ECG, and CM)
    eeg_channels = [c for c in df_clean.columns 
                   if c not in [time_col, "X1:LEOG", "X2:REOG", "CM"]]
    
    # Define ECG channels
    ecg_channels = [c for c in ["X1:LEOG", "X2:REOG"] if c in df_clean.columns]
    
    # CM channel
    cm_channel = "CM" if "CM" in df_clean.columns else None
    
    print(f"EEG channels ({len(eeg_channels)}): {eeg_channels}")
    print(f"ECG channels ({len(ecg_channels)}): {ecg_channels}")
    print(f"CM channel: {cm_channel}")
    
    return time_series, eeg_channels, ecg_channels, cm_channel, df_clean


def create_interactive_plot(time_series, eeg_channels, ecg_channels, cm_channel, df_clean):
    """
    Create an interactive Plotly visualization with proper scaling.
    
    Args:
        time_series (pandas.Series): Time data
        eeg_channels (list): List of EEG channel names
        ecg_channels (list): List of ECG channel names  
        cm_channel (str): CM channel name (if exists)
        df_clean (pandas.DataFrame): Cleaned data
        
    Returns:
        plotly.graph_objects.Figure: Interactive plot
    """
    # Create subplot with multiple y-axes
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"secondary_y": True}]],
        subplot_titles=("Biomedical Signals: EEG, ECG, and CM",)
    )
    
    # Add EEG traces (µV scale) - use different colors for visibility
    colors_eeg = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
                  '#c49c94', '#f7b6d3', '#c7c7c7', '#dbdb8d', '#9edae5',
                  '#393b79']
    
    for i, channel in enumerate(eeg_channels):
        color = colors_eeg[i % len(colors_eeg)]
        fig.add_trace(
            go.Scatter(
                x=time_series,
                y=df_clean[channel],
                mode='lines',
                name=channel,
                line=dict(color=color, width=1),
                yaxis='y'
            ),
            secondary_y=False
        )
    
    # Add ECG traces (mV scale) - separate axis
    colors_ecg = ['#ff6b6b', '#4ecdc4']
    for i, channel in enumerate(ecg_channels):
        color = colors_ecg[i % len(colors_ecg)]
        fig.add_trace(
            go.Scatter(
                x=time_series,
                y=df_clean[channel],
                mode='lines',
                name=channel,
                line=dict(color=color, width=2),
                yaxis='y2'
            ),
            secondary_y=True
        )
    
    # Add CM trace (large amplitude, separate axis)
    if cm_channel:
        fig.add_trace(
            go.Scatter(
                x=time_series,
                y=df_clean[cm_channel],
                mode='lines',
                name=cm_channel,
                line=dict(color='#ff9f43', width=1.5),
                yaxis='y3'
            ),
            secondary_y=False
        )
    
    # Update layout with multiple y-axes
    fig.update_layout(
        title={
            'text': "Interactive Biomedical Signal Visualization<br><sub>EEG (µV) | ECG (mV) | CM Reference</sub>",
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
    fig.update_yaxes(
        title_text="EEG Channels (µV)",
        secondary_y=False,
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray'
    )
    
    fig.update_yaxes(
        title_text="ECG Channels (mV)",
        secondary_y=True,
        showgrid=False,
        side="right"
    )
    
    # Add third y-axis for CM if it exists
    if cm_channel:
        fig.update_layout(
            yaxis3=dict(
                title="CM Reference (µV)",
                overlaying="y",
                side="right",
                position=0.95,
                showgrid=False
            )
        )
    
    return fig


def add_export_features(fig):
    """
    Add export and interaction features to the plot.
    
    Args:
        fig (plotly.graph_objects.Figure): Plot to enhance
        
    Returns:
        plotly.graph_objects.Figure: Enhanced plot
    """
    # Add range selector buttons
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
        )
    )
    
    # Add download button configuration
    fig.update_layout(
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToAdd': ['drawline', 'eraseshape'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'biomedical_signals',
                'height': 700,
                'width': 1200,
                'scale': 2
            }
        }
    )
    
    return fig


def main():
    """Main function to run the biomedical signal visualization."""
    parser = argparse.ArgumentParser(description='Visualize EEG and ECG data')
    parser.add_argument('csv_file', nargs='?', default='EEG and ECG data_02_raw.csv',
                       help='Path to CSV file (default: EEG and ECG data_02_raw.csv)')
    parser.add_argument('--export', action='store_true',
                       help='Export plot as HTML file')
    parser.add_argument('--no-show', action='store_true',
                       help='Do not display plot in browser')
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.csv_file):
        print(f"Error: File '{args.csv_file}' not found.")
        sys.exit(1)
    
    # Load and preprocess data
    df = load_data(args.csv_file)
    time_series, eeg_channels, ecg_channels, cm_channel, df_clean = preprocess_data(df)
    
    # Create interactive plot
    print("Creating interactive visualization...")
    fig = create_interactive_plot(time_series, eeg_channels, ecg_channels, cm_channel, df_clean)
    
    # Add export features
    fig = add_export_features(fig)
    
    # Export to HTML if requested
    if args.export:
        output_file = "biomedical_signals_plot.html"
        fig.write_html(output_file)
        print(f"Plot exported to: {output_file}")
    
    # Show plot unless --no-show is specified
    if not args.no_show:
        print("Displaying interactive plot...")
        fig.show()
    else:
        print("Plot created successfully. Use --no-show=False to display.")
    
    print("\nFeatures available:")
    print("- Scroll, pan, and zoom with mouse")
    print("- Range selector buttons for quick time navigation")
    print("- Toggle traces on/off in legend")
    print("- Export to PNG via toolbar")
    print("- Hover for detailed values")
    
    return fig


if __name__ == "__main__":
    main()
