"""
Solar PV Project Management - Reports & WBS Module
MODULE_ID: REPORTS_WBS_SESSION5

This module provides:
1. Solar-specific report templates (Test Results, Equipment, Manpower, Project Status, Compliance)
2. Complete Work Breakdown Structure (WBS) with hierarchical management
3. Export capabilities (PDF, Excel, CSV, JSON)
4. Performance analytics and baseline comparison
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from io import BytesIO
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

MODULE_ID = 'REPORTS_WBS_SESSION5'

# ============================================================================
# INITIALIZATION & SAMPLE DATA
# ============================================================================

def init_reports_wbs_data():
    """Initialize WBS structure and reports data in session state"""

    # Initialize WBS structure
    if 'wbs_structure' not in st.session_state:
        st.session_state.wbs_structure = create_sample_wbs()

    # Initialize reports data
    if 'reports' not in st.session_state:
        st.session_state.reports = []

    # Initialize baselines
    if 'wbs_baselines' not in st.session_state:
        st.session_state.wbs_baselines = create_sample_baselines()

def create_sample_wbs():
    """Create sample WBS structure: 1 project, 3 phases, 12 tasks"""

    base_date = datetime.now()

    wbs_structure = [
        # Project Root
        {
            'wbs_id': 'WBS-1.0',
            'parent_id': None,
            'name': 'Solar PV Module Testing & Certification Project',
            'level': 0,
            'duration': 180,
            'start_date': base_date,
            'end_date': base_date + timedelta(days=180),
            'assigned_to': 'Project Manager',
            'status': 'In Progress',
            'progress': 45,
            'budget': 500000,
            'actual_cost': 225000,
            'type': 'project',
            'dependencies': [],
            'is_milestone': False,
            'is_critical': True
        },

        # Phase 1: Planning & Setup
        {
            'wbs_id': 'WBS-1.1',
            'parent_id': 'WBS-1.0',
            'name': 'Phase 1: Planning & Setup',
            'level': 1,
            'duration': 30,
            'start_date': base_date,
            'end_date': base_date + timedelta(days=30),
            'assigned_to': 'Planning Team',
            'status': 'Completed',
            'progress': 100,
            'budget': 75000,
            'actual_cost': 72000,
            'type': 'phase',
            'dependencies': [],
            'is_milestone': False,
            'is_critical': True
        },

        # Phase 1 Tasks
        {
            'wbs_id': 'WBS-1.1.1',
            'parent_id': 'WBS-1.1',
            'name': 'Project Charter & Scope Definition',
            'level': 2,
            'duration': 5,
            'start_date': base_date,
            'end_date': base_date + timedelta(days=5),
            'assigned_to': 'Sarah Johnson',
            'status': 'Completed',
            'progress': 100,
            'budget': 15000,
            'actual_cost': 14500,
            'type': 'task',
            'dependencies': [],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.1.2',
            'parent_id': 'WBS-1.1',
            'name': 'Resource Planning & Allocation',
            'level': 2,
            'duration': 10,
            'start_date': base_date + timedelta(days=5),
            'end_date': base_date + timedelta(days=15),
            'assigned_to': 'Michael Chen',
            'status': 'Completed',
            'progress': 100,
            'budget': 20000,
            'actual_cost': 19500,
            'type': 'task',
            'dependencies': ['WBS-1.1.1'],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.1.3',
            'parent_id': 'WBS-1.1',
            'name': 'Test Method Selection & Standards Review',
            'level': 2,
            'duration': 10,
            'start_date': base_date + timedelta(days=5),
            'end_date': base_date + timedelta(days=15),
            'assigned_to': 'David Wilson',
            'status': 'Completed',
            'progress': 100,
            'budget': 25000,
            'actual_cost': 23000,
            'type': 'task',
            'dependencies': ['WBS-1.1.1'],
            'is_milestone': False,
            'is_critical': False
        },
        {
            'wbs_id': 'WBS-1.1.4',
            'parent_id': 'WBS-1.1',
            'name': 'Equipment Setup & Calibration',
            'level': 2,
            'duration': 15,
            'start_date': base_date + timedelta(days=15),
            'end_date': base_date + timedelta(days=30),
            'assigned_to': 'Robert Martinez',
            'status': 'Completed',
            'progress': 100,
            'budget': 15000,
            'actual_cost': 15000,
            'type': 'task',
            'dependencies': ['WBS-1.1.2'],
            'is_milestone': True,
            'is_critical': True
        },

        # Phase 2: Testing Execution
        {
            'wbs_id': 'WBS-1.2',
            'parent_id': 'WBS-1.0',
            'name': 'Phase 2: Testing Execution',
            'level': 1,
            'duration': 90,
            'start_date': base_date + timedelta(days=30),
            'end_date': base_date + timedelta(days=120),
            'assigned_to': 'Testing Team',
            'status': 'In Progress',
            'progress': 60,
            'budget': 300000,
            'actual_cost': 135000,
            'type': 'phase',
            'dependencies': ['WBS-1.1'],
            'is_milestone': False,
            'is_critical': True
        },

        # Phase 2 Tasks
        {
            'wbs_id': 'WBS-1.2.1',
            'parent_id': 'WBS-1.2',
            'name': 'Visual Inspection & Documentation',
            'level': 2,
            'duration': 15,
            'start_date': base_date + timedelta(days=30),
            'end_date': base_date + timedelta(days=45),
            'assigned_to': 'Emily Rodriguez',
            'status': 'Completed',
            'progress': 100,
            'budget': 30000,
            'actual_cost': 28000,
            'type': 'task',
            'dependencies': ['WBS-1.1.4'],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.2.2',
            'parent_id': 'WBS-1.2',
            'name': 'Electrical Performance Testing (I-V Curve)',
            'level': 2,
            'duration': 25,
            'start_date': base_date + timedelta(days=45),
            'end_date': base_date + timedelta(days=70),
            'assigned_to': 'James Anderson',
            'status': 'Completed',
            'progress': 100,
            'budget': 80000,
            'actual_cost': 75000,
            'type': 'task',
            'dependencies': ['WBS-1.2.1'],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.2.3',
            'parent_id': 'WBS-1.2',
            'name': 'Environmental Testing (Thermal, Humidity)',
            'level': 2,
            'duration': 30,
            'start_date': base_date + timedelta(days=70),
            'end_date': base_date + timedelta(days=100),
            'assigned_to': 'Lisa Thompson',
            'status': 'In Progress',
            'progress': 70,
            'budget': 100000,
            'actual_cost': 65000,
            'type': 'task',
            'dependencies': ['WBS-1.2.2'],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.2.4',
            'parent_id': 'WBS-1.2',
            'name': 'Mechanical Load & Stress Testing',
            'level': 2,
            'duration': 20,
            'start_date': base_date + timedelta(days=100),
            'end_date': base_date + timedelta(days=120),
            'assigned_to': 'Kevin Brown',
            'status': 'Not Started',
            'progress': 0,
            'budget': 90000,
            'actual_cost': 0,
            'type': 'task',
            'dependencies': ['WBS-1.2.3'],
            'is_milestone': True,
            'is_critical': True
        },

        # Phase 3: Analysis & Reporting
        {
            'wbs_id': 'WBS-1.3',
            'parent_id': 'WBS-1.0',
            'name': 'Phase 3: Analysis & Reporting',
            'level': 1,
            'duration': 60,
            'start_date': base_date + timedelta(days=120),
            'end_date': base_date + timedelta(days=180),
            'assigned_to': 'Analysis Team',
            'status': 'Not Started',
            'progress': 0,
            'budget': 125000,
            'actual_cost': 0,
            'type': 'phase',
            'dependencies': ['WBS-1.2'],
            'is_milestone': False,
            'is_critical': True
        },

        # Phase 3 Tasks
        {
            'wbs_id': 'WBS-1.3.1',
            'parent_id': 'WBS-1.3',
            'name': 'Data Analysis & Statistical Evaluation',
            'level': 2,
            'duration': 20,
            'start_date': base_date + timedelta(days=120),
            'end_date': base_date + timedelta(days=140),
            'assigned_to': 'Amanda White',
            'status': 'Not Started',
            'progress': 0,
            'budget': 40000,
            'actual_cost': 0,
            'type': 'task',
            'dependencies': ['WBS-1.2.4'],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.3.2',
            'parent_id': 'WBS-1.3',
            'name': 'Compliance Verification & Standards Check',
            'level': 2,
            'duration': 15,
            'start_date': base_date + timedelta(days=140),
            'end_date': base_date + timedelta(days=155),
            'assigned_to': 'Christopher Lee',
            'status': 'Not Started',
            'progress': 0,
            'budget': 35000,
            'actual_cost': 0,
            'type': 'task',
            'dependencies': ['WBS-1.3.1'],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.3.3',
            'parent_id': 'WBS-1.3',
            'name': 'Final Report Generation & Documentation',
            'level': 2,
            'duration': 20,
            'start_date': base_date + timedelta(days=155),
            'end_date': base_date + timedelta(days=175),
            'assigned_to': 'Sarah Johnson',
            'status': 'Not Started',
            'progress': 0,
            'budget': 30000,
            'actual_cost': 0,
            'type': 'task',
            'dependencies': ['WBS-1.3.2'],
            'is_milestone': False,
            'is_critical': True
        },
        {
            'wbs_id': 'WBS-1.3.4',
            'parent_id': 'WBS-1.3',
            'name': 'Client Review & Project Closure',
            'level': 2,
            'duration': 5,
            'start_date': base_date + timedelta(days=175),
            'end_date': base_date + timedelta(days=180),
            'assigned_to': 'Project Manager',
            'status': 'Not Started',
            'progress': 0,
            'budget': 20000,
            'actual_cost': 0,
            'type': 'task',
            'dependencies': ['WBS-1.3.3'],
            'is_milestone': True,
            'is_critical': True
        }
    ]

    return wbs_structure

def create_sample_baselines():
    """Create 2 sample baselines for comparison"""

    base_date = datetime.now()

    baselines = [
        {
            'baseline_id': 'BL001',
            'name': 'Original Baseline',
            'created_date': base_date - timedelta(days=90),
            'created_by': 'Project Manager',
            'description': 'Initial project baseline approved by stakeholders',
            'total_duration': 180,
            'total_budget': 500000,
            'planned_end_date': base_date + timedelta(days=90)
        },
        {
            'baseline_id': 'BL002',
            'name': 'Revised Baseline (After Phase 1)',
            'created_date': base_date - timedelta(days=60),
            'created_by': 'Project Manager',
            'description': 'Updated baseline after Phase 1 completion review',
            'total_duration': 180,
            'total_budget': 485000,
            'planned_end_date': base_date + timedelta(days=90)
        }
    ]

    return baselines

# ============================================================================
# WBS UTILITY FUNCTIONS
# ============================================================================

def get_wbs_node(wbs_id):
    """Get a specific WBS node by ID"""
    for node in st.session_state.wbs_structure:
        if node['wbs_id'] == wbs_id:
            return node
    return None

def get_children(parent_id):
    """Get all children of a parent WBS node"""
    children = []
    for node in st.session_state.wbs_structure:
        if node['parent_id'] == parent_id:
            children.append(node)
    return children

def calculate_rollup_progress(wbs_id):
    """Calculate progress by averaging children's progress"""
    children = get_children(wbs_id)
    if not children:
        node = get_wbs_node(wbs_id)
        return node['progress'] if node else 0

    total_progress = sum(child['progress'] for child in children)
    return total_progress / len(children) if children else 0

def calculate_rollup_duration(wbs_id):
    """Calculate duration based on children"""
    children = get_children(wbs_id)
    if not children:
        node = get_wbs_node(wbs_id)
        return node['duration'] if node else 0

    return sum(child['duration'] for child in children)

def calculate_rollup_cost(wbs_id):
    """Calculate actual cost by summing children's costs"""
    children = get_children(wbs_id)
    if not children:
        node = get_wbs_node(wbs_id)
        return node['actual_cost'] if node else 0

    return sum(calculate_rollup_cost(child['wbs_id']) for child in children)

def calculate_rollup_budget(wbs_id):
    """Calculate budget by summing children's budgets"""
    children = get_children(wbs_id)
    if not children:
        node = get_wbs_node(wbs_id)
        return node['budget'] if node else 0

    return sum(calculate_rollup_budget(child['wbs_id']) for child in children)

def update_wbs_rollups():
    """Update all rollup calculations for parent nodes"""
    # Process from bottom to top (highest level first)
    max_level = max(node['level'] for node in st.session_state.wbs_structure)

    for level in range(max_level, -1, -1):
        nodes_at_level = [n for n in st.session_state.wbs_structure if n['level'] == level]
        for node in nodes_at_level:
            children = get_children(node['wbs_id'])
            if children:
                node['progress'] = calculate_rollup_progress(node['wbs_id'])
                node['actual_cost'] = calculate_rollup_cost(node['wbs_id'])

def find_critical_path():
    """Identify critical path through the WBS"""
    critical_tasks = []

    for node in st.session_state.wbs_structure:
        if node['type'] == 'task' and node['is_critical']:
            critical_tasks.append(node)

    # Sort by start date
    critical_tasks.sort(key=lambda x: x['start_date'])

    return critical_tasks

def calculate_schedule_variance(wbs_id):
    """Calculate schedule variance (Planned vs Actual)"""
    node = get_wbs_node(wbs_id)
    if not node:
        return 0

    today = datetime.now()
    planned_progress = 0

    if node['start_date'] <= today <= node['end_date']:
        days_elapsed = (today - node['start_date']).days
        planned_progress = (days_elapsed / node['duration']) * 100 if node['duration'] > 0 else 0
    elif today > node['end_date']:
        planned_progress = 100

    return node['progress'] - planned_progress

def calculate_cost_variance(wbs_id):
    """Calculate cost variance (Budget vs Actual)"""
    node = get_wbs_node(wbs_id)
    if not node:
        return 0

    planned_cost = (node['budget'] * node['progress']) / 100 if node['progress'] > 0 else 0
    return planned_cost - node['actual_cost']

# ============================================================================
# WBS VISUALIZATION FUNCTIONS
# ============================================================================

def render_wbs_tree():
    """Render interactive WBS tree view with expand/collapse"""

    st.subheader("📊 Work Breakdown Structure - Tree View")

    # Initialize expand state
    if 'wbs_expanded' not in st.session_state:
        st.session_state.wbs_expanded = {}

    def render_node(node, indent_level=0):
        """Recursively render WBS nodes"""

        # Create unique key for expansion state
        expand_key = f"expand_{node['wbs_id']}"
        if expand_key not in st.session_state.wbs_expanded:
            st.session_state.wbs_expanded[expand_key] = node['level'] <= 1  # Expand phases by default

        children = get_children(node['wbs_id'])
        has_children = len(children) > 0

        # Indent based on level
        indent = "&nbsp;" * (indent_level * 6)

        # Icon based on type and expansion
        if has_children:
            icon = "📂" if st.session_state.wbs_expanded[expand_key] else "📁"
        elif node['type'] == 'task':
            icon = "📋"
        else:
            icon = "⚡"

        # Status color
        status_colors = {
            'Completed': '🟢',
            'In Progress': '🟡',
            'Not Started': '⚪',
            'On Hold': '🔴'
        }
        status_icon = status_colors.get(node['status'], '⚪')

        # Milestone indicator
        milestone_icon = "🏁" if node.get('is_milestone', False) else ""

        # Critical path indicator
        critical_icon = "⚠️" if node.get('is_critical', False) else ""

        # Progress bar
        progress = node['progress']
        progress_bar = f"{'█' * int(progress/10)}{'░' * (10 - int(progress/10))}"

        # Create expandable section
        col1, col2, col3, col4, col5 = st.columns([0.5, 3, 1, 1, 1])

        with col1:
            if has_children:
                if st.button("➕" if not st.session_state.wbs_expanded[expand_key] else "➖",
                           key=f"btn_{node['wbs_id']}"):
                    st.session_state.wbs_expanded[expand_key] = not st.session_state.wbs_expanded[expand_key]
                    st.rerun()

        with col2:
            st.markdown(f"{indent}{icon} **{node['wbs_id']}**: {node['name']} {milestone_icon} {critical_icon}",
                       unsafe_allow_html=True)

        with col3:
            st.markdown(f"{status_icon} {node['status']}")

        with col4:
            st.markdown(f"`{progress_bar}` {progress:.0f}%")

        with col5:
            st.markdown(f"**{node['duration']}** days")

        # Show details
        with st.expander(f"Details - {node['wbs_id']}", expanded=False):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Budget", f"${node['budget']:,.0f}")
                st.metric("Actual Cost", f"${node['actual_cost']:,.0f}")
            with col_b:
                st.metric("Start Date", node['start_date'].strftime('%Y-%m-%d'))
                st.metric("End Date", node['end_date'].strftime('%Y-%m-%d'))
            with col_c:
                st.metric("Assigned To", node['assigned_to'])
                variance = calculate_schedule_variance(node['wbs_id'])
                st.metric("Schedule Variance", f"{variance:.1f}%", delta=f"{variance:.1f}%")

        # Render children if expanded
        if has_children and st.session_state.wbs_expanded[expand_key]:
            for child in children:
                render_node(child, indent_level + 1)

    # Get root nodes (projects)
    root_nodes = [n for n in st.session_state.wbs_structure if n['parent_id'] is None]

    # Render each root
    for root in root_nodes:
        render_node(root)
        st.divider()

def render_wbs_gantt():
    """Render WBS Gantt chart with dependencies and critical path"""

    st.subheader("📅 Work Breakdown Structure - Gantt Chart View")

    # Prepare data for Gantt chart
    tasks_for_gantt = []

    for node in st.session_state.wbs_structure:
        if node['type'] in ['phase', 'task']:  # Only show phases and tasks
            tasks_for_gantt.append({
                'Task': f"{node['wbs_id']}: {node['name']}",
                'Start': node['start_date'].strftime('%Y-%m-%d'),
                'Finish': node['end_date'].strftime('%Y-%m-%d'),
                'Progress': node['progress'],
                'Resource': node['assigned_to'],
                'Status': node['status'],
                'Critical': node.get('is_critical', False),
                'Milestone': node.get('is_milestone', False),
                'Level': node['level']
            })

    df_gantt = pd.DataFrame(tasks_for_gantt)

    # Create color mapping
    def get_task_color(row):
        if row['Milestone']:
            return 'purple'
        elif row['Critical']:
            return 'red'
        elif row['Status'] == 'Completed':
            return 'green'
        elif row['Status'] == 'In Progress':
            return 'orange'
        else:
            return 'lightblue'

    df_gantt['Color'] = df_gantt.apply(get_task_color, axis=1)

    # Create Gantt chart
    fig = go.Figure()

    # Add bars for each task
    for idx, row in df_gantt.iterrows():
        # Main task bar
        fig.add_trace(go.Bar(
            x=[pd.Timestamp(row['Finish']) - pd.Timestamp(row['Start'])],
            y=[row['Task']],
            base=[pd.Timestamp(row['Start'])],
            orientation='h',
            marker=dict(color=row['Color']),
            name=row['Status'],
            hovertemplate=f"<b>{row['Task']}</b><br>" +
                         f"Start: {row['Start']}<br>" +
                         f"Finish: {row['Finish']}<br>" +
                         f"Progress: {row['Progress']}%<br>" +
                         f"Resource: {row['Resource']}<br>" +
                         f"Status: {row['Status']}<extra></extra>",
            showlegend=False
        ))

        # Progress indicator
        if row['Progress'] > 0:
            duration = pd.Timestamp(row['Finish']) - pd.Timestamp(row['Start'])
            completed_duration = duration * (row['Progress'] / 100)

            fig.add_trace(go.Bar(
                x=[completed_duration],
                y=[row['Task']],
                base=[pd.Timestamp(row['Start'])],
                orientation='h',
                marker=dict(color='darkgreen', opacity=0.6),
                showlegend=False,
                hoverinfo='skip'
            ))

    # Add vertical line for today
    fig.add_vline(
        x=datetime.now().timestamp() * 1000,
        line_dash="dash",
        line_color="red",
        annotation_text="Today"
    )

    # Update layout
    fig.update_layout(
        title='WBS Gantt Chart - Project Timeline',
        xaxis_title='Timeline',
        yaxis_title='Tasks',
        height=max(600, len(df_gantt) * 30),
        barmode='overlay',
        xaxis=dict(type='date'),
        showlegend=False,
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Legend
    st.markdown("""
    **Legend:**
    - 🔴 Red: Critical Path Tasks
    - 🟢 Green: Completed Tasks
    - 🟠 Orange: In Progress Tasks
    - 🔵 Light Blue: Not Started Tasks
    - 🟣 Purple: Milestone Tasks
    - Dark Green Overlay: Progress Indicator
    """)

def render_wbs_performance_analytics():
    """Render performance analytics for WBS"""

    st.subheader("📈 Performance Analytics")

    # Calculate overall metrics
    total_budget = calculate_rollup_budget('WBS-1.0')
    total_actual_cost = calculate_rollup_cost('WBS-1.0')
    overall_progress = calculate_rollup_progress('WBS-1.0')

    cost_variance = total_budget - total_actual_cost
    cost_variance_pct = (cost_variance / total_budget * 100) if total_budget > 0 else 0

    schedule_variance = calculate_schedule_variance('WBS-1.0')

    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Overall Progress", f"{overall_progress:.1f}%",
                 delta=f"{overall_progress - 50:.1f}% vs target")

    with col2:
        st.metric("Total Budget", f"${total_budget:,.0f}")

    with col3:
        st.metric("Actual Cost", f"${total_actual_cost:,.0f}",
                 delta=f"${cost_variance:,.0f}")

    with col4:
        st.metric("Cost Variance", f"{cost_variance_pct:.1f}%",
                 delta="Under Budget" if cost_variance > 0 else "Over Budget")

    # Performance charts
    col_a, col_b = st.columns(2)

    with col_a:
        # Budget vs Actual by Phase
        phases = [n for n in st.session_state.wbs_structure if n['type'] == 'phase']

        phase_data = []
        for phase in phases:
            phase_data.append({
                'Phase': phase['name'],
                'Budget': phase['budget'],
                'Actual': phase['actual_cost'],
                'Variance': phase['budget'] - phase['actual_cost']
            })

        df_phases = pd.DataFrame(phase_data)

        fig_budget = go.Figure()
        fig_budget.add_trace(go.Bar(name='Budget', x=df_phases['Phase'], y=df_phases['Budget'],
                                    marker_color='lightblue'))
        fig_budget.add_trace(go.Bar(name='Actual', x=df_phases['Phase'], y=df_phases['Actual'],
                                    marker_color='darkblue'))

        fig_budget.update_layout(
            title='Budget vs Actual Cost by Phase',
            barmode='group',
            height=400
        )

        st.plotly_chart(fig_budget, use_container_width=True)

    with col_b:
        # Progress by Phase
        progress_data = []
        for phase in phases:
            progress_data.append({
                'Phase': phase['name'],
                'Progress': phase['progress']
            })

        df_progress = pd.DataFrame(progress_data)

        fig_progress = px.bar(df_progress, x='Phase', y='Progress',
                             title='Progress by Phase',
                             color='Progress',
                             color_continuous_scale='RdYlGn',
                             range_color=[0, 100])

        fig_progress.update_layout(height=400)

        st.plotly_chart(fig_progress, use_container_width=True)

    # Critical Path Analysis
    st.markdown("### 🎯 Critical Path Analysis")

    critical_tasks = find_critical_path()

    if critical_tasks:
        critical_df = pd.DataFrame([{
            'WBS ID': task['wbs_id'],
            'Task Name': task['name'],
            'Duration': f"{task['duration']} days",
            'Start': task['start_date'].strftime('%Y-%m-%d'),
            'End': task['end_date'].strftime('%Y-%m-%d'),
            'Status': task['status'],
            'Progress': f"{task['progress']}%",
            'Assigned To': task['assigned_to']
        } for task in critical_tasks])

        st.dataframe(critical_df, use_container_width=True)
    else:
        st.info("No critical path tasks identified.")

def render_baseline_comparison():
    """Render baseline comparison view"""

    st.subheader("📊 Baseline Comparison")

    if not st.session_state.wbs_baselines:
        st.warning("No baselines available for comparison.")
        return

    # Select baseline
    baseline_names = [b['name'] for b in st.session_state.wbs_baselines]
    selected_baseline = st.selectbox("Select Baseline", baseline_names)

    baseline = next((b for b in st.session_state.wbs_baselines if b['name'] == selected_baseline), None)

    if baseline:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Baseline Budget", f"${baseline['total_budget']:,.0f}")
            st.metric("Created Date", baseline['created_date'].strftime('%Y-%m-%d'))

        with col2:
            current_budget = calculate_rollup_budget('WBS-1.0')
            budget_variance = current_budget - baseline['total_budget']
            st.metric("Current Budget", f"${current_budget:,.0f}",
                     delta=f"${budget_variance:,.0f}")
            st.metric("Created By", baseline['created_by'])

        with col3:
            st.metric("Baseline Duration", f"{baseline['total_duration']} days")
            st.metric("Planned End", baseline['planned_end_date'].strftime('%Y-%m-%d'))

        st.markdown(f"**Description:** {baseline['description']}")

        # Variance analysis
        st.markdown("### Variance Analysis")

        col_a, col_b = st.columns(2)

        with col_a:
            schedule_var = calculate_schedule_variance('WBS-1.0')
            st.metric("Schedule Variance", f"{schedule_var:.1f}%",
                     delta="Ahead" if schedule_var > 0 else "Behind")

        with col_b:
            cost_var = calculate_cost_variance('WBS-1.0')
            st.metric("Cost Variance", f"${cost_var:,.0f}",
                     delta="Under Budget" if cost_var > 0 else "Over Budget")

# ============================================================================
# REPORT GENERATION FUNCTIONS
# ============================================================================

def render_test_report(test_result_id=None):
    """Generate Test Result Report"""

    st.subheader("🧪 Test Result Report")

    # Get test results from session state
    if 'test_results' not in st.session_state or not st.session_state.test_results:
        st.warning("No test results available. Generating sample data...")
        generate_sample_test_results()

    # Select test result
    if test_result_id:
        test_result = next((t for t in st.session_state.test_results if t['id'] == test_result_id), None)
    else:
        test_ids = [t['id'] for t in st.session_state.test_results]
        if test_ids:
            selected_id = st.selectbox("Select Test Result", test_ids)
            test_result = next((t for t in st.session_state.test_results if t['id'] == selected_id), None)
        else:
            st.error("No test results available.")
            return

    if not test_result:
        st.error("Test result not found.")
        return

    # Display report header
    st.markdown(f"### Test Report: {test_result['id']}")
    st.markdown(f"**Test Date:** {test_result['date']}")
    st.markdown(f"**Operator:** {test_result['operator']}")
    st.markdown(f"**Standard:** {test_result['standard']}")

    # Test details
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Test Method", test_result['method'])

    with col2:
        pass_fail = "✅ PASS" if test_result['pass_fail'] else "❌ FAIL"
        st.metric("Result", pass_fail)

    with col3:
        st.metric("Sample ID", test_result['sample_id'])

    # Test results data
    st.markdown("### Test Results")

    results_df = pd.DataFrame([test_result['results']])
    st.dataframe(results_df, use_container_width=True)

    # Visualization
    if test_result['method'] == 'I-V Curve Test':
        st.markdown("### I-V Curve Visualization")

        # Generate I-V curve data
        voltage = np.linspace(0, 40, 100)
        current = 9.5 * (1 - np.exp((voltage - 38) / 5))
        current = np.maximum(current, 0)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=voltage, y=current, mode='lines', name='I-V Curve',
                                line=dict(color='blue', width=2)))

        fig.update_layout(
            title='Current-Voltage Characteristic Curve',
            xaxis_title='Voltage (V)',
            yaxis_title='Current (A)',
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

    # Export options
    st.markdown("### Export Options")

    col_exp1, col_exp2, col_exp3 = st.columns(3)

    with col_exp1:
        if st.button("📄 Export to PDF"):
            pdf_data = generate_test_report_pdf(test_result)
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name=f"test_report_{test_result['id']}.pdf",
                mime="application/pdf"
            )

    with col_exp2:
        if st.button("📊 Export to Excel"):
            excel_data = generate_test_report_excel(test_result)
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"test_report_{test_result['id']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with col_exp3:
        if st.button("📋 Export to CSV"):
            csv_data = results_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"test_report_{test_result['id']}.csv",
                mime="text/csv"
            )

def generate_sample_test_results():
    """Generate sample test results data"""

    st.session_state.test_results = [
        {
            'id': 'TEST-001',
            'sample_id': 'SMP-001',
            'method': 'I-V Curve Test',
            'standard': 'IEC 61215',
            'operator': 'James Anderson',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'results': {
                'Voc (V)': 38.2,
                'Isc (A)': 9.45,
                'Vmp (V)': 31.5,
                'Imp (A)': 8.95,
                'Pmax (W)': 281.9,
                'Fill Factor': 0.78,
                'Efficiency (%)': 17.2
            },
            'pass_fail': True
        },
        {
            'id': 'TEST-002',
            'sample_id': 'SMP-002',
            'method': 'Thermal Cycling',
            'standard': 'IEC 61215',
            'operator': 'Lisa Thompson',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'results': {
                'Cycles Completed': 200,
                'Initial Power (W)': 285.0,
                'Final Power (W)': 280.3,
                'Power Degradation (%)': 1.65,
                'Visual Defects': 'None',
                'Insulation Resistance (MΩ)': 1250
            },
            'pass_fail': True
        },
        {
            'id': 'TEST-003',
            'sample_id': 'SMP-003',
            'method': 'Mechanical Load Test',
            'standard': 'IEC 61215',
            'operator': 'Kevin Brown',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'results': {
                'Load Applied (Pa)': 2400,
                'Duration (hours)': 1,
                'Deflection (mm)': 8.5,
                'Power Degradation (%)': 0.8,
                'Visual Defects': 'None',
                'Pass/Fail': 'Pass'
            },
            'pass_fail': True
        }
    ]

def render_equipment_performance_report():
    """Generate Equipment Performance Report"""

    st.subheader("🔧 Equipment Performance Report")

    # Get equipment from session state
    if 'equipment' not in st.session_state or not st.session_state.equipment:
        st.warning("No equipment data available.")
        return

    # Equipment selection
    equipment_ids = [eq['equipment_id'] for eq in st.session_state.equipment]
    selected_eq = st.selectbox("Select Equipment", equipment_ids)

    equipment = next((eq for eq in st.session_state.equipment if eq['equipment_id'] == selected_eq), None)

    if not equipment:
        st.error("Equipment not found.")
        return

    # Report header
    st.markdown(f"### Equipment Report: {equipment['name']}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Equipment ID", equipment['equipment_id'])
        st.metric("Type", equipment['type'])

    with col2:
        st.metric("Status", equipment['status'])
        st.metric("Location", equipment['location'])

    with col3:
        st.metric("Utilization", f"{equipment.get('utilization', 75)}%")
        st.metric("Last Calibration", equipment.get('last_calibration', 'N/A'))

    with col4:
        st.metric("Next Calibration", equipment.get('next_calibration', 'N/A'))
        st.metric("Downtime (hrs)", equipment.get('downtime_hours', 0))

    # Usage statistics
    st.markdown("### Usage Statistics")

    # Generate sample usage data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    usage_hours = np.random.randint(4, 10, size=30)

    usage_df = pd.DataFrame({
        'Date': dates,
        'Usage Hours': usage_hours
    })

    fig_usage = px.line(usage_df, x='Date', y='Usage Hours',
                       title='Daily Usage Hours (Last 30 Days)')

    st.plotly_chart(fig_usage, use_container_width=True)

    # Maintenance logs
    st.markdown("### Maintenance Log")

    maintenance_data = [
        {'Date': '2025-10-15', 'Type': 'Calibration', 'Technician': 'John Smith', 'Status': 'Completed'},
        {'Date': '2025-09-20', 'Type': 'Preventive', 'Technician': 'Jane Doe', 'Status': 'Completed'},
        {'Date': '2025-08-10', 'Type': 'Repair', 'Technician': 'Bob Wilson', 'Status': 'Completed'}
    ]

    maintenance_df = pd.DataFrame(maintenance_data)
    st.dataframe(maintenance_df, use_container_width=True)

    # Export button
    if st.button("📊 Export Equipment Report"):
        excel_data = generate_equipment_report_excel(equipment, usage_df, maintenance_df)
        st.download_button(
            label="Download Excel Report",
            data=excel_data,
            file_name=f"equipment_report_{equipment['equipment_id']}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def render_manpower_utilization_report():
    """Generate Manpower Utilization Report"""

    st.subheader("👥 Manpower Utilization Report")

    # Get manpower from session state
    if 'manpower' not in st.session_state or not st.session_state.manpower:
        st.warning("No manpower data available.")
        return

    # Calculate utilization metrics
    manpower_data = []

    for person in st.session_state.manpower:
        # Calculate assigned tasks
        assigned_tasks = [t for t in st.session_state.get('tasks', [])
                         if t.get('assigned_to') == person['name']]

        total_hours = sum(t.get('estimated_hours', 0) for t in assigned_tasks)
        completed_hours = sum(t.get('actual_hours', 0) for t in assigned_tasks
                             if t['status'] == 'Completed')

        utilization = (completed_hours / (person.get('available_hours', 160))) * 100 if person.get('available_hours', 160) > 0 else 0

        manpower_data.append({
            'Name': person['name'],
            'Role': person['role'],
            'Skills': ', '.join(person.get('skills', [])),
            'Assigned Tasks': len(assigned_tasks),
            'Total Hours': total_hours,
            'Completed Hours': completed_hours,
            'Utilization %': round(utilization, 1),
            'Performance Score': person.get('performance_score', 85)
        })

    df_manpower = pd.DataFrame(manpower_data)

    # Display summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Staff", len(df_manpower))

    with col2:
        avg_utilization = df_manpower['Utilization %'].mean()
        st.metric("Avg Utilization", f"{avg_utilization:.1f}%")

    with col3:
        avg_performance = df_manpower['Performance Score'].mean()
        st.metric("Avg Performance", f"{avg_performance:.1f}")

    with col4:
        total_tasks = df_manpower['Assigned Tasks'].sum()
        st.metric("Total Assigned Tasks", total_tasks)

    # Display table
    st.markdown("### Staff Utilization Details")
    st.dataframe(df_manpower, use_container_width=True)

    # Visualizations
    col_a, col_b = st.columns(2)

    with col_a:
        fig_util = px.bar(df_manpower, x='Name', y='Utilization %',
                         title='Staff Utilization Rate',
                         color='Utilization %',
                         color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_util, use_container_width=True)

    with col_b:
        fig_perf = px.bar(df_manpower, x='Name', y='Performance Score',
                         title='Performance Scores',
                         color='Performance Score',
                         color_continuous_scale='Viridis')
        st.plotly_chart(fig_perf, use_container_width=True)

    # Skills matrix
    st.markdown("### Skills Distribution")

    all_skills = []
    for person in st.session_state.manpower:
        all_skills.extend(person.get('skills', []))

    from collections import Counter
    skills_count = Counter(all_skills)

    skills_df = pd.DataFrame([
        {'Skill': skill, 'Count': count}
        for skill, count in skills_count.most_common()
    ])

    fig_skills = px.bar(skills_df, x='Skill', y='Count',
                       title='Team Skills Distribution')
    st.plotly_chart(fig_skills, use_container_width=True)

    # Export button
    if st.button("📊 Export Manpower Report"):
        excel_data = generate_manpower_report_excel(df_manpower, skills_df)
        st.download_button(
            label="Download Excel Report",
            data=excel_data,
            file_name=f"manpower_utilization_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

def render_project_status_report():
    """Generate Project Status Report with Gantt, progress, milestones, KPIs"""

    st.subheader("📊 Project Status Report")

    # Report date
    report_date = datetime.now()
    st.markdown(f"**Report Date:** {report_date.strftime('%Y-%m-%d %H:%M')}")

    # Executive Summary
    st.markdown("### Executive Summary")

    # Get project data
    project = get_wbs_node('WBS-1.0')

    if project:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Overall Progress", f"{project['progress']:.1f}%")

        with col2:
            schedule_var = calculate_schedule_variance('WBS-1.0')
            st.metric("Schedule Variance", f"{schedule_var:.1f}%",
                     delta="On Track" if abs(schedule_var) < 5 else "At Risk")

        with col3:
            cost_var = calculate_cost_variance('WBS-1.0')
            st.metric("Cost Variance", f"${cost_var:,.0f}",
                     delta="Under Budget" if cost_var > 0 else "Over Budget")

        with col4:
            completed_tasks = len([n for n in st.session_state.wbs_structure
                                  if n['type'] == 'task' and n['status'] == 'Completed'])
            total_tasks = len([n for n in st.session_state.wbs_structure if n['type'] == 'task'])
            st.metric("Tasks Completed", f"{completed_tasks}/{total_tasks}")

    # Phase Progress
    st.markdown("### Phase Progress")

    phases = [n for n in st.session_state.wbs_structure if n['type'] == 'phase']

    phase_progress = []
    for phase in phases:
        phase_progress.append({
            'Phase': phase['name'],
            'Progress': phase['progress'],
            'Status': phase['status'],
            'Budget': phase['budget'],
            'Actual Cost': phase['actual_cost']
        })

    df_phases = pd.DataFrame(phase_progress)
    st.dataframe(df_phases, use_container_width=True)

    # Gantt chart
    st.markdown("### Project Timeline (Gantt View)")
    render_wbs_gantt()

    # Milestones
    st.markdown("### Milestone Status")

    milestones = [n for n in st.session_state.wbs_structure if n.get('is_milestone', False)]

    milestone_data = []
    for milestone in milestones:
        milestone_data.append({
            'Milestone': milestone['name'],
            'WBS ID': milestone['wbs_id'],
            'Target Date': milestone['end_date'].strftime('%Y-%m-%d'),
            'Status': milestone['status'],
            'Progress': f"{milestone['progress']}%"
        })

    df_milestones = pd.DataFrame(milestone_data)
    st.dataframe(df_milestones, use_container_width=True)

    # Key Performance Indicators
    st.markdown("### Key Performance Indicators (KPIs)")

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

    with col_kpi1:
        st.markdown("**Schedule Performance Index (SPI)**")
        spi = (project['progress'] / 50) if project else 0  # 50% is planned progress
        st.metric("SPI", f"{spi:.2f}", delta="Good" if spi >= 0.95 else "At Risk")

    with col_kpi2:
        st.markdown("**Cost Performance Index (CPI)**")
        earned_value = (project['budget'] * project['progress'] / 100) if project else 0
        cpi = (earned_value / project['actual_cost']) if project and project['actual_cost'] > 0 else 0
        st.metric("CPI", f"{cpi:.2f}", delta="Good" if cpi >= 0.95 else "At Risk")

    with col_kpi3:
        st.markdown("**Critical Path Tasks On Track**")
        critical_tasks = find_critical_path()
        on_track = len([t for t in critical_tasks if t['status'] in ['Completed', 'In Progress']])
        total_critical = len(critical_tasks)
        st.metric("Critical Tasks", f"{on_track}/{total_critical}")

    # Export button
    if st.button("📄 Export Project Status Report"):
        pdf_data = generate_project_status_pdf(project, df_phases, df_milestones)
        st.download_button(
            label="Download PDF Report",
            data=pdf_data,
            file_name=f"project_status_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

def render_compliance_report():
    """Generate Compliance Report for IEC/ISO standards"""

    st.subheader("✅ Compliance Report")

    st.markdown("### IEC/ISO Standard Alignment")

    # Define compliance standards
    compliance_standards = [
        {
            'Standard': 'IEC 61215',
            'Description': 'Crystalline Silicon Terrestrial PV Modules - Design Qualification',
            'Status': 'Compliant',
            'Last Audit': '2025-10-01',
            'Next Audit': '2026-10-01',
            'Requirements Met': 28,
            'Total Requirements': 30,
            'Compliance %': 93.3
        },
        {
            'Standard': 'IEC 61730',
            'Description': 'PV Module Safety Qualification',
            'Status': 'Compliant',
            'Last Audit': '2025-09-15',
            'Next Audit': '2026-09-15',
            'Requirements Met': 22,
            'Total Requirements': 22,
            'Compliance %': 100.0
        },
        {
            'Standard': 'ISO 9001:2015',
            'Description': 'Quality Management Systems',
            'Status': 'Compliant',
            'Last Audit': '2025-08-20',
            'Next Audit': '2026-08-20',
            'Requirements Met': 45,
            'Total Requirements': 48,
            'Compliance %': 93.8
        },
        {
            'Standard': 'ISO 17025',
            'Description': 'Testing and Calibration Laboratories',
            'Status': 'Minor Non-Conformance',
            'Last Audit': '2025-07-10',
            'Next Audit': '2026-01-10',
            'Requirements Met': 38,
            'Total Requirements': 40,
            'Compliance %': 95.0
        }
    ]

    df_compliance = pd.DataFrame(compliance_standards)

    # Display compliance metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        compliant_count = len([s for s in compliance_standards if s['Status'] == 'Compliant'])
        st.metric("Compliant Standards", f"{compliant_count}/{len(compliance_standards)}")

    with col2:
        avg_compliance = df_compliance['Compliance %'].mean()
        st.metric("Avg Compliance", f"{avg_compliance:.1f}%")

    with col3:
        total_requirements = df_compliance['Total Requirements'].sum()
        met_requirements = df_compliance['Requirements Met'].sum()
        st.metric("Requirements Met", f"{met_requirements}/{total_requirements}")

    with col4:
        non_conformances = len([s for s in compliance_standards if s['Status'] != 'Compliant'])
        st.metric("Non-Conformances", non_conformances)

    # Compliance table
    st.markdown("### Compliance Status by Standard")
    st.dataframe(df_compliance, use_container_width=True)

    # Compliance visualization
    fig_compliance = go.Figure()

    fig_compliance.add_trace(go.Bar(
        name='Requirements Met',
        x=df_compliance['Standard'],
        y=df_compliance['Requirements Met'],
        marker_color='green'
    ))

    fig_compliance.add_trace(go.Bar(
        name='Requirements Not Met',
        x=df_compliance['Standard'],
        y=df_compliance['Total Requirements'] - df_compliance['Requirements Met'],
        marker_color='red'
    ))

    fig_compliance.update_layout(
        title='Compliance Requirements Status',
        barmode='stack',
        height=400
    )

    st.plotly_chart(fig_compliance, use_container_width=True)

    # Certification checks
    st.markdown("### Certification Status")

    certifications = [
        {'Certificate': 'UL 1703', 'Status': 'Valid', 'Expiry': '2026-12-31', 'Issuer': 'UL LLC'},
        {'Certificate': 'CE Mark', 'Status': 'Valid', 'Expiry': '2027-06-30', 'Issuer': 'TÜV Rheinland'},
        {'Certificate': 'IEC CB Scheme', 'Status': 'Valid', 'Expiry': '2026-09-15', 'Issuer': 'IECEE'},
        {'Certificate': 'CEC Listed', 'Status': 'Valid', 'Expiry': '2027-03-31', 'Issuer': 'California Energy Commission'}
    ]

    df_certs = pd.DataFrame(certifications)
    st.dataframe(df_certs, use_container_width=True)

    # Audit trail summary
    st.markdown("### Audit Trail Summary")

    if 'audit_trail' in st.session_state and st.session_state.audit_trail:
        recent_audits = st.session_state.audit_trail[-10:]
        audit_df = pd.DataFrame(recent_audits)
        st.dataframe(audit_df, use_container_width=True)
    else:
        st.info("No audit trail data available.")

    # Export button
    if st.button("📄 Export Compliance Report"):
        pdf_data = generate_compliance_report_pdf(df_compliance, df_certs)
        st.download_button(
            label="Download PDF Report",
            data=pdf_data,
            file_name=f"compliance_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf"
        )

def render_report_builder_ui():
    """Dynamic report builder with filters and date ranges"""

    st.subheader("🛠️ Custom Report Builder")

    # Report type selection
    report_types = [
        "Test Results Summary",
        "Equipment Utilization",
        "Manpower Analysis",
        "Project Performance",
        "Compliance Summary",
        "Custom Query"
    ]

    selected_report = st.selectbox("Select Report Type", report_types)

    # Date range filter
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))

    with col2:
        end_date = st.date_input("End Date", datetime.now())

    # Additional filters
    st.markdown("### Filters")

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        # Project filter
        if 'projects' in st.session_state and st.session_state.projects:
            project_options = ['All'] + [p['id'] for p in st.session_state.projects]
            selected_project = st.selectbox("Project", project_options)

    with col_b:
        # Status filter
        status_options = ['All', 'Completed', 'In Progress', 'Not Started']
        selected_status = st.selectbox("Status", status_options)

    with col_c:
        # Resource filter
        if 'manpower' in st.session_state and st.session_state.manpower:
            resource_options = ['All'] + [p['name'] for p in st.session_state.manpower]
            selected_resource = st.selectbox("Resource", resource_options)

    # Report configuration
    st.markdown("### Report Configuration")

    col_conf1, col_conf2 = st.columns(2)

    with col_conf1:
        include_charts = st.checkbox("Include Charts", value=True)
        include_summary = st.checkbox("Include Executive Summary", value=True)

    with col_conf2:
        include_details = st.checkbox("Include Detailed Data", value=True)
        include_recommendations = st.checkbox("Include Recommendations", value=False)

    # Export format selection
    st.markdown("### Export Format")

    export_format = st.radio("Select Format", ["PDF", "Excel", "CSV", "JSON"], horizontal=True)

    # Generate report button
    if st.button("🔄 Generate Report", type="primary"):
        with st.spinner("Generating report..."):
            # Simulate report generation
            import time
            time.sleep(1)

            st.success("Report generated successfully!")

            # Display preview
            st.markdown("### Report Preview")

            if selected_report == "Test Results Summary":
                if 'test_results' in st.session_state and st.session_state.test_results:
                    df_preview = pd.DataFrame(st.session_state.test_results)
                    st.dataframe(df_preview, use_container_width=True)
                else:
                    st.info("No test results available.")

            elif selected_report == "Equipment Utilization":
                if 'equipment' in st.session_state and st.session_state.equipment:
                    df_preview = pd.DataFrame(st.session_state.equipment)
                    st.dataframe(df_preview, use_container_width=True)
                else:
                    st.info("No equipment data available.")

            elif selected_report == "Project Performance":
                # Show WBS summary
                phases = [n for n in st.session_state.wbs_structure if n['type'] == 'phase']
                df_preview = pd.DataFrame([{
                    'Phase': p['name'],
                    'Progress': f"{p['progress']}%",
                    'Status': p['status'],
                    'Budget': f"${p['budget']:,.0f}",
                    'Actual Cost': f"${p['actual_cost']:,.0f}"
                } for p in phases])
                st.dataframe(df_preview, use_container_width=True)

            # Download button
            if export_format == "PDF":
                st.download_button(
                    label="📥 Download Report (PDF)",
                    data=b"Sample PDF report content",
                    file_name=f"custom_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            elif export_format == "Excel":
                st.download_button(
                    label="📥 Download Report (Excel)",
                    data=b"Sample Excel report content",
                    file_name=f"custom_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            elif export_format == "CSV":
                st.download_button(
                    label="📥 Download Report (CSV)",
                    data="Sample CSV report content",
                    file_name=f"custom_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:  # JSON
                st.download_button(
                    label="📥 Download Report (JSON)",
                    data='{"report": "Sample JSON report content"}',
                    file_name=f"custom_report_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================

def generate_test_report_pdf(test_result):
    """Generate PDF for test result report"""

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#003366'),
        alignment=TA_CENTER
    )

    elements.append(Paragraph("Test Result Report", title_style))
    elements.append(Spacer(1, 0.3*inch))

    # Test information
    info_data = [
        ['Test ID:', test_result['id']],
        ['Sample ID:', test_result['sample_id']],
        ['Test Method:', test_result['method']],
        ['Standard:', test_result['standard']],
        ['Operator:', test_result['operator']],
        ['Date:', test_result['date']],
        ['Result:', 'PASS' if test_result['pass_fail'] else 'FAIL']
    ]

    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))

    # Test results
    elements.append(Paragraph("Test Results", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))

    results_data = [['Parameter', 'Value']]
    for key, value in test_result['results'].items():
        results_data.append([key, str(value)])

    results_table = Table(results_data, colWidths=[3*inch, 3*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))

    elements.append(results_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def generate_test_report_excel(test_result):
    """Generate Excel for test result report"""

    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Test info sheet
        info_df = pd.DataFrame([{
            'Test ID': test_result['id'],
            'Sample ID': test_result['sample_id'],
            'Method': test_result['method'],
            'Standard': test_result['standard'],
            'Operator': test_result['operator'],
            'Date': test_result['date'],
            'Pass/Fail': 'PASS' if test_result['pass_fail'] else 'FAIL'
        }])

        info_df.to_excel(writer, sheet_name='Test Information', index=False)

        # Results sheet
        results_df = pd.DataFrame([test_result['results']])
        results_df.to_excel(writer, sheet_name='Test Results', index=False)

    output.seek(0)
    return output.getvalue()

def generate_equipment_report_excel(equipment, usage_df, maintenance_df):
    """Generate Excel for equipment report"""

    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Equipment info
        info_df = pd.DataFrame([equipment])
        info_df.to_excel(writer, sheet_name='Equipment Info', index=False)

        # Usage statistics
        usage_df.to_excel(writer, sheet_name='Usage Statistics', index=False)

        # Maintenance log
        maintenance_df.to_excel(writer, sheet_name='Maintenance Log', index=False)

    output.seek(0)
    return output.getvalue()

def generate_manpower_report_excel(manpower_df, skills_df):
    """Generate Excel for manpower report"""

    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        manpower_df.to_excel(writer, sheet_name='Utilization', index=False)
        skills_df.to_excel(writer, sheet_name='Skills Distribution', index=False)

    output.seek(0)
    return output.getvalue()

def generate_project_status_pdf(project, phases_df, milestones_df):
    """Generate PDF for project status report"""

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Project Status Report", styles['Title']))
    elements.append(Spacer(1, 0.3*inch))

    # Project summary
    if project:
        summary_data = [
            ['Project:', project['name']],
            ['Progress:', f"{project['progress']:.1f}%"],
            ['Status:', project['status']],
            ['Budget:', f"${project['budget']:,.0f}"],
            ['Actual Cost:', f"${project['actual_cost']:,.0f}"]
        ]

        summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))

    # Phase progress
    elements.append(Paragraph("Phase Progress", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))

    # Convert dataframe to table data
    phase_table_data = [phases_df.columns.tolist()] + phases_df.values.tolist()
    phase_table = Table(phase_table_data)
    phase_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(phase_table)
    elements.append(PageBreak())

    # Milestones
    elements.append(Paragraph("Milestones", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))

    milestone_table_data = [milestones_df.columns.tolist()] + milestones_df.values.tolist()
    milestone_table = Table(milestone_table_data)
    milestone_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(milestone_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

def generate_compliance_report_pdf(compliance_df, certs_df):
    """Generate PDF for compliance report"""

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("Compliance Report", styles['Title']))
    elements.append(Spacer(1, 0.3*inch))

    # Compliance standards
    elements.append(Paragraph("Standard Compliance Status", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))

    compliance_table_data = [compliance_df.columns.tolist()] + compliance_df.values.tolist()
    compliance_table = Table(compliance_table_data)
    compliance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(compliance_table)
    elements.append(PageBreak())

    # Certifications
    elements.append(Paragraph("Certifications", styles['Heading2']))
    elements.append(Spacer(1, 0.1*inch))

    certs_table_data = [certs_df.columns.tolist()] + certs_df.values.tolist()
    certs_table = Table(certs_table_data)
    certs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(certs_table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# ============================================================================
# MAIN RENDER FUNCTION
# ============================================================================

def render_reports_wbs_module():
    """Main function to render the Reports & WBS module"""

    # Initialize data
    init_reports_wbs_data()

    st.title("📊 Reports & Work Breakdown Structure")

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Reports",
        "🏗️ WBS Structure",
        "📊 Performance Analytics",
        "🛠️ Report Builder"
    ])

    with tab1:
        st.header("Solar-Specific Reports")

        report_type = st.selectbox(
            "Select Report Type",
            [
                "Test Result Report",
                "Equipment Performance Report",
                "Manpower Utilization Report",
                "Project Status Report",
                "Compliance Report"
            ]
        )

        if report_type == "Test Result Report":
            render_test_report()
        elif report_type == "Equipment Performance Report":
            render_equipment_performance_report()
        elif report_type == "Manpower Utilization Report":
            render_manpower_utilization_report()
        elif report_type == "Project Status Report":
            render_project_status_report()
        elif report_type == "Compliance Report":
            render_compliance_report()

    with tab2:
        st.header("Work Breakdown Structure")

        wbs_view = st.radio("View Type", ["Tree View", "Gantt Chart", "Both"], horizontal=True)

        if wbs_view in ["Tree View", "Both"]:
            render_wbs_tree()

        if wbs_view in ["Gantt Chart", "Both"]:
            st.divider()
            render_wbs_gantt()

        # Baseline comparison
        with st.expander("📊 Baseline Comparison", expanded=False):
            render_baseline_comparison()

    with tab3:
        st.header("Performance Analytics")
        render_wbs_performance_analytics()

    with tab4:
        st.header("Custom Report Builder")
        render_report_builder_ui()

# ============================================================================
# STANDALONE EXECUTION (for testing)
# ============================================================================

if __name__ == "__main__":
    render_reports_wbs_module()
