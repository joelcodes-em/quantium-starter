import chromedriver_autoinstaller
from dash.testing.application_runners import import_app
from dash.testing.composite import DashComposite
import pytest
import time

# Auto-install chromedriver for testing
chromedriver_autoinstaller.install()

# Import your actual app from vis.py
app = import_app("vis")

def test_header_present(dash_duo: DashComposite):
    """Test that the header and subtitle are present with correct text"""
    dash_duo.start_server(app)
    
    # Wait for elements to load
    dash_duo.wait_for_element("h1", timeout=10)
    
    # Check main header exists with correct text
    header = dash_duo.find_element("h1")
    assert header.text == "Soul Foods - Pink Morsel Performance"
    
    # Check subtitle exists with correct text
    subtitle = dash_duo.find_element("p")
    assert subtitle.text == "Regional Sales Analysis | Q1 2021"

def test_visualization_present(dash_duo: DashComposite):
    """Test that the visualization is present"""
    dash_duo.start_server(app)
    
    # Wait for the chart to load - using a more specific selector
    dash_duo.wait_for_element(".js-plotly-plot", timeout=15)
    
    # Check if visualization exists using Plotly's class
    visualization = dash_duo.find_element(".js-plotly-plot")
    assert visualization is not None
    assert visualization.is_displayed()

def test_region_picker_present(dash_duo):
    """Test that the region picker is present"""
    dash_duo.start_server(app)
    dash_duo.wait_for_element("input[type='radio']", timeout=15)
    radio_inputs = dash_duo.find_elements("input[type='radio']")
    assert len(radio_inputs) >= 1  # At least one radio button exists



def test_stats_table_present(dash_duo: DashComposite):
    """Test that the stats table is present"""
    dash_duo.start_server(app)
    
    # Wait for the stats table to load - it might take a moment to render
    time.sleep(3)
    
    # Check if stats table container exists
    stats_container = dash_duo.find_element("#stats-table")
    assert stats_container is not None
    assert stats_container.is_displayed()
    
    # Check that the table has content
    assert stats_container.text != ""