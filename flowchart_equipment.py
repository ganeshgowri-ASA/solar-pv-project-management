"""
FLOWCHART & EQUIPMENT MANAGEMENT MODULE
Module ID: FLOWCHART_EQUIPMENT_SESSION2

This module provides independent modular functions for:
1. Interactive workflow flowchart visualization
2. Equipment registry and management
3. Equipment availability tracking
4. Calibration alerts and maintenance logs

All functions are self-contained and use Streamlit session state for data storage.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

# MODULE_ID for tracking
MODULE_ID = 'FLOWCHART_EQUIPMENT'

# ============================================================================
# SAMPLE DATA INITIALIZATION
# ============================================================================

def initialize_workflow_data():
    """
    Initialize sample workflow data for testing.
    Creates nodes and edges for the workflow flowchart.

    Returns:
        None (stores data in session_state)
    """
    if 'workflow_data' not in st.session_state:
        # Define workflow nodes with hierarchy
        workflow_nodes = [
            # Level 0: Project
            {'id': 'proj_1', 'label': 'Solar PV Installation Project', 'type': 'Project',
             'status': 'in-progress', 'level': 0},

            # Level 1: Phases
            {'id': 'phase_1', 'label': 'Design Phase', 'type': 'Phase',
             'status': 'completed', 'level': 1},
            {'id': 'phase_2', 'label': 'Testing Phase', 'type': 'Phase',
             'status': 'in-progress', 'level': 1},
            {'id': 'phase_3', 'label': 'Deployment Phase', 'type': 'Phase',
             'status': 'pending', 'level': 1},

            # Level 2: Tasks
            {'id': 'task_1', 'label': 'System Design', 'type': 'Task',
             'status': 'completed', 'level': 2},
            {'id': 'task_2', 'label': 'Performance Testing', 'type': 'Task',
             'status': 'in-progress', 'level': 2},
            {'id': 'task_3', 'label': 'Safety Testing', 'type': 'Task',
             'status': 'in-progress', 'level': 2},
            {'id': 'task_4', 'label': 'Field Installation', 'type': 'Task',
             'status': 'pending', 'level': 2},

            # Level 3: Tests
            {'id': 'test_1', 'label': 'Voltage Test', 'type': 'Test',
             'status': 'completed', 'level': 3},
            {'id': 'test_2', 'label': 'Current Test', 'type': 'Test',
             'status': 'in-progress', 'level': 3},
            {'id': 'test_3', 'label': 'Insulation Test', 'type': 'Test',
             'status': 'blocked', 'level': 3},

            # Level 4: Approvals
            {'id': 'approval_1', 'label': 'Design Approval', 'type': 'Approval',
             'status': 'completed', 'level': 4},
            {'id': 'approval_2', 'label': 'Test Approval', 'type': 'Approval',
             'status': 'pending', 'level': 4},

            # Level 5: Reports
            {'id': 'report_1', 'label': 'Final Report', 'type': 'Report',
             'status': 'pending', 'level': 5},
        ]

        # Define edges (connections between nodes)
        workflow_edges = [
            # Project to Phases
            {'source': 'proj_1', 'target': 'phase_1'},
            {'source': 'proj_1', 'target': 'phase_2'},
            {'source': 'proj_1', 'target': 'phase_3'},

            # Phases to Tasks
            {'source': 'phase_1', 'target': 'task_1'},
            {'source': 'phase_2', 'target': 'task_2'},
            {'source': 'phase_2', 'target': 'task_3'},
            {'source': 'phase_3', 'target': 'task_4'},

            # Tasks to Tests
            {'source': 'task_2', 'target': 'test_1'},
            {'source': 'task_2', 'target': 'test_2'},
            {'source': 'task_3', 'target': 'test_3'},

            # Tests to Approvals
            {'source': 'test_1', 'target': 'approval_1'},
            {'source': 'test_2', 'target': 'approval_2'},
            {'source': 'test_3', 'target': 'approval_2'},

            # Approvals to Reports
            {'source': 'approval_1', 'target': 'report_1'},
            {'source': 'approval_2', 'target': 'report_1'},
        ]

        st.session_state.workflow_data = {
            'nodes': workflow_nodes,
            'edges': workflow_edges
        }


def initialize_equipment_data():
    """
    Initialize sample equipment registry data for testing.

    Returns:
        None (stores data in session_state)
    """
    if 'equipment_registry' not in st.session_state:
        # Equipment registry with detailed information
        equipment_registry = [
            {
                'equipment_id': 'EQ001',
                'name': 'Solar Panel Tester',
                'type': 'Testing Equipment',
                'model': 'SPT-5000',
                'serial': 'SN123456',
                'calibration_date': (datetime.now() - timedelta(days=300)).strftime('%Y-%m-%d'),
                'last_service': (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d'),
                'status': 'available',
                'location': 'Lab A',
                'tests_completed': 245,
                'avg_time': 45.5,
                'success_rate': 98.2,
                'downtime_hours': 12.5
            },
            {
                'equipment_id': 'EQ002',
                'name': 'Digital Multimeter',
                'type': 'Measurement',
                'model': 'DMM-7500',
                'serial': 'SN789012',
                'calibration_date': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
                'last_service': (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d'),
                'status': 'in-use',
                'location': 'Lab B',
                'tests_completed': 532,
                'avg_time': 12.3,
                'success_rate': 99.5,
                'downtime_hours': 3.2
            },
            {
                'equipment_id': 'EQ003',
                'name': 'Insulation Tester',
                'type': 'Testing Equipment',
                'model': 'IT-3000',
                'serial': 'SN345678',
                'calibration_date': (datetime.now() - timedelta(days=370)).strftime('%Y-%m-%d'),
                'last_service': (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'),
                'status': 'maintenance',
                'location': 'Maintenance',
                'tests_completed': 189,
                'avg_time': 38.7,
                'success_rate': 95.8,
                'downtime_hours': 45.0
            },
            {
                'equipment_id': 'EQ004',
                'name': 'Thermal Camera',
                'type': 'Imaging',
                'model': 'TC-9000',
                'serial': 'SN901234',
                'calibration_date': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                'last_service': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
                'status': 'available',
                'location': 'Lab A',
                'tests_completed': 78,
                'avg_time': 25.8,
                'success_rate': 97.4,
                'downtime_hours': 6.5
            },
            {
                'equipment_id': 'EQ005',
                'name': 'Power Analyzer',
                'type': 'Analysis',
                'model': 'PA-4500',
                'serial': 'SN567890',
                'calibration_date': (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d'),
                'last_service': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
                'status': 'available',
                'location': 'Lab C',
                'tests_completed': 412,
                'avg_time': 32.1,
                'success_rate': 98.9,
                'downtime_hours': 8.0
            }
        ]

        st.session_state.equipment_registry = equipment_registry

    # Initialize equipment bookings for availability calendar
    if 'equipment_bookings' not in st.session_state:
        bookings = []
        base_date = datetime.now()

        # Generate sample bookings
        for i in range(15):
            equipment_id = f"EQ{str(i % 5 + 1).zfill(3)}"
            start_date = base_date + timedelta(days=np.random.randint(-10, 20))
            duration = np.random.randint(1, 5)
            end_date = start_date + timedelta(days=duration)

            bookings.append({
                'booking_id': f'BK{str(i+1).zfill(4)}',
                'equipment_id': equipment_id,
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'booked_by': f'User {i % 3 + 1}',
                'purpose': ['Testing', 'Calibration', 'Maintenance', 'Research'][i % 4],
                'status': ['confirmed', 'pending', 'completed'][i % 3]
            })

        st.session_state.equipment_bookings = bookings

    # Initialize maintenance logs
    if 'maintenance_logs' not in st.session_state:
        logs = []

        for i in range(20):
            equipment_id = f"EQ{str(i % 5 + 1).zfill(3)}"
            log_date = datetime.now() - timedelta(days=np.random.randint(1, 180))

            logs.append({
                'log_id': f'ML{str(i+1).zfill(4)}',
                'equipment_id': equipment_id,
                'date': log_date.strftime('%Y-%m-%d %H:%M:%S'),
                'type': ['Calibration', 'Repair', 'Inspection', 'Cleaning'][i % 4],
                'technician': f'Tech {i % 4 + 1}',
                'notes': f'Routine maintenance performed. All systems operational.',
                'cost': np.random.randint(100, 1000),
                'duration_hours': np.random.randint(1, 8)
            })

        # Sort by date descending
        logs.sort(key=lambda x: x['date'], reverse=True)
        st.session_state.maintenance_logs = logs


# ============================================================================
# FLOWCHART VIEW MODULE
# ============================================================================

def get_status_color(status: str) -> str:
    """
    Get color code for status.

    Args:
        status: Status string (pending, in-progress, completed, blocked)

    Returns:
        Color hex code
    """
    color_map = {
        'pending': '#808080',      # Gray
        'in-progress': '#FFD700',  # Yellow
        'completed': '#00AA00',    # Green
        'blocked': '#FF0000'       # Red
    }
    return color_map.get(status, '#808080')


def create_flowchart_layout(nodes: List[Dict], edges: List[Dict]) -> Tuple[Dict, Dict]:
    """
    Create hierarchical layout for flowchart nodes.

    Args:
        nodes: List of node dictionaries
        edges: List of edge dictionaries

    Returns:
        Tuple of (positions dict, node_map dict)
    """
    # Group nodes by level
    levels = {}
    for node in nodes:
        level = node['level']
        if level not in levels:
            levels[level] = []
        levels[level].append(node)

    # Calculate positions
    positions = {}
    node_map = {node['id']: node for node in nodes}

    level_height = 1.5
    max_level = max(levels.keys())

    for level, level_nodes in levels.items():
        num_nodes = len(level_nodes)
        node_width = 8.0 / max(num_nodes, 1)

        for i, node in enumerate(level_nodes):
            x = (i + 0.5) * node_width
            y = (max_level - level) * level_height
            positions[node['id']] = {'x': x, 'y': y}

    return positions, node_map


def render_flowchart_view():
    """
    Render interactive workflow flowchart using Plotly.

    Creates a hierarchical flowchart with:
    - Nodes colored by status
    - Interactive hover details
    - Click handlers for drill-down
    - Edge connections showing workflow

    Returns:
        None (renders directly to Streamlit)
    """
    try:
        # Initialize data if needed
        initialize_workflow_data()

        # Get workflow data
        workflow_data = st.session_state.workflow_data
        nodes = workflow_data['nodes']
        edges = workflow_data['edges']

        # Create layout
        positions, node_map = create_flowchart_layout(nodes, edges)

        # Create figure
        fig = go.Figure()

        # Add edges first (so they appear behind nodes)
        for edge in edges:
            source = edge['source']
            target = edge['target']

            if source in positions and target in positions:
                x0, y0 = positions[source]['x'], positions[source]['y']
                x1, y1 = positions[target]['x'], positions[target]['y']

                fig.add_trace(go.Scatter(
                    x=[x0, x1],
                    y=[y0, y1],
                    mode='lines',
                    line=dict(color='#CCCCCC', width=2),
                    hoverinfo='skip',
                    showlegend=False
                ))

        # Add nodes grouped by status for legend
        status_groups = {}
        for node in nodes:
            status = node['status']
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(node)

        # Add nodes by status group
        for status, status_nodes in status_groups.items():
            node_x = []
            node_y = []
            node_text = []
            node_hover = []

            for node in status_nodes:
                pos = positions[node['id']]
                node_x.append(pos['x'])
                node_y.append(pos['y'])
                node_text.append(node['label'])

                hover_text = (
                    f"<b>{node['label']}</b><br>"
                    f"Type: {node['type']}<br>"
                    f"Status: {node['status']}<br>"
                    f"ID: {node['id']}"
                )
                node_hover.append(hover_text)

            fig.add_trace(go.Scatter(
                x=node_x,
                y=node_y,
                mode='markers+text',
                name=status.title(),
                marker=dict(
                    size=30,
                    color=get_status_color(status),
                    line=dict(color='white', width=2)
                ),
                text=node_text,
                textposition="bottom center",
                textfont=dict(size=10),
                hovertext=node_hover,
                hoverinfo='text',
                hoverlabel=dict(bgcolor='white')
            ))

        # Update layout
        fig.update_layout(
            title={
                'text': 'Project Workflow Flowchart',
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#333333'}
            },
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            hovermode='closest',
            plot_bgcolor='#F8F9FA',
            paper_bgcolor='white',
            height=700,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False,
                range=[-0.5, 8.5]
            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            ),
            margin=dict(l=20, r=20, t=80, b=20)
        )

        # Display the flowchart
        st.plotly_chart(fig, use_container_width=True)

        # Display detailed node information
        st.subheader("Workflow Details")

        # Create tabs for different node types
        tabs = st.tabs(["All Nodes", "Projects", "Phases", "Tasks", "Tests", "Approvals", "Reports"])

        with tabs[0]:
            df_nodes = pd.DataFrame(nodes)
            st.dataframe(
                df_nodes[['id', 'label', 'type', 'status', 'level']],
                use_container_width=True,
                hide_index=True
            )

        # Filter by type for other tabs
        node_types = ["Project", "Phase", "Task", "Test", "Approval", "Report"]
        for i, node_type in enumerate(node_types, 1):
            with tabs[i]:
                filtered_nodes = [n for n in nodes if n['type'] == node_type]
                if filtered_nodes:
                    df_filtered = pd.DataFrame(filtered_nodes)
                    st.dataframe(
                        df_filtered[['id', 'label', 'status', 'level']],
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info(f"No {node_type} nodes found.")

        # Status summary
        st.subheader("Status Summary")
        status_counts = pd.DataFrame(nodes)['status'].value_counts()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Completed", status_counts.get('completed', 0))
        with col2:
            st.metric("In Progress", status_counts.get('in-progress', 0))
        with col3:
            st.metric("Pending", status_counts.get('pending', 0))
        with col4:
            st.metric("Blocked", status_counts.get('blocked', 0))

    except Exception as e:
        st.error(f"Error rendering flowchart: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


# ============================================================================
# EQUIPMENT MANAGEMENT MODULE
# ============================================================================

def check_calibration_alerts(equipment_df: pd.DataFrame) -> pd.DataFrame:
    """
    Check for equipment calibration alerts.

    Args:
        equipment_df: DataFrame with equipment data

    Returns:
        DataFrame with alert information
    """
    alerts = []
    today = datetime.now()
    warning_days = 30

    for _, eq in equipment_df.iterrows():
        try:
            cal_date = datetime.strptime(eq['calibration_date'], '%Y-%m-%d')
            days_until = (cal_date - today).days

            if days_until < 0:
                alerts.append({
                    'equipment_id': eq['equipment_id'],
                    'name': eq['name'],
                    'calibration_date': eq['calibration_date'],
                    'days_overdue': abs(days_until),
                    'alert_level': 'critical'
                })
            elif days_until <= warning_days:
                alerts.append({
                    'equipment_id': eq['equipment_id'],
                    'name': eq['name'],
                    'calibration_date': eq['calibration_date'],
                    'days_remaining': days_until,
                    'alert_level': 'warning'
                })
        except Exception as e:
            st.warning(f"Error parsing date for {eq['equipment_id']}: {str(e)}")

    return pd.DataFrame(alerts)


def render_equipment_dashboard():
    """
    Render equipment dashboard with overview, table, charts, and metrics.

    Displays:
    - Equipment inventory table
    - Performance metrics
    - Status distribution
    - Calibration alerts
    - Type distribution

    Returns:
        None (renders directly to Streamlit)
    """
    try:
        # Initialize data if needed
        initialize_equipment_data()

        # Get equipment data
        equipment_data = st.session_state.equipment_registry
        df = pd.DataFrame(equipment_data)

        st.title("Equipment Dashboard")
        st.markdown("---")

        # Top metrics
        st.subheader("Overview Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total Equipment", len(df))

        with col2:
            available = len(df[df['status'] == 'available'])
            st.metric("Available", available)

        with col3:
            in_use = len(df[df['status'] == 'in-use'])
            st.metric("In Use", in_use)

        with col4:
            avg_success = df['success_rate'].mean()
            st.metric("Avg Success Rate", f"{avg_success:.1f}%")

        with col5:
            total_tests = df['tests_completed'].sum()
            st.metric("Total Tests", total_tests)

        st.markdown("---")

        # Calibration Alerts
        st.subheader("Calibration Alerts")
        alerts_df = check_calibration_alerts(df)

        if len(alerts_df) > 0:
            critical_alerts = alerts_df[alerts_df['alert_level'] == 'critical']
            warning_alerts = alerts_df[alerts_df['alert_level'] == 'warning']

            if len(critical_alerts) > 0:
                st.error(f"⚠️ {len(critical_alerts)} equipment item(s) have OVERDUE calibration!")
                st.dataframe(critical_alerts, use_container_width=True, hide_index=True)

            if len(warning_alerts) > 0:
                st.warning(f"⚠️ {len(warning_alerts)} equipment item(s) require calibration within 30 days!")
                st.dataframe(warning_alerts, use_container_width=True, hide_index=True)
        else:
            st.success("✅ All equipment calibrations are up to date!")

        st.markdown("---")

        # Equipment Table
        st.subheader("Equipment Inventory")

        # Add filters
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df['status'].unique(),
                default=df['status'].unique()
            )

        with col_f2:
            type_filter = st.multiselect(
                "Filter by Type",
                options=df['type'].unique(),
                default=df['type'].unique()
            )

        with col_f3:
            location_filter = st.multiselect(
                "Filter by Location",
                options=df['location'].unique(),
                default=df['location'].unique()
            )

        # Apply filters
        filtered_df = df[
            (df['status'].isin(status_filter)) &
            (df['type'].isin(type_filter)) &
            (df['location'].isin(location_filter))
        ]

        # Display table
        st.dataframe(
            filtered_df[[
                'equipment_id', 'name', 'type', 'model', 'serial',
                'status', 'location', 'calibration_date', 'last_service'
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # Charts Section
        st.subheader("Equipment Analytics")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            # Status distribution pie chart
            status_counts = df['status'].value_counts()
            fig_status = go.Figure(data=[go.Pie(
                labels=status_counts.index,
                values=status_counts.values,
                hole=0.4,
                marker=dict(colors=['#00AA00', '#FFD700', '#FF6B6B'])
            )])
            fig_status.update_layout(
                title="Equipment Status Distribution",
                height=400
            )
            st.plotly_chart(fig_status, use_container_width=True)

        with chart_col2:
            # Type distribution bar chart
            type_counts = df['type'].value_counts()
            fig_type = go.Figure(data=[go.Bar(
                x=type_counts.index,
                y=type_counts.values,
                marker=dict(color='#4A90E2')
            )])
            fig_type.update_layout(
                title="Equipment by Type",
                xaxis_title="Type",
                yaxis_title="Count",
                height=400
            )
            st.plotly_chart(fig_type, use_container_width=True)

        # Performance metrics charts
        chart_col3, chart_col4 = st.columns(2)

        with chart_col3:
            # Success rate by equipment
            fig_success = go.Figure(data=[go.Bar(
                x=df['name'],
                y=df['success_rate'],
                marker=dict(
                    color=df['success_rate'],
                    colorscale='RdYlGn',
                    showscale=True,
                    cmin=90,
                    cmax=100
                ),
                text=df['success_rate'].apply(lambda x: f"{x:.1f}%"),
                textposition='outside'
            )])
            fig_success.update_layout(
                title="Success Rate by Equipment",
                xaxis_title="Equipment",
                yaxis_title="Success Rate (%)",
                height=400,
                yaxis=dict(range=[0, 105])
            )
            st.plotly_chart(fig_success, use_container_width=True)

        with chart_col4:
            # Downtime by equipment
            fig_downtime = go.Figure(data=[go.Bar(
                x=df['name'],
                y=df['downtime_hours'],
                marker=dict(color='#FF6B6B')
            )])
            fig_downtime.update_layout(
                title="Downtime by Equipment (Hours)",
                xaxis_title="Equipment",
                yaxis_title="Downtime (hours)",
                height=400
            )
            st.plotly_chart(fig_downtime, use_container_width=True)

        # Tests completed chart
        st.subheader("Test Performance")
        fig_tests = go.Figure()

        fig_tests.add_trace(go.Bar(
            name='Tests Completed',
            x=df['name'],
            y=df['tests_completed'],
            marker=dict(color='#4A90E2')
        ))

        fig_tests.add_trace(go.Scatter(
            name='Avg Time (min)',
            x=df['name'],
            y=df['avg_time'],
            yaxis='y2',
            mode='lines+markers',
            marker=dict(color='#FF9800', size=10),
            line=dict(width=2)
        ))

        fig_tests.update_layout(
            title="Tests Completed vs Average Time",
            xaxis_title="Equipment",
            yaxis_title="Tests Completed",
            yaxis2=dict(
                title="Avg Time (minutes)",
                overlaying='y',
                side='right'
            ),
            height=500,
            hovermode='x unified'
        )

        st.plotly_chart(fig_tests, use_container_width=True)

    except Exception as e:
        st.error(f"Error rendering equipment dashboard: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


def render_equipment_availability():
    """
    Render equipment availability calendar view with bookings.

    Displays:
    - Calendar/Gantt view of equipment bookings
    - Booking details table
    - Availability summary
    - Booking management interface

    Returns:
        None (renders directly to Streamlit)
    """
    try:
        # Initialize data if needed
        initialize_equipment_data()

        # Get data
        equipment_data = st.session_state.equipment_registry
        bookings_data = st.session_state.equipment_bookings

        st.title("Equipment Availability Calendar")
        st.markdown("---")

        # Summary metrics
        df_bookings = pd.DataFrame(bookings_data)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_bookings = len(df_bookings)
            st.metric("Total Bookings", total_bookings)

        with col2:
            confirmed = len(df_bookings[df_bookings['status'] == 'confirmed'])
            st.metric("Confirmed", confirmed)

        with col3:
            pending = len(df_bookings[df_bookings['status'] == 'pending'])
            st.metric("Pending", pending)

        with col4:
            completed = len(df_bookings[df_bookings['status'] == 'completed'])
            st.metric("Completed", completed)

        st.markdown("---")

        # Create Gantt chart for availability
        st.subheader("Equipment Booking Calendar")

        # Prepare data for Gantt chart
        gantt_data = []
        equipment_map = {eq['equipment_id']: eq['name'] for eq in equipment_data}

        for booking in bookings_data:
            gantt_data.append({
                'Equipment': equipment_map.get(booking['equipment_id'], booking['equipment_id']),
                'Start': booking['start_date'],
                'Finish': booking['end_date'],
                'Purpose': booking['purpose'],
                'Booked By': booking['booked_by'],
                'Status': booking['status'],
                'Booking ID': booking['booking_id']
            })

        df_gantt = pd.DataFrame(gantt_data)

        # Create Gantt chart
        color_map = {
            'confirmed': '#00AA00',
            'pending': '#FFD700',
            'completed': '#808080'
        }

        fig_gantt = go.Figure()

        for status in ['completed', 'pending', 'confirmed']:
            df_status = df_gantt[df_gantt['Status'] == status]

            for _, row in df_status.iterrows():
                fig_gantt.add_trace(go.Bar(
                    name=status.title(),
                    x=[pd.to_datetime(row['Finish']) - pd.to_datetime(row['Start'])],
                    y=[row['Equipment']],
                    base=pd.to_datetime(row['Start']),
                    orientation='h',
                    marker=dict(color=color_map[status]),
                    hovertemplate=(
                        f"<b>{row['Equipment']}</b><br>"
                        f"Booking: {row['Booking ID']}<br>"
                        f"Purpose: {row['Purpose']}<br>"
                        f"Booked By: {row['Booked By']}<br>"
                        f"Start: {row['Start']}<br>"
                        f"End: {row['Finish']}<br>"
                        f"Status: {row['Status']}<br>"
                        "<extra></extra>"
                    ),
                    showlegend=True if _ == 0 else False,
                    legendgroup=status
                ))

        fig_gantt.update_layout(
            title="Equipment Booking Timeline",
            xaxis_title="Date",
            yaxis_title="Equipment",
            barmode='overlay',
            height=max(400, len(equipment_data) * 50),
            hovermode='closest',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        st.plotly_chart(fig_gantt, use_container_width=True)

        st.markdown("---")

        # Bookings table
        st.subheader("Booking Details")

        # Add filters
        col_f1, col_f2 = st.columns(2)

        with col_f1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df_bookings['status'].unique(),
                default=df_bookings['status'].unique(),
                key='booking_status_filter'
            )

        with col_f2:
            purpose_filter = st.multiselect(
                "Filter by Purpose",
                options=df_bookings['purpose'].unique(),
                default=df_bookings['purpose'].unique(),
                key='booking_purpose_filter'
            )

        # Apply filters
        filtered_bookings = df_bookings[
            (df_bookings['status'].isin(status_filter)) &
            (df_bookings['purpose'].isin(purpose_filter))
        ]

        # Display table
        st.dataframe(
            filtered_bookings[[
                'booking_id', 'equipment_id', 'start_date', 'end_date',
                'booked_by', 'purpose', 'status'
            ]],
            use_container_width=True,
            hide_index=True
        )

        # Equipment availability status
        st.markdown("---")
        st.subheader("Current Equipment Status")

        # Check current availability
        today = datetime.now().strftime('%Y-%m-%d')
        current_bookings = df_bookings[
            (df_bookings['start_date'] <= today) &
            (df_bookings['end_date'] >= today) &
            (df_bookings['status'].isin(['confirmed', 'pending']))
        ]

        booked_equipment = set(current_bookings['equipment_id'].unique())

        availability_data = []
        for eq in equipment_data:
            is_booked = eq['equipment_id'] in booked_equipment
            availability_data.append({
                'Equipment ID': eq['equipment_id'],
                'Name': eq['name'],
                'Type': eq['type'],
                'Location': eq['location'],
                'Status': eq['status'],
                'Availability': '🔴 Booked' if is_booked else '🟢 Available'
            })

        df_availability = pd.DataFrame(availability_data)
        st.dataframe(df_availability, use_container_width=True, hide_index=True)

        # Utilization chart
        st.markdown("---")
        st.subheader("Equipment Utilization")

        utilization_data = []
        for eq in equipment_data:
            eq_bookings = df_bookings[df_bookings['equipment_id'] == eq['equipment_id']]
            total_days = 0

            for _, booking in eq_bookings.iterrows():
                start = datetime.strptime(booking['start_date'], '%Y-%m-%d')
                end = datetime.strptime(booking['end_date'], '%Y-%m-%d')
                total_days += (end - start).days + 1

            utilization_data.append({
                'Equipment': eq['name'],
                'Booking Days': total_days,
                'Total Bookings': len(eq_bookings)
            })

        df_utilization = pd.DataFrame(utilization_data)

        fig_util = go.Figure()

        fig_util.add_trace(go.Bar(
            name='Booking Days',
            x=df_utilization['Equipment'],
            y=df_utilization['Booking Days'],
            marker=dict(color='#4A90E2')
        ))

        fig_util.update_layout(
            title="Total Booking Days by Equipment",
            xaxis_title="Equipment",
            yaxis_title="Days Booked",
            height=400
        )

        st.plotly_chart(fig_util, use_container_width=True)

    except Exception as e:
        st.error(f"Error rendering equipment availability: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


def render_maintenance_logs():
    """
    Render maintenance logs with timestamps and filtering.

    Displays:
    - Maintenance history table
    - Cost analysis
    - Maintenance type distribution
    - Timeline view

    Returns:
        None (renders directly to Streamlit)
    """
    try:
        # Initialize data if needed
        initialize_equipment_data()

        # Get maintenance logs
        logs_data = st.session_state.maintenance_logs
        df_logs = pd.DataFrame(logs_data)

        st.title("Equipment Maintenance Logs")
        st.markdown("---")

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_logs = len(df_logs)
            st.metric("Total Logs", total_logs)

        with col2:
            total_cost = df_logs['cost'].sum()
            st.metric("Total Cost", f"${total_cost:,.0f}")

        with col3:
            avg_cost = df_logs['cost'].mean()
            st.metric("Avg Cost", f"${avg_cost:.0f}")

        with col4:
            total_hours = df_logs['duration_hours'].sum()
            st.metric("Total Hours", f"{total_hours:.0f}")

        st.markdown("---")

        # Filters
        st.subheader("Filter Logs")
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            equipment_filter = st.multiselect(
                "Equipment",
                options=df_logs['equipment_id'].unique(),
                default=df_logs['equipment_id'].unique(),
                key='maint_eq_filter'
            )

        with col_f2:
            type_filter = st.multiselect(
                "Maintenance Type",
                options=df_logs['type'].unique(),
                default=df_logs['type'].unique(),
                key='maint_type_filter'
            )

        with col_f3:
            tech_filter = st.multiselect(
                "Technician",
                options=df_logs['technician'].unique(),
                default=df_logs['technician'].unique(),
                key='maint_tech_filter'
            )

        # Apply filters
        filtered_logs = df_logs[
            (df_logs['equipment_id'].isin(equipment_filter)) &
            (df_logs['type'].isin(type_filter)) &
            (df_logs['technician'].isin(tech_filter))
        ]

        st.markdown("---")

        # Maintenance logs table
        st.subheader("Maintenance History")
        st.dataframe(
            filtered_logs[[
                'log_id', 'equipment_id', 'date', 'type',
                'technician', 'cost', 'duration_hours', 'notes'
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        # Analytics
        st.subheader("Maintenance Analytics")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            # Maintenance type distribution
            type_counts = filtered_logs['type'].value_counts()
            fig_type = go.Figure(data=[go.Pie(
                labels=type_counts.index,
                values=type_counts.values,
                hole=0.4
            )])
            fig_type.update_layout(
                title="Maintenance Type Distribution",
                height=400
            )
            st.plotly_chart(fig_type, use_container_width=True)

        with chart_col2:
            # Cost by type
            cost_by_type = filtered_logs.groupby('type')['cost'].sum().sort_values(ascending=False)
            fig_cost = go.Figure(data=[go.Bar(
                x=cost_by_type.index,
                y=cost_by_type.values,
                marker=dict(color='#FF6B6B')
            )])
            fig_cost.update_layout(
                title="Total Cost by Maintenance Type",
                xaxis_title="Type",
                yaxis_title="Cost ($)",
                height=400
            )
            st.plotly_chart(fig_cost, use_container_width=True)

        # Timeline chart
        st.subheader("Maintenance Timeline")

        # Parse dates for timeline
        filtered_logs['date_parsed'] = pd.to_datetime(filtered_logs['date'])
        filtered_logs_sorted = filtered_logs.sort_values('date_parsed')

        fig_timeline = go.Figure()

        for maint_type in filtered_logs_sorted['type'].unique():
            df_type = filtered_logs_sorted[filtered_logs_sorted['type'] == maint_type]

            fig_timeline.add_trace(go.Scatter(
                x=df_type['date_parsed'],
                y=df_type['cost'],
                mode='markers+lines',
                name=maint_type,
                marker=dict(size=10),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    "Date: %{x}<br>"
                    "Cost: $%{y}<br>"
                    "<extra></extra>"
                ),
                text=df_type['equipment_id']
            ))

        fig_timeline.update_layout(
            title="Maintenance Cost Timeline",
            xaxis_title="Date",
            yaxis_title="Cost ($)",
            height=500,
            hovermode='closest'
        )

        st.plotly_chart(fig_timeline, use_container_width=True)

        # Cost by equipment
        st.subheader("Cost by Equipment")
        cost_by_eq = filtered_logs.groupby('equipment_id')['cost'].sum().sort_values(ascending=False)

        fig_eq_cost = go.Figure(data=[go.Bar(
            x=cost_by_eq.index,
            y=cost_by_eq.values,
            marker=dict(
                color=cost_by_eq.values,
                colorscale='Reds',
                showscale=True
            ),
            text=cost_by_eq.values.apply(lambda x: f"${x:,.0f}"),
            textposition='outside'
        )])

        fig_eq_cost.update_layout(
            title="Total Maintenance Cost by Equipment",
            xaxis_title="Equipment ID",
            yaxis_title="Total Cost ($)",
            height=400
        )

        st.plotly_chart(fig_eq_cost, use_container_width=True)

    except Exception as e:
        st.error(f"Error rendering maintenance logs: {str(e)}")
        import traceback
        st.error(traceback.format_exc())


# ============================================================================
# MODULE TESTING & DEMONSTRATION
# ============================================================================

def demo_all_features():
    """
    Demonstration function to show all features of the module.
    Can be called from main app or run standalone for testing.

    Returns:
        None (renders directly to Streamlit)
    """
    st.set_page_config(
        page_title="Flowchart & Equipment Management Demo",
        page_icon="🔧",
        layout="wide"
    )

    st.title("🔧 Flowchart & Equipment Management Module")
    st.markdown(f"**Module ID:** `{MODULE_ID}`")
    st.markdown("---")

    # Create tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Flowchart View",
        "🔧 Equipment Dashboard",
        "📅 Equipment Availability",
        "🔨 Maintenance Logs"
    ])

    with tab1:
        render_flowchart_view()

    with tab2:
        render_equipment_dashboard()

    with tab3:
        render_equipment_availability()

    with tab4:
        render_maintenance_logs()

    # Footer
    st.markdown("---")
    st.markdown(
        f"**Module:** {MODULE_ID} | "
        "**Session:** FLOWCHART_EQUIPMENT_SESSION2 | "
        "**Version:** 1.0"
    )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Run demonstration if executed directly
    demo_all_features()
