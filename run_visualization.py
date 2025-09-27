#!/usr/bin/env python3
"""
Simple script to run the biomedical signal visualization
"""

import sys
import os

def main():
    print("Biomedical Signal Visualization")
    print("=" * 40)
    
    # Check if data file exists
    data_file = "EEG and ECG data_02_raw.csv"
    if not os.path.exists(data_file):
        print(f"Error: {data_file} not found!")
        return
    
    try:
        # Import required packages
        print("Importing packages...")
        import pandas as pd
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        import numpy as np
        print("✓ All packages imported successfully")
        
        # Load data
        print(f"Loading data from {data_file}...")
        df = pd.read_csv(data_file, comment='#')
        print(f"✓ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        
        # Identify channels
        ignore_cols = ["X3:", "Trigger", "Time_Offset", "ADC_Status", 
                       "ADC_Sequence", "Event", "Comments"]
        df_clean = df.drop(columns=[c for c in ignore_cols if c in df.columns], errors='ignore')
        
        time_col = "Time"
        time_series = df_clean[time_col]
        eeg_channels = [c for c in df_clean.columns 
                       if c not in [time_col, "X1:LEOG", "X2:REOG", "CM"]]
        ecg_channels = [c for c in ["X1:LEOG", "X2:REOG"] if c in df_clean.columns]
        cm_channel = "CM" if "CM" in df_clean.columns else None
        
        print(f"✓ Found {len(eeg_channels)} EEG channels")
        print(f"✓ Found {len(ecg_channels)} ECG channels")
        print(f"✓ CM channel: {cm_channel}")
        
        # Create interactive plot
        print("Creating interactive visualization...")
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]],
            subplot_titles=("Biomedical Signals: EEG, ECG, and CM",)
        )
        
        # Add EEG traces (µV scale) - show first 10 for clarity
        colors_eeg = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        for i, channel in enumerate(eeg_channels[:10]):  # Show first 10 EEG channels
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
        
        # Add ECG traces (mV scale)
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
        
        # Add CM trace if exists
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
        
        # Update layout
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
        
        # Add range selector
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
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'biomedical_signals',
                    'height': 700,
                    'width': 1200,
                    'scale': 2
                }
            }
        )
        
        # Save as HTML and show
        output_file = "biomedical_signals_visualization.html"
        fig.write_html(output_file)
        print(f"✓ Visualization saved as: {output_file}")
        
        print("\n" + "=" * 40)
        print("VISUALIZATION READY!")
        print("=" * 40)
        print(f"✓ Interactive plot created successfully")
        print(f"✓ Saved as: {output_file}")
        print(f"✓ Open {output_file} in your browser to view the interactive plot")
        print("\nFeatures available:")
        print("- Scroll, pan, and zoom with mouse")
        print("- Range selector buttons for quick time navigation")
        print("- Toggle traces on/off in legend")
        print("- Export to PNG via toolbar")
        print("- Hover for detailed values")
        
        # Try to open in browser
        try:
            import webbrowser
            webbrowser.open(output_file)
            print(f"\n✓ Opening {output_file} in your default browser...")
        except:
            print(f"\nPlease manually open {output_file} in your browser")
        
        return fig
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        print("Please install required packages: pip install pandas plotly numpy")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
