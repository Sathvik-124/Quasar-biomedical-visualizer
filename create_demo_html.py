#!/usr/bin/env python3
"""
Create a demo HTML file with the biomedical signal visualization
This script will generate a standalone HTML file that you can open in any browser
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

def create_visualization():
    """Create the biomedical signal visualization"""
    
    print("Creating biomedical signal visualization...")
    
    # Load data
    df = pd.read_csv('EEG and ECG data_02_raw.csv', comment='#')
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Clean data
    ignore_cols = ["X3:", "Trigger", "Time_Offset", "ADC_Status", 
                   "ADC_Sequence", "Event", "Comments"]
    df_clean = df.drop(columns=[c for c in ignore_cols if c in df.columns], errors='ignore')
    
    time_col = "Time"
    time_series = df_clean[time_col]
    eeg_channels = [c for c in df_clean.columns 
                   if c not in [time_col, "X1:LEOG", "X2:REOG", "CM"]]
    ecg_channels = [c for c in ["X1:LEOG", "X2:REOG"] if c in df_clean.columns]
    cm_channel = "CM" if "CM" in df_clean.columns else None
    
    print(f"EEG channels: {len(eeg_channels)}")
    print(f"ECG channels: {len(ecg_channels)}")
    print(f"CM channel: {cm_channel}")
    
    # Create subplot
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"secondary_y": True}]],
        subplot_titles=("Biomedical Signals: EEG, ECG, and CM",)
    )
    
    # Colors for EEG channels
    colors_eeg = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
                  '#c49c94', '#f7b6d3', '#c7c7c7', '#dbdb8d', '#9edae5',
                  '#393b79']
    
    # Add EEG traces (show first 15 channels for clarity)
    for i, channel in enumerate(eeg_channels[:15]):
        color = colors_eeg[i % len(colors_eeg)]
        fig.add_trace(
            go.Scatter(
                x=time_series,
                y=df_clean[channel],
                mode='lines',
                name=f"EEG: {channel}",
                line=dict(color=color, width=1),
                hovertemplate=f"<b>{channel}</b><br>" +
                             "Time: %{x:.3f}s<br>" +
                             "EEG: %{y:.1f} µV<br>" +
                             "<extra></extra>"
            ),
            secondary_y=False
        )
    
    # Add ECG traces
    colors_ecg = ['#ff6b6b', '#4ecdc4']
    for i, channel in enumerate(ecg_channels):
        color = colors_ecg[i % len(colors_ecg)]
        fig.add_trace(
            go.Scatter(
                x=time_series,
                y=df_clean[channel],
                mode='lines',
                name=f"ECG: {channel}",
                line=dict(color=color, width=2),
                hovertemplate=f"<b>{channel}</b><br>" +
                             "Time: %{x:.3f}s<br>" +
                             "ECG: %{y:.1f} mV<br>" +
                             "<extra></extra>"
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
                name=f"CM: {cm_channel}",
                line=dict(color='#ff9f43', width=1.5),
                yaxis='y3',
                hovertemplate=f"<b>{cm_channel}</b><br>" +
                             "Time: %{x:.3f}s<br>" +
                             "CM: %{y:.1f} µV<br>" +
                             "<extra></extra>"
            ),
            secondary_y=False
        )
    
    # Update layout
    fig.update_layout(
        title={
            'text': "Interactive Biomedical Signal Visualization<br><sub>EEG (µV) | ECG (mV) | CM Reference</sub>",
            'x': 0.5,
            'font': {'size': 18}
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
        )
    )
    
    return fig

def main():
    try:
        # Create the visualization
        fig = create_visualization()
        
        # Save as standalone HTML file with config
        output_file = "biomedical_signals_demo.html"
        config = {
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
        fig.write_html(output_file, include_plotlyjs=True, config=config)
        
        print(f"\n✓ Visualization created successfully!")
        print(f"✓ Saved as: {output_file}")
        print(f"\nTo view the visualization:")
        print(f"1. Open {output_file} in your web browser")
        print(f"2. Or double-click the file to open it")
        
        print(f"\nFeatures available in the visualization:")
        print("- Scroll, pan, and zoom with mouse")
        print("- Range selector buttons (1s, 5s, 10s, 30s, All)")
        print("- Toggle channels on/off in legend")
        print("- Export to PNG via toolbar")
        print("- Hover for detailed signal values")
        print("- Range slider at bottom for navigation")
        
        return output_file
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
