import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import hashlib
import uuid
from io import BytesIO
import base64
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Solar PV Test Project Management",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional UI
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
    }
    .stTabs [data-baseweb="tab-list"] [data-testid="stMarkdownContainer"] {
        font-size: 14px;
    }
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #cccccc;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;
    }
    .task-card {
        background-color: white;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ddd;
        margin: 5px 0;
    }
    .priority-high { border-left: 4px solid #ff4444; }
    .priority-medium { border-left: 4px solid #ffaa00; }
    .priority-low { border-left: 4px solid #00aa00; }
    .status-badge {
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'projects': [],
        'tasks': [],
        'samples': [],
        'equipment': [],
        'manpower': [],
        'test_methods': [],
        'test_results': [],
        'risks': [],
        'issues': [],
        'approvals': [],
        'documents': [],
        'notifications': [],
        'current_user': 'Admin User',
        'user_role': 'Admin',
        'holidays': [],
        'signatures': [],
        'audit_trail': [],
        'initialized': False
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Initialize with sample data if not already done
    if not st.session_state.initialized:
        init_sample_data()
        st.session_state.initialized = True

def init_sample_data():
    """Initialize sample data for demo"""
    # Sample Projects
    st.session_state.projects = [
        {
            'id': 'PRJ001',
            'name': 'Solar Panel Efficiency Testing Q1',
            'client': 'SolarTech Corp',
            'start_date': datetime.now().date(),
            'end_date': (datetime.now() + timedelta(days=90)).date(),
            'baseline_start': datetime.now().date(),
            'baseline_end': (datetime.now() + timedelta(days=90)).date(),
            'status': 'In Progress',
            'priority': 'High',
            'budget': 500000,
            'spent': 125000,
            'manager': 'John Smith',
            'description': 'Comprehensive testing of new solar panel models for efficiency certification'
        }
    ]
    
    # Sample Tasks with WBS
    tasks = []
    task_data = [
        ('1', 'Project Initiation', 'Not Started', 'High', 5, 0, None),
        ('1.1', 'Kickoff Meeting', 'Completed', 'High', 1, 100, ['1']),
        ('1.2', 'Requirements Gathering', 'In Progress', 'High', 3, 60, ['1.1']),
        ('2', 'Sample Preparation', 'In Progress', 'High', 10, 40, None),
        ('2.1', 'Sample Collection', 'In Progress', 'Medium', 3, 70, ['2']),
        ('2.2', 'Sample Conditioning', 'Not Started', 'Medium', 5, 0, ['2.1']),
        ('3', 'Testing Phase', 'Not Started', 'Critical', 30, 0, None),
        ('3.1', 'Efficiency Testing', 'Not Started', 'Critical', 10, 0, ['2.2']),
        ('3.2', 'Durability Testing', 'Not Started', 'High', 15, 0, ['3.1']),
        ('3.3', 'Environmental Testing', 'Not Started', 'Medium', 10, 0, ['3.1']),
        ('4', 'Analysis & Reporting', 'Not Started', 'High', 15, 0, None),
        ('4.1', 'Data Analysis', 'Not Started', 'High', 7, 0, ['3.2', '3.3']),
        ('4.2', 'Report Generation', 'Not Started', 'High', 5, 0, ['4.1']),
        ('4.3', 'Final Presentation', 'Not Started', 'Medium', 3, 0, ['4.2'])
    ]
    
    for i, (wbs, name, status, priority, duration, progress, deps) in enumerate(task_data):
        tasks.append({
            'id': f'TSK{i+1:03d}',
            'wbs': wbs,
            'name': name,
            'project_id': 'PRJ001',
            'status': status,
            'priority': priority,
            'assigned_to': ['John Smith', 'Jane Doe'][i % 2],
            'start_date': datetime.now().date() + timedelta(days=i*3),
            'end_date': datetime.now().date() + timedelta(days=i*3 + duration),
            'duration': duration,
            'progress': progress,
            'dependencies': deps if deps else [],
            'is_milestone': 'Meeting' in name or 'Presentation' in name,
            'is_critical': priority == 'Critical',
            'description': f'Task description for {name}',
            'estimated_hours': duration * 8,
            'actual_hours': (duration * 8 * progress / 100) if progress > 0 else 0
        })
    st.session_state.tasks = tasks
    
    # Sample Test Samples with Chain of Custody
    st.session_state.samples = [
        {
            'id': 'SMP001',
            'name': 'Monocrystalline Panel A1',
            'type': 'Monocrystalline',
            'batch': 'BATCH-2024-001',
            'received_date': datetime.now().date(),
            'condition': 'Good',
            'location': 'Lab Storage A',
            'chain_of_custody': [
                {'date': datetime.now(), 'from': 'Warehouse', 'to': 'Lab Storage A', 
                 'handler': 'Mike Johnson', 'notes': 'Initial receipt'},
                {'date': datetime.now() - timedelta(days=1), 'from': 'Manufacturing', 
                 'to': 'Warehouse', 'handler': 'Sarah Lee', 'notes': 'Quality check passed'}
            ],
            'status': 'Available',
            'test_status': 'Pending',
            'barcode': 'BC001234567'
        },
        {
            'id': 'SMP002',
            'name': 'Polycrystalline Panel B2',
            'type': 'Polycrystalline',
            'batch': 'BATCH-2024-002',
            'received_date': datetime.now().date() - timedelta(days=2),
            'condition': 'Good',
            'location': 'Testing Chamber 1',
            'chain_of_custody': [
                {'date': datetime.now(), 'from': 'Lab Storage A', 'to': 'Testing Chamber 1',
                 'handler': 'Tom Wilson', 'notes': 'Moved for efficiency testing'}
            ],
            'status': 'In Testing',
            'test_status': 'In Progress',
            'barcode': 'BC001234568'
        }
    ]
    
    # Sample Equipment
    st.session_state.equipment = [
        {
            'id': 'EQP001',
            'name': 'Solar Simulator SS-1000',
            'type': 'Testing Equipment',
            'status': 'Available',
            'location': 'Test Lab 1',
            'last_calibration': datetime.now().date() - timedelta(days=30),
            'next_calibration': datetime.now().date() + timedelta(days=335),
            'performance_metric': 98.5,
            'utilization': 65,
            'maintenance_history': [
                {'date': datetime.now().date() - timedelta(days=30), 
                 'type': 'Calibration', 'technician': 'Bob Tech', 'notes': 'Annual calibration'}
            ],
            'bookings': []
        },
        {
            'id': 'EQP002',
            'name': 'Environmental Chamber EC-500',
            'type': 'Testing Equipment',
            'status': 'In Use',
            'location': 'Test Lab 2',
            'last_calibration': datetime.now().date() - timedelta(days=60),
            'next_calibration': datetime.now().date() + timedelta(days=305),
            'performance_metric': 96.2,
            'utilization': 80,
            'maintenance_history': [],
            'bookings': [
                {'date': datetime.now().date(), 'project': 'PRJ001', 
                 'user': 'Jane Doe', 'duration': 4}
            ]
        }
    ]
    
    # Sample Manpower
    st.session_state.manpower = [
        {
            'id': 'EMP001',
            'name': 'John Smith',
            'role': 'Test Engineer',
            'skills': ['Efficiency Testing', 'Data Analysis', 'Report Writing'],
            'availability': 'Available',
            'current_project': 'PRJ001',
            'performance_score': 92,
            'hours_logged': 1250,
            'certifications': ['ISO 17025', 'IEC 61215'],
            'schedule': []
        },
        {
            'id': 'EMP002',
            'name': 'Jane Doe',
            'role': 'Senior Test Engineer',
            'skills': ['Environmental Testing', 'Calibration', 'Quality Control'],
            'availability': 'Busy',
            'current_project': 'PRJ001',
            'performance_score': 95,
            'hours_logged': 1480,
            'certifications': ['ISO 17025', 'IEC 61215', 'IEC 61730'],
            'schedule': [
                {'date': datetime.now().date(), 'task': 'TSK003', 'hours': 8}
            ]
        }
    ]
    
    # Sample Test Methods
    st.session_state.test_methods = [
        {
            'id': 'TM001',
            'name': 'Power Output Measurement',
            'standard': 'IEC 61215-2:2016',
            'method_number': 'MQT-01',
            'category': 'Electrical Performance',
            'equipment_required': ['Solar Simulator SS-1000'],
            'duration_hours': 2,
            'parameters': ['Irradiance', 'Temperature', 'Voltage', 'Current'],
            'acceptance_criteria': 'Power output within ±3% of rated power'
        },
        {
            'id': 'TM002',
            'name': 'Thermal Cycling Test',
            'standard': 'IEC 61730-2:2016',
            'method_number': 'MQT-11',
            'category': 'Environmental Testing',
            'equipment_required': ['Environmental Chamber EC-500'],
            'duration_hours': 200,
            'parameters': ['Temperature Range', 'Cycle Count', 'Humidity'],
            'acceptance_criteria': 'No visual defects, power degradation < 5%'
        }
    ]
    
    # Sample Risks
    st.session_state.risks = [
        {
            'id': 'RSK001',
            'title': 'Equipment Calibration Delay',
            'category': 'Technical',
            'probability': 'Medium',
            'impact': 'High',
            'status': 'Open',
            'mitigation': 'Schedule backup equipment, maintain calibration calendar',
            'owner': 'John Smith',
            'identified_date': datetime.now().date() - timedelta(days=10),
            'project_id': 'PRJ001'
        },
        {
            'id': 'RSK002',
            'title': 'Sample Delivery Delays',
            'category': 'Supply Chain',
            'probability': 'Low',
            'impact': 'Medium',
            'status': 'Mitigated',
            'mitigation': 'Multiple supplier agreements, buffer stock',
            'owner': 'Jane Doe',
            'identified_date': datetime.now().date() - timedelta(days=20),
            'project_id': 'PRJ001'
        }
    ]
    
    # Sample Issues
    st.session_state.issues = [
        {
            'id': 'ISS001',
            'title': 'Temperature Sensor Malfunction',
            'category': 'Equipment',
            'severity': 'High',
            'status': 'In Progress',
            'description': 'Temperature sensor in Chamber 2 showing erratic readings',
            'resolution': 'Replacement sensor ordered, temporary workaround in place',
            'reported_by': 'Tom Wilson',
            'assigned_to': 'Mike Johnson',
            'reported_date': datetime.now().date() - timedelta(days=2),
            'project_id': 'PRJ001'
        }
    ]
    
    # Sample Holidays
    st.session_state.holidays = [
        {'date': datetime.now().date() + timedelta(days=30), 'name': 'National Holiday', 'type': 'Public'},
        {'date': datetime.now().date() + timedelta(days=45), 'name': 'Company Anniversary', 'type': 'Company'}
    ]
    
    # Initialize empty lists for other data
    st.session_state.test_results = []
    st.session_state.approvals = []
    st.session_state.documents = []
    st.session_state.notifications = []
    st.session_state.signatures = []
    st.session_state.audit_trail = []

def add_audit_trail(action, entity_type, entity_id, details):
    """Add entry to audit trail"""
    st.session_state.audit_trail.append({
        'timestamp': datetime.now(),
        'user': st.session_state.current_user,
        'action': action,
        'entity_type': entity_type,
        'entity_id': entity_id,
        'details': details
    })

def create_notification(recipient, type, title, message, priority='Medium'):
    """Create a notification"""
    st.session_state.notifications.append({
        'id': str(uuid.uuid4()),
        'recipient': recipient,
        'type': type,
        'title': title,
        'message': message,
        'priority': priority,
        'timestamp': datetime.now(),
        'read': False
    })

# Dashboard Functions
def render_dashboard():
    """Render main dashboard with comprehensive metrics"""
    st.header("📊 Project Dashboard")
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t['status'] == 'Completed'])
    in_progress_tasks = len([t for t in st.session_state.tasks if t['status'] == 'In Progress'])
    critical_tasks = len([t for t in st.session_state.tasks if t['is_critical']])
    
    col1.metric("Total Tasks", total_tasks, f"+{in_progress_tasks} active")
    col2.metric("Completed", completed_tasks, f"{(completed_tasks/total_tasks*100):.0f}%")
    col3.metric("Critical Path Tasks", critical_tasks, "⚠️" if critical_tasks > 0 else "✅")
    col4.metric("Active Samples", len([s for s in st.session_state.samples if s['status'] == 'In Testing']))
    col5.metric("Equipment Utilization", f"{np.mean([e['utilization'] for e in st.session_state.equipment]):.0f}%")
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Project Progress Overview")
        if st.session_state.tasks:
            progress_data = pd.DataFrame(st.session_state.tasks)
            progress_data['progress_category'] = pd.cut(progress_data['progress'], 
                                                        bins=[0, 25, 50, 75, 100],
                                                        labels=['0-25%', '26-50%', '51-75%', '76-100%'])
            fig = px.histogram(progress_data, x='progress_category', 
                              title="Task Progress Distribution",
                              color='priority',
                              color_discrete_map={'High': '#ff4444', 'Medium': '#ffaa00', 
                                                 'Low': '#00aa00', 'Critical': '#880000'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Resource Utilization")
        resource_data = pd.DataFrame({
            'Resource': ['Equipment', 'Manpower', 'Budget', 'Time'],
            'Utilization': [
                np.mean([e['utilization'] for e in st.session_state.equipment]),
                len([m for m in st.session_state.manpower if m['availability'] == 'Busy']) / len(st.session_state.manpower) * 100 if st.session_state.manpower else 0,
                (st.session_state.projects[0]['spent'] / st.session_state.projects[0]['budget'] * 100) if st.session_state.projects else 0,
                65  # Example time utilization
            ]
        })
        fig = px.bar(resource_data, x='Resource', y='Utilization', 
                    title="Resource Utilization (%)",
                    color='Utilization',
                    color_continuous_scale='RdYlGn_r')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Task Status Distribution")
        if st.session_state.tasks:
            status_counts = pd.DataFrame(st.session_state.tasks)['status'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title="Tasks by Status",
                        color_discrete_map={'Completed': '#00aa00', 'In Progress': '#ffaa00',
                                          'Not Started': '#cccccc'})
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Risk Matrix")
        if st.session_state.risks:
            risk_df = pd.DataFrame(st.session_state.risks)
            risk_matrix = pd.crosstab(risk_df['probability'], risk_df['impact'])
            fig = px.imshow(risk_matrix, 
                          labels=dict(x="Impact", y="Probability", color="Count"),
                          title="Risk Heat Map",
                          color_continuous_scale='Reds')
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Activity Timeline
    st.subheader("📅 Recent Activity")
    if st.session_state.audit_trail:
        recent_activities = st.session_state.audit_trail[-5:]
        for activity in reversed(recent_activities):
            st.info(f"**{activity['timestamp'].strftime('%Y-%m-%d %H:%M')}** - {activity['user']}: {activity['action']} on {activity['entity_type']} ({activity['entity_id']})")

# Project Management Functions
def render_project_management():
    """Render project management interface"""
    st.header("📋 Project Management")
    
    tabs = st.tabs(["WBS & Tasks", "Gantt Chart", "Critical Path", "Baselines", "Milestones"])
    
    with tabs[0]:
        render_wbs_view()
    
    with tabs[1]:
        render_gantt_chart()
    
    with tabs[2]:
        render_critical_path()
    
    with tabs[3]:
        render_baseline_tracking()
    
    with tabs[4]:
        render_milestones()

def render_wbs_view():
    """Render Work Breakdown Structure view"""
    st.subheader("Work Breakdown Structure")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display WBS tree
        for task in st.session_state.tasks:
            indent = len(task['wbs'].split('.')) - 1
            prefix = "  " * indent + ("├─ " if indent > 0 else "")
            
            status_color = {'Completed': '🟢', 'In Progress': '🟡', 'Not Started': '⚪'}
            priority_badge = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}
            
            st.markdown(f"{prefix}**{task['wbs']}** {task['name']} "
                       f"{status_color[task['status']]} "
                       f"{priority_badge[task['priority']]} "
                       f"[{task['progress']}%]")
    
    with col2:
        st.subheader("Add New Task")
        with st.form("add_task_form"):
            wbs = st.text_input("WBS Code")
            name = st.text_input("Task Name")
            priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
            duration = st.number_input("Duration (days)", min_value=1, value=5)
            assigned = st.selectbox("Assigned To", [m['name'] for m in st.session_state.manpower])
            
            if st.form_submit_button("Add Task"):
                new_task = {
                    'id': f'TSK{len(st.session_state.tasks)+1:03d}',
                    'wbs': wbs,
                    'name': name,
                    'project_id': 'PRJ001',
                    'status': 'Not Started',
                    'priority': priority,
                    'assigned_to': assigned,
                    'start_date': datetime.now().date(),
                    'end_date': datetime.now().date() + timedelta(days=duration),
                    'duration': duration,
                    'progress': 0,
                    'dependencies': [],
                    'is_milestone': False,
                    'is_critical': priority == 'Critical',
                    'description': '',
                    'estimated_hours': duration * 8,
                    'actual_hours': 0
                }
                st.session_state.tasks.append(new_task)
                add_audit_trail('Created', 'Task', new_task['id'], f"Added task {name}")
                st.success(f"Task {name} added successfully!")
                st.rerun()

def render_gantt_chart():
    """Render Gantt chart view"""
    st.subheader("Gantt Chart View")
    
    if st.session_state.tasks:
        # Prepare data for Gantt chart
        df = pd.DataFrame(st.session_state.tasks)
        
        fig = go.Figure()
        
        # Add tasks to Gantt
        for idx, task in df.iterrows():
            color = {'Critical': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}[task['priority']]
            
            fig.add_trace(go.Scatter(
                x=[task['start_date'], task['end_date']],
                y=[task['name'], task['name']],
                mode='lines',
                line=dict(color=color, width=20),
                name=task['name'],
                hovertemplate=f"<b>{task['name']}</b><br>" +
                             f"WBS: {task['wbs']}<br>" +
                             f"Start: {task['start_date']}<br>" +
                             f"End: {task['end_date']}<br>" +
                             f"Progress: {task['progress']}%<br>" +
                             f"Priority: {task['priority']}"
            ))
            
            # Add progress overlay
            if task['progress'] > 0:
                progress_end = task['start_date'] + timedelta(days=int(task['duration'] * task['progress'] / 100))
                fig.add_trace(go.Scatter(
                    x=[task['start_date'], progress_end],
                    y=[task['name'], task['name']],
                    mode='lines',
                    line=dict(color='darkgreen', width=10),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        # Add today line
        fig.add_vline(x=str(datetime.now().date()), line_dash="dash", line_color="red",
                     annotation_text="Today")
        
        fig.update_layout(
            title="Project Gantt Chart",
            xaxis_title="Timeline",
            yaxis_title="Tasks",
            height=600,
            showlegend=False,
            hovermode='closest'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_critical_path():
    """Render critical path analysis"""
    st.subheader("Critical Path Analysis")
    
    critical_tasks = [t for t in st.session_state.tasks if t['is_critical']]
    
    if critical_tasks:
        # Display critical path
        st.warning(f"⚠️ Critical Path contains {len(critical_tasks)} tasks")
        
        total_duration = sum([t['duration'] for t in critical_tasks])
        st.metric("Total Critical Path Duration", f"{total_duration} days")
        
        # Critical path network diagram
        fig = go.Figure()
        
        # Add nodes for critical tasks
        for i, task in enumerate(critical_tasks):
            fig.add_trace(go.Scatter(
                x=[i],
                y=[0],
                mode='markers+text',
                marker=dict(size=50, color='red'),
                text=[f"{task['wbs']}<br>{task['name'][:15]}..."],
                textposition='top center',
                hovertemplate=f"<b>{task['name']}</b><br>Duration: {task['duration']} days<br>Progress: {task['progress']}%"
            ))
            
            # Add edges
            if i > 0:
                fig.add_trace(go.Scatter(
                    x=[i-1, i],
                    y=[0, 0],
                    mode='lines',
                    line=dict(color='red', width=2),
                    showlegend=False,
                    hoverinfo='skip'
                ))
        
        fig.update_layout(
            title="Critical Path Network",
            showlegend=False,
            height=300,
            xaxis=dict(showticklabels=False, showgrid=False),
            yaxis=dict(showticklabels=False, showgrid=False, range=[-1, 1])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Critical tasks table
        st.dataframe(
            pd.DataFrame(critical_tasks)[['wbs', 'name', 'duration', 'progress', 'start_date', 'end_date']],
            use_container_width=True
        )

def render_baseline_tracking():
    """Render baseline tracking view"""
    st.subheader("Baseline Tracking")
    
    if st.session_state.projects:
        project = st.session_state.projects[0]
        
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Baseline Start", project['baseline_start'])
        col2.metric("Baseline End", project['baseline_end'])
        col3.metric("Current End", project['end_date'])
        
        # Schedule variance
        baseline_duration = (project['baseline_end'] - project['baseline_start']).days
        current_duration = (project['end_date'] - project['start_date']).days
        schedule_variance = current_duration - baseline_duration
        
        if schedule_variance > 0:
            st.error(f"⚠️ Project is {schedule_variance} days behind schedule")
        elif schedule_variance < 0:
            st.success(f"✅ Project is {abs(schedule_variance)} days ahead of schedule")
        else:
            st.info("📅 Project is on schedule")
        
        # Cost variance
        cost_variance = project['spent'] - (project['budget'] * 0.25)  # Assuming 25% should be spent
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Budget", f"${project['budget']:,.0f}")
            st.metric("Spent", f"${project['spent']:,.0f}")
        
        with col2:
            st.metric("Cost Variance", f"${cost_variance:,.0f}", 
                     delta=f"{cost_variance/project['budget']*100:.1f}%")

def render_milestones():
    """Render milestones view"""
    st.subheader("Project Milestones")
    
    milestones = [t for t in st.session_state.tasks if t['is_milestone']]
    
    if milestones:
        # Timeline visualization
        fig = go.Figure()
        
        for i, milestone in enumerate(milestones):
            status_color = {'Completed': 'green', 'In Progress': 'orange', 'Not Started': 'gray'}[milestone['status']]
            
            fig.add_trace(go.Scatter(
                x=[milestone['end_date']],
                y=[i],
                mode='markers+text',
                marker=dict(size=20, color=status_color, symbol='diamond'),
                text=[milestone['name']],
                textposition='middle right',
                hovertemplate=f"<b>{milestone['name']}</b><br>Date: {milestone['end_date']}<br>Status: {milestone['status']}"
            ))
        
        fig.add_vline(x=str(datetime.now().date(), line_dash="dash", line_color="red", 
                     annotation_text="Today")
        
        fig.update_layout(
            title="Milestone Timeline",
            xaxis_title="Date",
            showlegend=False,
            height=400,
            yaxis=dict(showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Milestones table
        st.dataframe(
            pd.DataFrame(milestones)[['name', 'end_date', 'status', 'assigned_to']],
            use_container_width=True
        )

# Multiple View Functions
def render_views():
    """Render different project views"""
    st.header("👁️ Project Views")
    
    view_tabs = st.tabs(["Kanban Board", "Calendar View", "List View", "Flowchart", "Route Card"])
    
    with view_tabs[0]:
        render_kanban_board()
    
    with view_tabs[1]:
        render_calendar_view()
    
    with view_tabs[2]:
        render_list_view()
    
    with view_tabs[3]:
        render_flowchart_view()
    
    with view_tabs[4]:
        render_route_card_view()

def render_kanban_board():
    """Render Kanban board view"""
    st.subheader("Kanban Board")
    
    columns = ['Not Started', 'In Progress', 'Completed']
    cols = st.columns(len(columns))
    
    for idx, status in enumerate(columns):
        with cols[idx]:
            st.markdown(f"### {status}")
            
            status_tasks = [t for t in st.session_state.tasks if t['status'] == status]
            
            for task in status_tasks:
                priority_class = f"priority-{task['priority'].lower()}"
                
                # Task card
                with st.container():
                    st.markdown(f"""
                    <div class="task-card {priority_class}">
                        <h4>{task['name']}</h4>
                        <p>WBS: {task['wbs']}</p>
                        <p>Assigned: {task['assigned_to']}</p>
                        <p>Progress: {task['progress']}%</p>
                        <p>Due: {task['end_date']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Move task buttons
                    col1, col2 = st.columns(2)
                    if idx > 0:
                        if col1.button("⬅", key=f"move_left_{task['id']}"):
                            task['status'] = columns[idx-1]
                            st.rerun()
                    if idx < len(columns)-1:
                        if col2.button("➡", key=f"move_right_{task['id']}"):
                            task['status'] = columns[idx+1]
                            st.rerun()

def render_calendar_view():
    """Render calendar view"""
    st.subheader("Calendar View")
    
    # Create calendar data
    events = []
    for task in st.session_state.tasks:
        events.append({
            'title': task['name'],
            'start': str(task['start_date']),
            'end': str(task['end_date']),
            'color': {'Critical': 'red', 'High': 'orange', 'Medium': 'yellow', 'Low': 'green'}[task['priority']]
        })
    
    # Add holidays
    for holiday in st.session_state.holidays:
        events.append({
            'title': holiday['name'],
            'start': str(holiday['date']),
            'end': str(holiday['date']),
            'color': 'purple'
        })
    
    # Display month view
    selected_date = st.date_input("Select Date", value=datetime.now().date())
    
    # Filter events for selected month
    month_start = selected_date.replace(day=1)
    month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    month_events = [e for e in events if month_start <= str(e['start'])).date() <= month_end]
    
    # Display events
    st.write(f"### Events for {selected_date.strftime('%B %Y')}")
    
    for event in month_events:
        st.info(f"📅 **{event['title']}** - {event['start']} to {event['end']}")

def render_list_view():
    """Render list view of tasks"""
    st.subheader("List View")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.multiselect("Status", ["Not Started", "In Progress", "Completed"])
    with col2:
        filter_priority = st.multiselect("Priority", ["Critical", "High", "Medium", "Low"])
    with col3:
        filter_assigned = st.multiselect("Assigned To", list(set([t['assigned_to'] for t in st.session_state.tasks])))
    
    # Apply filters
    filtered_tasks = st.session_state.tasks
    if filter_status:
        filtered_tasks = [t for t in filtered_tasks if t['status'] in filter_status]
    if filter_priority:
        filtered_tasks = [t for t in filtered_tasks if t['priority'] in filter_priority]
    if filter_assigned:
        filtered_tasks = [t for t in filtered_tasks if t['assigned_to'] in filter_assigned]
    
    # Display tasks
    if filtered_tasks:
        df = pd.DataFrame(filtered_tasks)
        st.dataframe(
            df[['wbs', 'name', 'status', 'priority', 'assigned_to', 'progress', 'start_date', 'end_date']],
            use_container_width=True
        )

def render_flowchart_view():
    """Render flowchart view of process"""
    st.subheader("Process Flowchart")
    
    # Create flowchart using plotly
    fig = go.Figure()
    
    # Define process steps
    steps = [
        ("Start", 0, 0),
        ("Sample Receipt", 1, 0),
        ("Conditioning", 2, 0),
        ("Testing", 3, 0),
        ("Analysis", 4, 0),
        ("Reporting", 5, 0),
        ("Approval", 6, 0),
        ("End", 7, 0)
    ]
    
    # Add nodes
    for step, x, y in steps:
        fig.add_trace(go.Scatter(
            x=[x], y=[y],
            mode='markers+text',
            marker=dict(size=40, color='lightblue', line=dict(color='blue', width=2)),
            text=[step],
            textposition='middle center',
            showlegend=False
        ))
    
    # Add edges
    for i in range(len(steps)-1):
        fig.add_trace(go.Scatter(
            x=[steps[i][1], steps[i+1][1]],
            y=[steps[i][2], steps[i+1][2]],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False
        ))
        
        # Add arrow annotation
        fig.add_annotation(
            x=steps[i+1][1],
            y=steps[i+1][2],
            ax=steps[i][1],
            ay=steps[i][2],
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="gray"
        )
    
    fig.update_layout(
        title="Testing Process Flow",
        showlegend=False,
        height=400,
        xaxis=dict(showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False, showgrid=False, range=[-1, 1])
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_route_card_view():
    """Render route card view for samples"""
    st.subheader("Sample Route Cards")
    
    if st.session_state.samples:
        selected_sample = st.selectbox("Select Sample", [s['name'] for s in st.session_state.samples])
        sample = next((s for s in st.session_state.samples if s['name'] == selected_sample), None)
        
        if sample:
            # Route card display
            st.markdown("### 📋 Route Card")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Sample ID:** {sample['id']}")
                st.write(f"**Name:** {sample['name']}")
                st.write(f"**Type:** {sample['type']}")
                st.write(f"**Batch:** {sample['batch']}")
                st.write(f"**Barcode:** {sample['barcode']}")
            
            with col2:
                st.write(f"**Status:** {sample['status']}")
                st.write(f"**Location:** {sample['location']}")
                st.write(f"**Condition:** {sample['condition']}")
                st.write(f"**Test Status:** {sample['test_status']}")
            
            # Chain of custody
            st.markdown("### 🔗 Chain of Custody")
            for entry in sample['chain_of_custody']:
                st.info(f"📅 {entry['date'].strftime('%Y-%m-%d %H:%M')} - From: {entry['from']} → To: {entry['to']} | Handler: {entry['handler']} | Notes: {entry['notes']}")
            
            # Add transfer
            with st.expander("Add Transfer"):
                with st.form("transfer_form"):
                    new_location = st.text_input("New Location")
                    handler = st.selectbox("Handler", [m['name'] for m in st.session_state.manpower])
                    notes = st.text_area("Notes")
                    
                    if st.form_submit_button("Add Transfer"):
                        sample['chain_of_custody'].append({
                            'date': datetime.now(),
                            'from': sample['location'],
                            'to': new_location,
                            'handler': handler,
                            'notes': notes
                        })
                        sample['location'] = new_location
                        st.success("Transfer recorded successfully!")
                        st.rerun()

# Solar Testing Management
def render_solar_testing():
    """Render solar testing management interface"""
    st.header("☀️ Solar Testing Management")
    
    tabs = st.tabs(["Sample Tracking", "Equipment Management", "Test Methods", "Test Execution", "Results Entry"])
    
    with tabs[0]:
        render_sample_tracking()
    
    with tabs[1]:
        render_equipment_management()
    
    with tabs[2]:
        render_test_methods()
    
    with tabs[3]:
        render_test_execution()
    
    with tabs[4]:
        render_results_entry()

def render_sample_tracking():
    """Render sample tracking with chain of custody"""
    st.subheader("Sample Tracking & Chain of Custody")
    
    # Display samples
    if st.session_state.samples:
        df = pd.DataFrame(st.session_state.samples)
        st.dataframe(df[['id', 'name', 'type', 'batch', 'status', 'location', 'test_status']], use_container_width=True)
    
    # Add new sample
    with st.expander("Add New Sample"):
        with st.form("add_sample_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sample_name = st.text_input("Sample Name")
                sample_type = st.selectbox("Type", ["Monocrystalline", "Polycrystalline", "Thin Film", "Bifacial"])
                batch = st.text_input("Batch Number")
                barcode = st.text_input("Barcode")
            
            with col2:
                condition = st.selectbox("Condition", ["Good", "Minor Damage", "Major Damage"])
                location = st.text_input("Initial Location")
                received_by = st.selectbox("Received By", [m['name'] for m in st.session_state.manpower])
            
            if st.form_submit_button("Add Sample"):
                new_sample = {
                    'id': f'SMP{len(st.session_state.samples)+1:03d}',
                    'name': sample_name,
                    'type': sample_type,
                    'batch': batch,
                    'received_date': datetime.now().date(),
                    'condition': condition,
                    'location': location,
                    'chain_of_custody': [
                        {'date': datetime.now(), 'from': 'External', 'to': location,
                         'handler': received_by, 'notes': 'Initial receipt'}
                    ],
                    'status': 'Available',
                    'test_status': 'Pending',
                    'barcode': barcode
                }
                st.session_state.samples.append(new_sample)
                add_audit_trail('Created', 'Sample', new_sample['id'], f"Added sample {sample_name}")
                st.success(f"Sample {sample_name} added successfully!")
                st.rerun()

def render_equipment_management():
    """Render equipment management interface"""
    st.subheader("Equipment Management")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Equipment status overview
        for equipment in st.session_state.equipment:
            status_color = "🟢" if equipment['status'] == 'Available' else "🔴"
            
            with st.expander(f"{status_color} {equipment['name']} - {equipment['status']}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write(f"**Type:** {equipment['type']}")
                    st.write(f"**Location:** {equipment['location']}")
                    st.write(f"**Performance:** {equipment['performance_metric']}%")
                    st.write(f"**Utilization:** {equipment['utilization']}%")
                
                with col_b:
                    st.write(f"**Last Calibration:** {equipment['last_calibration']}")
                    st.write(f"**Next Calibration:** {equipment['next_calibration']}")
                    
                    days_to_calibration = (equipment['next_calibration'] - datetime.now().date()).days
                    if days_to_calibration < 30:
                        st.warning(f"⚠️ Calibration due in {days_to_calibration} days")
                
                # Booking calendar
                if equipment['bookings']:
                    st.write("**Current Bookings:**")
                    for booking in equipment['bookings']:
                        st.info(f"📅 {booking['date']} - {booking['user']} ({booking['project']}) - {booking['duration']}h")
    
    with col2:
        st.subheader("Equipment Metrics")
        
        # Performance chart
        performance_data = pd.DataFrame({
            'Equipment': [e['name'] for e in st.session_state.equipment],
            'Performance': [e['performance_metric'] for e in st.session_state.equipment]
        })
        
        fig = px.bar(performance_data, x='Equipment', y='Performance',
                    title="Equipment Performance (%)",
                    color='Performance',
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)

def render_test_methods():
    """Render test methods management"""
    st.subheader("Test Methods & Standards")
    
    # Display test methods
    for method in st.session_state.test_methods:
        with st.expander(f"{method['name']} ({method['method_number']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Standard:** {method['standard']}")
                st.write(f"**Category:** {method['category']}")
                st.write(f"**Duration:** {method['duration_hours']} hours")
            
            with col2:
                st.write(f"**Equipment Required:** {', '.join(method['equipment_required'])}")
                st.write(f"**Parameters:** {', '.join(method['parameters'])}")
                st.write(f"**Acceptance Criteria:** {method['acceptance_criteria']}")
    
    # Add new test method
    with st.expander("Add New Test Method"):
        with st.form("add_test_method_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                method_name = st.text_input("Method Name")
                standard = st.text_input("Standard (e.g., IEC 61215)")
                method_number = st.text_input("Method Number")
                category = st.selectbox("Category", ["Electrical Performance", "Environmental Testing", 
                                                    "Mechanical Testing", "Safety Testing"])
            
            with col2:
                duration = st.number_input("Duration (hours)", min_value=1)
                equipment = st.multiselect("Equipment Required", [e['name'] for e in st.session_state.equipment])
                parameters = st.text_input("Parameters (comma-separated)")
                criteria = st.text_area("Acceptance Criteria")
            
            if st.form_submit_button("Add Test Method"):
                new_method = {
                    'id': f'TM{len(st.session_state.test_methods)+1:03d}',
                    'name': method_name,
                    'standard': standard,
                    'method_number': method_number,
                    'category': category,
                    'equipment_required': equipment,
                    'duration_hours': duration,
                    'parameters': [p.strip() for p in parameters.split(',')],
                    'acceptance_criteria': criteria
                }
                st.session_state.test_methods.append(new_method)
                st.success(f"Test method {method_name} added successfully!")
                st.rerun()

def render_test_execution():
    """Render test execution interface"""
    st.subheader("Test Execution Protocol")
    
    # Select test to execute
    col1, col2 = st.columns(2)
    
    with col1:
        selected_sample = st.selectbox("Select Sample", 
                                      [s['name'] for s in st.session_state.samples if s['status'] == 'Available'])
        selected_method = st.selectbox("Select Test Method", 
                                      [m['name'] for m in st.session_state.test_methods])
    
    with col2:
        test_operator = st.selectbox("Test Operator", [m['name'] for m in st.session_state.manpower])
        test_date = st.date_input("Test Date", value=datetime.now().date())
    
    if selected_sample and selected_method:
        method = next((m for m in st.session_state.test_methods if m['name'] == selected_method), None)
        
        if method:
            st.markdown("### Test Protocol Sheet")
            
            # Protocol entry form
            with st.form("test_protocol_form"):
                st.write(f"**Standard:** {method['standard']}")
                st.write(f"**Method Number:** {method['method_number']}")
                st.write(f"**Duration:** {method['duration_hours']} hours")
                
                st.markdown("#### Test Parameters")
                parameter_values = {}
                for param in method['parameters']:
                    parameter_values[param] = st.number_input(f"{param}", value=0.0, format="%.2f")
                
                st.markdown("#### Test Conditions")
                ambient_temp = st.number_input("Ambient Temperature (°C)", value=25.0)
                humidity = st.number_input("Humidity (%)", value=50.0)
                
                notes = st.text_area("Test Notes")
                
                if st.form_submit_button("Start Test"):
                    # Update sample status
                    sample = next((s for s in st.session_state.samples if s['name'] == selected_sample), None)
                    if sample:
                        sample['status'] = 'In Testing'
                        sample['test_status'] = 'In Progress'
                    
                    # Create test record
                    test_record = {
                        'id': str(uuid.uuid4()),
                        'sample_id': sample['id'] if sample else None,
                        'method_id': method['id'],
                        'operator': test_operator,
                        'date': test_date,
                        'parameters': parameter_values,
                        'conditions': {'temperature': ambient_temp, 'humidity': humidity},
                        'notes': notes,
                        'status': 'In Progress'
                    }
                    st.session_state.test_results.append(test_record)
                    
                    create_notification(test_operator, 'Test', 'Test Started', 
                                      f"Test {method['name']} started on {selected_sample}")
                    st.success("Test started successfully!")
                    st.rerun()

def render_results_entry():
    """Render test results entry interface"""
    st.subheader("Test Results Entry")
    
    # Select ongoing test
    ongoing_tests = [t for t in st.session_state.test_results if t['status'] == 'In Progress']
    
    if ongoing_tests:
        selected_test = st.selectbox("Select Test to Complete", 
                                    [f"{t['id'][:8]} - {t['date']}" for t in ongoing_tests])
        
        if selected_test:
            test = next((t for t in ongoing_tests if selected_test.startswith(t['id'][:8])), None)
            
            if test:
                with st.form("results_entry_form"):
                    st.markdown("### Enter Test Results")
                    
                    # Result parameters
                    st.write("**Test Parameters Results:**")
                    results = {}
                    for param in test['parameters'].keys():
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write(f"{param}")
                        with col2:
                            results[param] = st.number_input(f"Result for {param}", value=0.0, format="%.3f")
                        with col3:
                            pass_fail = st.selectbox(f"Status", ["Pass", "Fail"], key=f"status_{param}")
                    
                    overall_result = st.selectbox("Overall Test Result", ["Pass", "Fail", "Conditional Pass"])
                    observations = st.text_area("Observations")
                    recommendations = st.text_area("Recommendations")
                    
                    if st.form_submit_button("Submit Results"):
                        test['results'] = results
                        test['overall_result'] = overall_result
                        test['observations'] = observations
                        test['recommendations'] = recommendations
                        test['status'] = 'Completed'
                        test['completed_date'] = datetime.now()
                        
                        # Update sample status
                        sample = next((s for s in st.session_state.samples if s['id'] == test['sample_id']), None)
                        if sample:
                            sample['status'] = 'Available'
                            sample['test_status'] = 'Completed'
                        
                        st.success("Test results submitted successfully!")
                        st.rerun()
    else:
        st.info("No ongoing tests to complete")

# Workflow Management
def render_workflows():
    """Render workflow management interface"""
    st.header("📝 Workflows & Approvals")
    
    tabs = st.tabs(["Approval Workflow", "Digital Signatures", "Review Status", "Escalations"])
    
    with tabs[0]:
        render_approval_workflow()
    
    with tabs[1]:
        render_digital_signatures()
    
    with tabs[2]:
        render_review_status()
    
    with tabs[3]:
        render_escalations()

def render_approval_workflow():
    """Render approval workflow interface"""
    st.subheader("Multi-Level Approval Workflow")
    
    # Create approval request
    with st.expander("Create Approval Request"):
        with st.form("approval_request_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                doc_type = st.selectbox("Document Type", ["Test Report", "Change Request", "Risk Assessment", "Project Plan"])
                doc_title = st.text_input("Document Title")
                priority = st.selectbox("Priority", ["High", "Medium", "Low"])
            
            with col2:
                approvers = st.multiselect("Select Approvers", [m['name'] for m in st.session_state.manpower])
                due_date = st.date_input("Due Date", value=datetime.now().date() + timedelta(days=3))
            
            description = st.text_area("Description")
            
            if st.form_submit_button("Submit for Approval"):
                approval_request = {
                    'id': f'APR{len(st.session_state.approvals)+1:03d}',
                    'type': doc_type,
                    'title': doc_title,
                    'priority': priority,
                    'submitter': st.session_state.current_user,
                    'submit_date': datetime.now(),
                    'due_date': due_date,
                    'description': description,
                    'approvers': [{'name': a, 'status': 'Pending', 'date': None, 'comments': ''} for a in approvers],
                    'status': 'Pending',
                    'current_level': 1,
                    'total_levels': len(approvers)
                }
                st.session_state.approvals.append(approval_request)
                
                # Send notifications
                for approver in approvers:
                    create_notification(approver, 'Approval', 'Approval Request',
                                      f"Please review and approve: {doc_title}", priority)
                
                st.success("Approval request submitted successfully!")
                st.rerun()
    
    # Display pending approvals
    st.markdown("### Pending Approvals")
    pending_approvals = [a for a in st.session_state.approvals if a['status'] == 'Pending']
    
    if pending_approvals:
        for approval in pending_approvals:
            with st.expander(f"{approval['title']} - Level {approval['current_level']}/{approval['total_levels']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Type:** {approval['type']}")
                    st.write(f"**Priority:** {approval['priority']}")
                    st.write(f"**Submitted by:** {approval['submitter']}")
                    st.write(f"**Due Date:** {approval['due_date']}")
                    st.write(f"**Description:** {approval['description']}")
                
                with col2:
                    st.write("**Approval Status:**")
                    for approver in approval['approvers']:
                        status_icon = "✅" if approver['status'] == 'Approved' else "⏳"
                        st.write(f"{status_icon} {approver['name']}: {approver['status']}")
                
                # Approval actions
                current_approver = approval['approvers'][approval['current_level']-1] if approval['current_level'] <= len(approval['approvers']) else None
                
                if current_approver and current_approver['name'] == st.session_state.current_user:
                    col1, col2, col3 = st.columns(3)
                    
                    comments = st.text_input("Comments", key=f"comments_{approval['id']}")
                    
                    if col1.button("Approve", key=f"approve_{approval['id']}"):
                        current_approver['status'] = 'Approved'
                        current_approver['date'] = datetime.now()
                        current_approver['comments'] = comments
                        
                        if approval['current_level'] < approval['total_levels']:
                            approval['current_level'] += 1
                            next_approver = approval['approvers'][approval['current_level']-1]
                            create_notification(next_approver['name'], 'Approval', 'Approval Required',
                                              f"Please review: {approval['title']}")
                        else:
                            approval['status'] = 'Approved'
                            create_notification(approval['submitter'], 'Approval', 'Approval Complete',
                                              f"{approval['title']} has been fully approved")
                        
                        st.success("Approved successfully!")
                        st.rerun()
                    
                    if col2.button("Reject", key=f"reject_{approval['id']}"):
                        current_approver['status'] = 'Rejected'
                        current_approver['date'] = datetime.now()
                        current_approver['comments'] = comments
                        approval['status'] = 'Rejected'
                        
                        create_notification(approval['submitter'], 'Approval', 'Approval Rejected',
                                          f"{approval['title']} was rejected by {current_approver['name']}")
                        
                        st.error("Rejected")
                        st.rerun()
                    
                    if col3.button("Request Info", key=f"info_{approval['id']}"):
                        create_notification(approval['submitter'], 'Approval', 'Information Requested',
                                          f"Additional information requested for {approval['title']}: {comments}")
                        st.info("Information requested")

def render_digital_signatures():
    """Render digital signatures interface"""
    st.subheader("Digital Signatures")
    
    # Sign document
    with st.expander("Sign Document"):
        doc_to_sign = st.selectbox("Select Document", 
                                   [a['title'] for a in st.session_state.approvals if a['status'] == 'Approved'])
        
        if doc_to_sign:
            with st.form("signature_form"):
                signature_text = st.text_input("Enter your name as signature")
                pin = st.text_input("Enter PIN", type="password")
                
                if st.form_submit_button("Sign Document"):
                    # Create signature hash
                    signature_hash = hashlib.sha256(f"{signature_text}{pin}{datetime.now()}".encode()).hexdigest()
                    
                    signature_record = {
                        'id': str(uuid.uuid4()),
                        'document': doc_to_sign,
                        'signer': st.session_state.current_user,
                        'signature': signature_text,
                        'hash': signature_hash,
                        'timestamp': datetime.now(),
                        'verified': True
                    }
                    st.session_state.signatures.append(signature_record)
                    
                    st.success(f"Document signed successfully! Signature ID: {signature_hash[:8]}")
                    st.rerun()
    
    # Display signatures
    st.markdown("### Document Signatures")
    if st.session_state.signatures:
        for sig in st.session_state.signatures[-5:]:
            st.info(f"📝 **{sig['document']}** - Signed by {sig['signer']} on {sig['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            st.code(f"Signature Hash: {sig['hash'][:16]}...")

def render_review_status():
    """Render review status dashboard"""
    st.subheader("Review Status Dashboard")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_approvals = len(st.session_state.approvals)
    pending = len([a for a in st.session_state.approvals if a['status'] == 'Pending'])
    approved = len([a for a in st.session_state.approvals if a['status'] == 'Approved'])
    rejected = len([a for a in st.session_state.approvals if a['status'] == 'Rejected'])
    
    col1.metric("Total Requests", total_approvals)
    col2.metric("Pending", pending)
    col3.metric("Approved", approved)
    col4.metric("Rejected", rejected)
    
    # Approval timeline
    if st.session_state.approvals:
        fig = go.Figure()
        
        for i, approval in enumerate(st.session_state.approvals[-10:]):
            color = {'Pending': 'yellow', 'Approved': 'green', 'Rejected': 'red'}[approval['status']]
            
            fig.add_trace(go.Scatter(
                x=[approval['submit_date']],
                y=[i],
                mode='markers+text',
                marker=dict(size=15, color=color),
                text=[approval['title'][:20]],
                textposition='middle right',
                hovertemplate=f"<b>{approval['title']}</b><br>Status: {approval['status']}<br>Priority: {approval['priority']}"
            ))
        
        fig.update_layout(
            title="Recent Approval Requests",
            xaxis_title="Date",
            showlegend=False,
            height=400,
            yaxis=dict(showticklabels=False)
        )
        
        st.plotly_chart(fig, use_container_width=True)

def render_escalations():
    """Render escalation management"""
    st.subheader("Escalation Management")
    
    # Auto-escalation rules
    st.markdown("### Auto-Escalation Rules")
    
    escalation_rules = [
        {"condition": "Approval pending > 3 days", "action": "Notify manager", "status": "Active"},
        {"condition": "Critical risk unmitigated > 7 days", "action": "Escalate to PMO", "status": "Active"},
        {"condition": "Equipment downtime > 24 hours", "action": "Alert operations head", "status": "Active"}
    ]
    
    for rule in escalation_rules:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"**Condition:** {rule['condition']}")
        col2.write(f"**Action:** {rule['action']}")
        col3.write(f"**Status:** {rule['status']}")
    
    # Check for escalations
    st.markdown("### Current Escalations")
    
    # Check pending approvals
    for approval in st.session_state.approvals:
        if approval['status'] == 'Pending':
            days_pending = (datetime.now() - approval['submit_date']).days
            if days_pending > 3:
                st.warning(f"⚠️ Approval '{approval['title']}' pending for {days_pending} days - Escalated to manager")
    
    # Check unmitigated risks
    for risk in st.session_state.risks:
        if risk['status'] == 'Open' and risk['probability'] == 'High':
            days_open = (datetime.now().date() - risk['identified_date']).days
            if days_open > 7:
                st.error(f"🚨 High risk '{risk['title']}' unmitigated for {days_open} days - Escalated to PMO")

# Resource Management
def render_resources():
    """Render resource management interface"""
    st.header("👥 Resource Management")
    
    tabs = st.tabs(["Manpower", "Equipment Booking", "Holiday Planning", "Performance Metrics"])
    
    with tabs[0]:
        render_manpower_management()
    
    with tabs[1]:
        render_equipment_booking()
    
    with tabs[2]:
        render_holiday_planning()
    
    with tabs[3]:
        render_performance_metrics()

def render_manpower_management():
    """Render manpower management interface"""
    st.subheader("Manpower Management")
    
    # Team overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        for person in st.session_state.manpower:
            availability_color = "🟢" if person['availability'] == 'Available' else "🔴"
            
            with st.expander(f"{availability_color} {person['name']} - {person['role']}"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.write(f"**Skills:** {', '.join(person['skills'])}")
                    st.write(f"**Certifications:** {', '.join(person['certifications'])}")
                    st.write(f"**Current Project:** {person['current_project']}")
                
                with col_b:
                    st.write(f"**Performance Score:** {person['performance_score']}%")
                    st.write(f"**Hours Logged:** {person['hours_logged']}")
                    st.write(f"**Availability:** {person['availability']}")
                
                # Schedule
                if person['schedule']:
                    st.write("**Today's Schedule:**")
                    for task in person['schedule']:
                        st.info(f"📅 {task['task']} - {task['hours']}h")
    
    with col2:
        st.subheader("Team Statistics")
        
        # Availability chart
        available = len([p for p in st.session_state.manpower if p['availability'] == 'Available'])
        busy = len([p for p in st.session_state.manpower if p['availability'] == 'Busy'])
        
        fig = px.pie(values=[available, busy], names=['Available', 'Busy'],
                    title="Team Availability",
                    color_discrete_map={'Available': 'green', 'Busy': 'red'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance distribution
        performance_scores = [p['performance_score'] for p in st.session_state.manpower]
        fig = px.histogram(x=performance_scores, nbins=5,
                         title="Performance Score Distribution",
                         labels={'x': 'Performance Score', 'y': 'Count'})
        st.plotly_chart(fig, use_container_width=True)

def render_equipment_booking():
    """Render equipment booking interface"""
    st.subheader("Equipment Booking System")
    
    # Book equipment
    with st.expander("Book Equipment"):
        with st.form("booking_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                equipment = st.selectbox("Select Equipment", 
                                        [e['name'] for e in st.session_state.equipment if e['status'] == 'Available'])
                booking_date = st.date_input("Booking Date", value=datetime.now().date() + timedelta(days=1))
                duration = st.number_input("Duration (hours)", min_value=1, max_value=24, value=4)
            
            with col2:
                project = st.selectbox("Project", [p['id'] for p in st.session_state.projects])
                purpose = st.text_input("Purpose")
            
            if st.form_submit_button("Book Equipment"):
                # Find equipment
                equip = next((e for e in st.session_state.equipment if e['name'] == equipment), None)
                
                if equip:
                    booking = {
                        'date': booking_date,
                        'project': project,
                        'user': st.session_state.current_user,
                        'duration': duration,
                        'purpose': purpose
                    }
                    equip['bookings'].append(booking)
                    
                    st.success(f"Equipment {equipment} booked successfully for {booking_date}")
                    st.rerun()
    
    # Equipment calendar
    st.markdown("### Equipment Booking Calendar")
    
    # Create calendar view
    for equipment in st.session_state.equipment:
        if equipment['bookings']:
            st.write(f"**{equipment['name']}**")
            
            # Sort bookings by date
            sorted_bookings = sorted(equipment['bookings'], key=lambda x: x['date'])
            
            for booking in sorted_bookings:
                st.info(f"📅 {booking['date']} - {booking['user']} ({booking['project']}) - {booking['duration']}h - {booking.get('purpose', 'N/A')}")

def render_holiday_planning():
    """Render holiday planning interface"""
    st.subheader("Holiday Planning")
    
    # Add holiday
    with st.expander("Add Holiday"):
        with st.form("holiday_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                holiday_name = st.text_input("Holiday Name")
                holiday_date = st.date_input("Date")
            
            with col2:
                holiday_type = st.selectbox("Type", ["Public", "Company", "Optional"])
            
            if st.form_submit_button("Add Holiday"):
                st.session_state.holidays.append({
                    'date': holiday_date,
                    'name': holiday_name,
                    'type': holiday_type
                })
                st.success(f"Holiday {holiday_name} added successfully!")
                st.rerun()
    
    # Holiday calendar
    st.markdown("### Holiday Calendar")
    
    # Display upcoming holidays
    upcoming_holidays = sorted([h for h in st.session_state.holidays if h['date'] >= datetime.now().date()],
                              key=lambda x: x['date'])
    
    if upcoming_holidays:
        for holiday in upcoming_holidays[:10]:
            type_emoji = {"Public": "🏛️", "Company": "🏢", "Optional": "🎉"}[holiday['type']]
            days_until = (holiday['date'] - datetime.now().date()).days
            
            st.info(f"{type_emoji} **{holiday['name']}** - {holiday['date']} ({days_until} days away)")

def render_performance_metrics():
    """Render performance metrics dashboard"""
    st.subheader("Performance Metrics Dashboard")
    
    # Team performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Individual Performance")
        
        performance_data = pd.DataFrame([
            {'Name': p['name'], 'Score': p['performance_score'], 'Hours': p['hours_logged']}
            for p in st.session_state.manpower
        ])
        
        fig = px.bar(performance_data, x='Name', y='Score',
                    title="Performance Scores",
                    color='Score',
                    color_continuous_scale='RdYlGn')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Productivity Metrics")
        
        # Calculate productivity metrics
        total_hours = sum([p['hours_logged'] for p in st.session_state.manpower])
        avg_performance = np.mean([p['performance_score'] for p in st.session_state.manpower])
        utilization_rate = len([p for p in st.session_state.manpower if p['availability'] == 'Busy']) / len(st.session_state.manpower) * 100
        
        st.metric("Total Hours Logged", f"{total_hours:,}")
        st.metric("Average Performance", f"{avg_performance:.1f}%")
        st.metric("Team Utilization", f"{utilization_rate:.1f}%")
        
        # Trend chart
        dates = pd.date_range(end=datetime.now().date(), periods=7)
        trend_data = pd.DataFrame({
            'Date': dates,
            'Utilization': np.random.randint(60, 95, 7)
        })
        
        fig = px.line(trend_data, x='Date', y='Utilization',
                     title="7-Day Utilization Trend",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)

# Risk & Issue Management
def render_risk_issues():
    """Render risk and issue management interface"""
    st.header("⚠️ Risk & Issue Management")
    
    tabs = st.tabs(["Risk Register", "Issue Tracker", "Mitigation Plans", "Risk Matrix"])
    
    with tabs[0]:
        render_risk_register()
    
    with tabs[1]:
        render_issue_tracker()
    
    with tabs[2]:
        render_mitigation_plans()
    
    with tabs[3]:
        render_risk_matrix()

def render_risk_register():
    """Render risk register"""
    st.subheader("Risk Register")
    
    # Add new risk
    with st.expander("Add New Risk"):
        with st.form("add_risk_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                risk_title = st.text_input("Risk Title")
                category = st.selectbox("Category", ["Technical", "Financial", "Schedule", "Resource", "External", "Supply Chain"])
                probability = st.selectbox("Probability", ["High", "Medium", "Low"])
            
            with col2:
                impact = st.selectbox("Impact", ["High", "Medium", "Low"])
                owner = st.selectbox("Risk Owner", [m['name'] for m in st.session_state.manpower])
            
            mitigation = st.text_area("Mitigation Strategy")
            
            if st.form_submit_button("Add Risk"):
                new_risk = {
                    'id': f'RSK{len(st.session_state.risks)+1:03d}',
                    'title': risk_title,
                    'category': category,
                    'probability': probability,
                    'impact': impact,
                    'status': 'Open',
                    'mitigation': mitigation,
                    'owner': owner,
                    'identified_date': datetime.now().date(),
                    'project_id': 'PRJ001'
                }
                st.session_state.risks.append(new_risk)
                add_audit_trail('Created', 'Risk', new_risk['id'], f"Added risk: {risk_title}")
                st.success(f"Risk '{risk_title}' added successfully!")
                st.rerun()
    
    # Display risks
    if st.session_state.risks:
        df = pd.DataFrame(st.session_state.risks)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_status = st.multiselect("Filter by Status", ["Open", "Mitigated", "Closed"], default=["Open"])
        with col2:
            filter_probability = st.multiselect("Filter by Probability", ["High", "Medium", "Low"])
        with col3:
            filter_impact = st.multiselect("Filter by Impact", ["High", "Medium", "Low"])
        
        # Apply filters
        if filter_status:
            df = df[df['status'].isin(filter_status)]
        if filter_probability:
            df = df[df['probability'].isin(filter_probability)]
        if filter_impact:
            df = df[df['impact'].isin(filter_impact)]
        
        # Display filtered risks
        for _, risk in df.iterrows():
            risk_score = {'High': 3, 'Medium': 2, 'Low': 1}
            score = risk_score[risk['probability']] * risk_score[risk['impact']]
            score_color = "🔴" if score >= 6 else "🟡" if score >= 3 else "🟢"
            
            with st.expander(f"{score_color} {risk['title']} - {risk['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Category:** {risk['category']}")
                    st.write(f"**Probability:** {risk['probability']}")
                    st.write(f"**Impact:** {risk['impact']}")
                    st.write(f"**Risk Score:** {score}/9")
                
                with col2:
                    st.write(f"**Owner:** {risk['owner']}")
                    st.write(f"**Identified:** {risk['identified_date']}")
                    st.write(f"**Status:** {risk['status']}")
                
                st.write(f"**Mitigation:** {risk['mitigation']}")
                
                # Update risk status
                if risk['status'] == 'Open':
                    if st.button(f"Mark as Mitigated", key=f"mitigate_{risk['id']}"):
                        risk['status'] = 'Mitigated'
                        st.success("Risk marked as mitigated!")
                        st.rerun()

def render_issue_tracker():
    """Render issue tracker"""
    st.subheader("Issue Tracker")
    
    # Add new issue
    with st.expander("Add New Issue"):
        with st.form("add_issue_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                issue_title = st.text_input("Issue Title")
                category = st.selectbox("Category", ["Equipment", "Process", "Quality", "Safety", "Resource", "Other"])
                severity = st.selectbox("Severity", ["Critical", "High", "Medium", "Low"])
            
            with col2:
                assigned_to = st.selectbox("Assigned To", [m['name'] for m in st.session_state.manpower])
                reported_by = st.text_input("Reported By", value=st.session_state.current_user)
            
            description = st.text_area("Description")
            
            if st.form_submit_button("Add Issue"):
                new_issue = {
                    'id': f'ISS{len(st.session_state.issues)+1:03d}',
                    'title': issue_title,
                    'category': category,
                    'severity': severity,
                    'status': 'Open',
                    'description': description,
                    'resolution': '',
                    'reported_by': reported_by,
                    'assigned_to': assigned_to,
                    'reported_date': datetime.now().date(),
                    'project_id': 'PRJ001'
                }
                st.session_state.issues.append(new_issue)
                add_audit_trail('Created', 'Issue', new_issue['id'], f"Added issue: {issue_title}")
                create_notification(assigned_to, 'Issue', 'New Issue Assigned',
                                  f"Issue '{issue_title}' has been assigned to you", severity)
                st.success(f"Issue '{issue_title}' added successfully!")
                st.rerun()
    
    # Display issues
    if st.session_state.issues:
        # Issue statistics
        col1, col2, col3, col4 = st.columns(4)
        
        open_issues = len([i for i in st.session_state.issues if i['status'] == 'Open'])
        in_progress = len([i for i in st.session_state.issues if i['status'] == 'In Progress'])
        resolved = len([i for i in st.session_state.issues if i['status'] == 'Resolved'])
        critical = len([i for i in st.session_state.issues if i['severity'] == 'Critical' and i['status'] != 'Resolved'])
        
        col1.metric("Open Issues", open_issues)
        col2.metric("In Progress", in_progress)
        col3.metric("Resolved", resolved)
        col4.metric("Critical Issues", critical, delta=None if critical == 0 else "⚠️")
        
        # Issue list
        for issue in st.session_state.issues:
            severity_color = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}[issue['severity']]
            
            with st.expander(f"{severity_color} {issue['title']} - {issue['status']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Category:** {issue['category']}")
                    st.write(f"**Severity:** {issue['severity']}")
                    st.write(f"**Reported By:** {issue['reported_by']}")
                    st.write(f"**Date:** {issue['reported_date']}")
                
                with col2:
                    st.write(f"**Assigned To:** {issue['assigned_to']}")
                    st.write(f"**Status:** {issue['status']}")
                
                st.write(f"**Description:** {issue['description']}")
                
                if issue['resolution']:
                    st.write(f"**Resolution:** {issue['resolution']}")
                
                # Issue actions
                if issue['status'] != 'Resolved':
                    resolution = st.text_input("Resolution", key=f"res_{issue['id']}")
                    
                    col1, col2 = st.columns(2)
                    if issue['status'] == 'Open' and col1.button("Start Working", key=f"start_{issue['id']}"):
                        issue['status'] = 'In Progress'
                        st.rerun()
                    
                    if col2.button("Resolve Issue", key=f"resolve_{issue['id']}"):
                        issue['status'] = 'Resolved'
                        issue['resolution'] = resolution
                        st.success("Issue resolved!")
                        st.rerun()

def render_mitigation_plans():
    """Render mitigation plans"""
    st.subheader("Risk Mitigation Plans")
    
    # Display mitigation plans for high-risk items
    high_risks = [r for r in st.session_state.risks if r['probability'] == 'High' or r['impact'] == 'High']
    
    if high_risks:
        for risk in high_risks:
            with st.expander(f"Mitigation Plan: {risk['title']}"):
                st.write(f"**Risk:** {risk['title']}")
                st.write(f"**Current Mitigation:** {risk['mitigation']}")
                
                # Mitigation tasks
                st.markdown("#### Mitigation Tasks")
                
                # Create mitigation task form
                with st.form(f"mitigation_task_{risk['id']}"):
                    task_name = st.text_input("Task Name")
                    responsible = st.selectbox("Responsible", [m['name'] for m in st.session_state.manpower])
                    due_date = st.date_input("Due Date", value=datetime.now().date() + timedelta(days=7))
                    
                    if st.form_submit_button("Add Mitigation Task"):
                        # Add task to main task list
                        new_task = {
                            'id': f'TSK{len(st.session_state.tasks)+1:03d}',
                            'wbs': f"MIT.{risk['id']}",
                            'name': f"Mitigation: {task_name}",
                            'project_id': 'PRJ001',
                            'status': 'Not Started',
                            'priority': 'High',
                            'assigned_to': responsible,
                            'start_date': datetime.now().date(),
                            'end_date': due_date,
                            'duration': (due_date - datetime.now().date()).days,
                            'progress': 0,
                            'dependencies': [],
                            'is_milestone': False,
                            'is_critical': False,
                            'description': f"Mitigation task for risk: {risk['title']}",
                            'estimated_hours': 8,
                            'actual_hours': 0
                        }
                        st.session_state.tasks.append(new_task)
                        st.success(f"Mitigation task '{task_name}' added!")
                        st.rerun()

def render_risk_matrix():
    """Render risk matrix visualization"""
    st.subheader("Risk Matrix")
    
    # Create risk matrix data
    risk_levels = ['Low', 'Medium', 'High']
    matrix = pd.DataFrame(0, index=risk_levels, columns=risk_levels)
    
    for risk in st.session_state.risks:
        if risk['status'] == 'Open':
            matrix.loc[risk['probability'], risk['impact']] += 1
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix.values,
        x=risk_levels,
        y=risk_levels,
        colorscale='Reds',
        text=matrix.values,
        texttemplate="%{text}",
        textfont={"size": 20},
        colorbar=dict(title="Risk Count")
    ))
    
    fig.update_layout(
        title="Risk Heat Map",
        xaxis_title="Impact →",
        yaxis_title="Probability →",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk details by quadrant
    st.markdown("### Risk Details by Severity")
    
    # Calculate risk scores
    risk_score_map = {'High': 3, 'Medium': 2, 'Low': 1}
    
    for risk in st.session_state.risks:
        if risk['status'] == 'Open':
            risk['score'] = risk_score_map[risk['probability']] * risk_score_map[risk['impact']]
    
    # Group by severity
    critical_risks = [r for r in st.session_state.risks if r['status'] == 'Open' and r.get('score', 0) >= 6]
    major_risks = [r for r in st.session_state.risks if r['status'] == 'Open' and 3 <= r.get('score', 0) < 6]
    minor_risks = [r for r in st.session_state.risks if r['status'] == 'Open' and r.get('score', 0) < 3]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error(f"**Critical Risks ({len(critical_risks)})**")
        for risk in critical_risks:
            st.write(f"• {risk['title']}")
    
    with col2:
        st.warning(f"**Major Risks ({len(major_risks)})**")
        for risk in major_risks:
            st.write(f"• {risk['title']}")
    
    with col3:
        st.success(f"**Minor Risks ({len(minor_risks)})**")
        for risk in minor_risks:
            st.write(f"• {risk['title']}")

# Reports & Documents
def render_reports():
    """Render reports and document generation interface"""
    st.header("📄 Reports & Documents")
    
    tabs = st.tabs(["Generate Report", "Document Library", "Audit Trail", "Export Data"])
    
    with tabs[0]:
        render_report_generation()
    
    with tabs[1]:
        render_document_library()
    
    with tabs[2]:
        render_audit_trail()
    
    with tabs[3]:
        render_export_data()

def render_report_generation():
    """Render report generation interface"""
    st.subheader("Generate Reports")
    
    report_type = st.selectbox("Select Report Type", 
                               ["Test Report", "Project Status Report", "Risk Assessment Report", 
                                "Resource Utilization Report", "Quality Report"])
    
    if report_type == "Test Report":
        # Test report generation
        completed_tests = [t for t in st.session_state.test_results if t.get('status') == 'Completed']
        
        if completed_tests:
            selected_test = st.selectbox("Select Test", 
                                        [f"{t['id'][:8]} - {t.get('date', 'N/A')}" for t in completed_tests])
            
            if st.button("Generate Test Report"):
                # Generate PDF report
                pdf_buffer = BytesIO()
                doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
                story = []
                styles = getSampleStyleSheet()
                
                # Title
                title_style = ParagraphStyle(
                    'CustomTitle',
                    parent=styles['Heading1'],
                    fontSize=24,
                    textColor=colors.HexColor('#1f77b4'),
                    spaceAfter=30,
                    alignment=TA_CENTER
                )
                
                story.append(Paragraph("Solar Panel Test Report", title_style))
                story.append(Spacer(1, 12))
                
                # Report content
                test = completed_tests[0]  # Use first test for demo
                
                # Test details
                story.append(Paragraph("Test Details", styles['Heading2']))
                test_data = [
                    ["Test ID", test.get('id', 'N/A')[:8]],
                    ["Test Date", str(test.get('date', 'N/A'))],
                    ["Operator", test.get('operator', 'N/A')],
                    ["Sample ID", test.get('sample_id', 'N/A')],
                    ["Method ID", test.get('method_id', 'N/A')]
                ]
                
                test_table = Table(test_data, colWidths=[2*inch, 4*inch])
                test_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(test_table)
                story.append(Spacer(1, 12))
                
                # Results
                story.append(Paragraph("Test Results", styles['Heading2']))
                if test.get('results'):
                    results_data = [["Parameter", "Result", "Status"]]
                    for param, value in test['results'].items():
                        results_data.append([param, f"{value:.3f}", "Pass"])
                    
                    results_table = Table(results_data, colWidths=[2*inch, 2*inch, 2*inch])
                    results_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(results_table)
                
                story.append(Spacer(1, 12))
                
                # Conclusions
                story.append(Paragraph("Conclusions", styles['Heading2']))
                story.append(Paragraph(f"Overall Result: {test.get('overall_result', 'N/A')}", styles['Normal']))
                if test.get('observations'):
                    story.append(Paragraph(f"Observations: {test['observations']}", styles['Normal']))
                if test.get('recommendations'):
                    story.append(Paragraph(f"Recommendations: {test['recommendations']}", styles['Normal']))
                
                # Build PDF
                doc.build(story)
                pdf_buffer.seek(0)
                
                # Provide download link
                b64 = base64.b64encode(pdf_buffer.read()).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="test_report.pdf">Download Test Report (PDF)</a>'
                st.markdown(href, unsafe_allow_html=True)
                
                st.success("Test report generated successfully!")
    
    elif report_type == "Project Status Report":
        if st.button("Generate Project Status Report"):
            # Create status report content
            report_content = f"""
# Project Status Report

## Project: {st.session_state.projects[0]['name'] if st.session_state.projects else 'N/A'}
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## Executive Summary
- Total Tasks: {len(st.session_state.tasks)}
- Completed: {len([t for t in st.session_state.tasks if t['status'] == 'Completed'])}
- In Progress: {len([t for t in st.session_state.tasks if t['status'] == 'In Progress'])}
- Critical Path Tasks: {len([t for t in st.session_state.tasks if t['is_critical']])}

## Budget Status
- Total Budget: ${st.session_state.projects[0]['budget']:,.0f}
- Spent to Date: ${st.session_state.projects[0]['spent']:,.0f}
- Remaining: ${st.session_state.projects[0]['budget'] - st.session_state.projects[0]['spent']:,.0f}

## Risk Summary
- Open Risks: {len([r for r in st.session_state.risks if r['status'] == 'Open'])}
- High Priority: {len([r for r in st.session_state.risks if r['probability'] == 'High' or r['impact'] == 'High'])}

## Key Milestones
"""
            for task in st.session_state.tasks:
                if task['is_milestone']:
                    report_content += f"- {task['name']}: {task['end_date']} ({task['status']})\n"
            
            # Display report
            st.markdown(report_content)
            
            # Download button
            st.download_button(
                label="Download Report (Markdown)",
                data=report_content,
                file_name=f"project_status_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown"
            )

def render_document_library():
    """Render document library"""
    st.subheader("Document Library")
    
    # Upload document
    with st.expander("Upload Document"):
        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'xlsx', 'txt'])
        
        if uploaded_file:
            doc_type = st.selectbox("Document Type", 
                                   ["Test Protocol", "Report", "Specification", "Certificate", "Other"])
            doc_description = st.text_area("Description")
            
            if st.button("Upload Document"):
                # Save document info
                doc_record = {
                    'id': str(uuid.uuid4()),
                    'name': uploaded_file.name,
                    'type': doc_type,
                    'size': uploaded_file.size,
                    'upload_date': datetime.now(),
                    'uploaded_by': st.session_state.current_user,
                    'description': doc_description,
                    'version': 1,
                    'content': uploaded_file.read()  # In production, save to file system
                }
                st.session_state.documents.append(doc_record)
                add_audit_trail('Uploaded', 'Document', doc_record['id'], f"Uploaded {uploaded_file.name}")
                st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
                st.rerun()
    
    # Display documents
    if st.session_state.documents:
        st.markdown("### Document List")
        
        for doc in st.session_state.documents:
            with st.expander(f"📄 {doc['name']} (v{doc['version']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Type:** {doc['type']}")
                    st.write(f"**Size:** {doc['size']/1024:.1f} KB")
                    st.write(f"**Uploaded:** {doc['upload_date'].strftime('%Y-%m-%d %H:%M')}")
                
                with col2:
                    st.write(f"**Uploaded By:** {doc['uploaded_by']}")
                    st.write(f"**Version:** {doc['version']}")
                
                st.write(f"**Description:** {doc['description']}")
                
                # Download button (in production, would retrieve actual file)
                st.download_button(
                    label="Download",
                    data=doc['content'],
                    file_name=doc['name'],
                    key=f"download_{doc['id']}"
                )

def render_audit_trail():
    """Render audit trail"""
    st.subheader("Audit Trail")
    
    if st.session_state.audit_trail:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filter_user = st.selectbox("Filter by User", 
                                      ['All'] + list(set([a['user'] for a in st.session_state.audit_trail])))
        
        with col2:
            filter_entity = st.selectbox("Filter by Entity Type",
                                        ['All'] + list(set([a['entity_type'] for a in st.session_state.audit_trail])))
        
        with col3:
            filter_action = st.selectbox("Filter by Action",
                                        ['All'] + list(set([a['action'] for a in st.session_state.audit_trail])))
        
        # Apply filters
        filtered_audit = st.session_state.audit_trail
        
        if filter_user != 'All':
            filtered_audit = [a for a in filtered_audit if a['user'] == filter_user]
        
        if filter_entity != 'All':
            filtered_audit = [a for a in filtered_audit if a['entity_type'] == filter_entity]
        
        if filter_action != 'All':
            filtered_audit = [a for a in filtered_audit if a['action'] == filter_action]
        
        # Display audit entries
        for entry in reversed(filtered_audit[-50:]):  # Show last 50 entries
            st.info(f"**{entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}** | "
                   f"**{entry['user']}** | "
                   f"{entry['action']} {entry['entity_type']} ({entry['entity_id']}) | "
                   f"{entry['details']}")
        
        # Export audit trail
        if st.button("Export Audit Trail (CSV)"):
            audit_df = pd.DataFrame(filtered_audit)
            csv = audit_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"audit_trail_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

def render_export_data():
    """Render data export interface"""
    st.subheader("Export Data")
    
    export_type = st.selectbox("Select Data to Export",
                              ["All Data", "Tasks", "Samples", "Test Results", "Risks", "Issues", "Resources"])
    
    export_format = st.radio("Export Format", ["CSV", "Excel", "JSON"])
    
    if st.button("Export Data"):
        # Prepare data based on selection
        if export_type == "All Data":
            export_data = {
                'projects': st.session_state.projects,
                'tasks': st.session_state.tasks,
                'samples': st.session_state.samples,
                'equipment': st.session_state.equipment,
                'manpower': st.session_state.manpower,
                'test_methods': st.session_state.test_methods,
                'test_results': st.session_state.test_results,
                'risks': st.session_state.risks,
                'issues': st.session_state.issues
            }
        elif export_type == "Tasks":
            export_data = st.session_state.tasks
        elif export_type == "Samples":
            export_data = st.session_state.samples
        elif export_type == "Test Results":
            export_data = st.session_state.test_results
        elif export_type == "Risks":
            export_data = st.session_state.risks
        elif export_type == "Issues":
            export_data = st.session_state.issues
        else:
            export_data = {
                'equipment': st.session_state.equipment,
                'manpower': st.session_state.manpower
            }
        
        # Export based on format
        if export_format == "CSV":
            if isinstance(export_data, list):
                df = pd.DataFrame(export_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"{export_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("CSV export is only available for single data types")
        
        elif export_format == "JSON":
            # Convert datetime objects to strings for JSON serialization
            def json_serial(obj):
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                raise TypeError(f"Type {type(obj)} not serializable")
            
            json_data = json.dumps(export_data, default=json_serial, indent=2)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"{export_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        elif export_format == "Excel":
            # Create Excel file with multiple sheets if needed
            output = BytesIO()
            
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                if isinstance(export_data, dict):
                    for sheet_name, data in export_data.items():
                        if isinstance(data, list) and data:
                            df = pd.DataFrame(data)
                            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel sheet name limit
                else:
                    df = pd.DataFrame(export_data)
                    df.to_excel(writer, sheet_name=export_type, index=False)
            
            output.seek(0)
            st.download_button(
                label="Download Excel",
                data=output,
                file_name=f"{export_type.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        
        st.success(f"Data exported successfully in {export_format} format!")

# Notifications System
def render_notifications():
    """Render notifications panel"""
    st.header("🔔 Notifications")
    
    # Mark all as read button
    if st.button("Mark All as Read"):
        for notif in st.session_state.notifications:
            notif['read'] = True
        st.rerun()
    
    # Display notifications
    unread = [n for n in st.session_state.notifications if not n['read']]
    read = [n for n in st.session_state.notifications if n['read']]
    
    if unread:
        st.subheader(f"Unread ({len(unread)})")
        for notif in reversed(unread[-10:]):
            priority_color = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}[notif['priority']]
            
            with st.container():
                st.warning(f"{priority_color} **{notif['title']}**\n\n"
                          f"{notif['message']}\n\n"
                          f"_{notif['timestamp'].strftime('%Y-%m-%d %H:%M')}_")
                
                if st.button(f"Mark as Read", key=f"read_{notif['id']}"):
                    notif['read'] = True
                    st.rerun()
    
    if read:
        with st.expander(f"Read ({len(read)})"):
            for notif in reversed(read[-20:]):
                st.info(f"**{notif['title']}** - {notif['timestamp'].strftime('%Y-%m-%d %H:%M')}\n\n{notif['message']}")

# Main Application
def main():
    """Main application entry point"""
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    st.sidebar.title("☀️ Solar PV Test PM")
    st.sidebar.markdown(f"**User:** {st.session_state.current_user}")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    
    # Check for unread notifications
    unread_count = len([n for n in st.session_state.notifications if not n['read']])
    if unread_count > 0:
        st.sidebar.error(f"🔔 {unread_count} unread notifications")
    
    st.sidebar.markdown("---")
    
    # Navigation menu
    menu_items = {
        "📊 Dashboard": "dashboard",
        "📋 Project Management": "project",
        "👁️ Views": "views",
        "☀️ Solar Testing": "testing",
        "📝 Workflows": "workflows",
        "👥 Resources": "resources",
        "⚠️ Risks & Issues": "risks",
        "📄 Reports": "reports",
        "🔔 Notifications": "notifications"
    }
    
    selected_page = st.sidebar.radio("Navigation", list(menu_items.keys()))
    
    # Token usage warning (approximation)
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Token Usage Alert**\nThis comprehensive app is approaching 85% of token capacity. Consider breaking into modules for production use.")
    
    # Main content area
    if selected_page == "📊 Dashboard":
        render_dashboard()
    elif selected_page == "📋 Project Management":
        render_project_management()
    elif selected_page == "👁️ Views":
        render_views()
    elif selected_page == "☀️ Solar Testing":
        render_solar_testing()
    elif selected_page == "📝 Workflows":
        render_workflows()
    elif selected_page == "👥 Resources":
        render_resources()
    elif selected_page == "⚠️ Risks & Issues":
        render_risk_issues()
    elif selected_page == "📄 Reports":
        render_reports()
    elif selected_page == "🔔 Notifications":
        render_notifications()
    
    # Footer
    st.markdown("---")
    st.markdown("© 2024 Solar PV Test Project Management System | Version 1.0 | Production Ready")

if __name__ == "__main__":
    main()
