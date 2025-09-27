#!/usr/bin/env python3
"""
Demonstration script showing different features of the biomedical signal visualizer.

This script creates multiple plots showcasing various features and options.
"""

import os
import sys
from plot_signals_advanced import BiomedicalSignalVisualizer


def demo_basic_visualization():
    """Demonstrate basic visualization."""
    print("="*60)
    print("DEMO 1: Basic Visualization")
    print("="*60)
    
    visualizer = BiomedicalSignalVisualizer('EEG and ECG data_02_raw.csv')
    visualizer.load_data()
    visualizer.preprocess_data()
    
    fig = visualizer.create_interactive_plot()
    fig.write_html("demo_basic.html")
    print("✓ Basic plot saved as demo_basic.html")


def demo_channel_selection():
    """Demonstrate channel selection feature."""
    print("\n" + "="*60)
    print("DEMO 2: Channel Selection")
    print("="*60)
    
    visualizer = BiomedicalSignalVisualizer('EEG and ECG data_02_raw.csv')
    visualizer.load_data()
    visualizer.preprocess_data()
    
    # Select specific EEG channels (frontal and central)
    selected_eeg = ['Fz', 'Cz', 'F3', 'F4', 'C3', 'C4']
    selected_ecg = ['X1:LEOG', 'X2:REOG']  # Both ECG channels
    
    fig = visualizer.create_interactive_plot(
        selected_eeg=selected_eeg,
        selected_ecg=selected_ecg,
        show_cm=True
    )
    fig.write_html("demo_channel_selection.html")
    print("✓ Channel selection plot saved as demo_channel_selection.html")


def demo_normalization():
    """Demonstrate normalization features."""
    print("\n" + "="*60)
    print("DEMO 3: Normalization Options")
    print("="*60)
    
    visualizer = BiomedicalSignalVisualizer('EEG and ECG data_02_raw.csv')
    visualizer.load_data()
    visualizer.preprocess_data()
    
    # Select a few channels for clarity
    selected_eeg = ['Fz', 'Cz', 'Pz']
    selected_ecg = ['X1:LEOG']
    
    # Z-score normalization
    fig1 = visualizer.create_interactive_plot(
        selected_eeg=selected_eeg,
        selected_ecg=selected_ecg,
        show_cm=False,
        normalize='zscore'
    )
    fig1.write_html("demo_zscore_normalization.html")
    print("✓ Z-score normalization plot saved as demo_zscore_normalization.html")
    
    # Min-max normalization
    fig2 = visualizer.create_interactive_plot(
        selected_eeg=selected_eeg,
        selected_ecg=selected_ecg,
        show_cm=False,
        normalize='minmax'
    )
    fig2.write_html("demo_minmax_normalization.html")
    print("✓ Min-max normalization plot saved as demo_minmax_normalization.html")
    
    # Unit conversion (µV to mV)
    fig3 = visualizer.create_interactive_plot(
        selected_eeg=selected_eeg,
        selected_ecg=selected_ecg,
        show_cm=False,
        normalize='unit_convert'
    )
    fig3.write_html("demo_unit_conversion.html")
    print("✓ Unit conversion plot saved as demo_unit_conversion.html")


def demo_statistics():
    """Demonstrate statistics feature."""
    print("\n" + "="*60)
    print("DEMO 4: Channel Statistics")
    print("="*60)
    
    visualizer = BiomedicalSignalVisualizer('EEG and ECG data_02_raw.csv')
    visualizer.load_data()
    visualizer.preprocess_data()
    
    visualizer.print_statistics()


def demo_ecg_focus():
    """Demonstrate ECG-focused visualization."""
    print("\n" + "="*60)
    print("DEMO 5: ECG-Focused Visualization")
    print("="*60)
    
    visualizer = BiomedicalSignalVisualizer('EEG and ECG data_02_raw.csv')
    visualizer.load_data()
    visualizer.preprocess_data()
    
    # Focus on ECG channels with a few EEG channels for context
    selected_eeg = ['Fz', 'Cz']  # Minimal EEG for context
    selected_ecg = ['X1:LEOG', 'X2:REOG']  # Both ECG channels
    
    fig = visualizer.create_interactive_plot(
        selected_eeg=selected_eeg,
        selected_ecg=selected_ecg,
        show_cm=False  # Hide CM to focus on ECG
    )
    fig.write_html("demo_ecg_focus.html")
    print("✓ ECG-focused plot saved as demo_ecg_focus.html")


def demo_eeg_montage():
    """Demonstrate EEG montage view."""
    print("\n" + "="*60)
    print("DEMO 6: EEG Montage View")
    print("="*60)
    
    visualizer = BiomedicalSignalVisualizer('EEG and ECG data_02_raw.csv')
    visualizer.load_data()
    visualizer.preprocess_data()
    
    # Standard 10-20 system channels (available in the data)
    selected_eeg = ['Fp1', 'Fp2', 'F3', 'F4', 'Fz', 'C3', 'C4', 'Cz', 
                   'P3', 'P4', 'Pz', 'O1', 'O2']
    
    fig = visualizer.create_interactive_plot(
        selected_eeg=selected_eeg,
        selected_ecg=[],  # No ECG
        show_cm=False  # No CM
    )
    fig.write_html("demo_eeg_montage.html")
    print("✓ EEG montage plot saved as demo_eeg_montage.html")


def main():
    """Run all demonstrations."""
    print("Biomedical Signal Visualization - Feature Demonstrations")
    print("="*60)
    
    if not os.path.exists('EEG and ECG data_02_raw.csv'):
        print("Error: EEG and ECG data_02_raw.csv not found!")
        print("Please ensure the data file is in the current directory.")
        sys.exit(1)
    
    try:
        demo_basic_visualization()
        demo_channel_selection()
        demo_normalization()
        demo_statistics()
        demo_ecg_focus()
        demo_eeg_montage()
        
        print("\n" + "="*60)
        print("DEMONSTRATION COMPLETE")
        print("="*60)
        print("Generated files:")
        print("- demo_basic.html")
        print("- demo_channel_selection.html")
        print("- demo_zscore_normalization.html")
        print("- demo_minmax_normalization.html")
        print("- demo_unit_conversion.html")
        print("- demo_ecg_focus.html")
        print("- demo_eeg_montage.html")
        print("\nOpen these HTML files in your browser to explore the features!")
        
    except Exception as e:
        print(f"Error during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
