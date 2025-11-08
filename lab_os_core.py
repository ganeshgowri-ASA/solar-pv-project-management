"""
SOLAR PV TESTING LAB ORGANISATION OS - CORE FRAMEWORK
MODULE_ID: CORE_LAB_OS_SESSION1
Version: 1.0.0
Created: 2025-11-08

OBJECTIVE: Complete foundational framework for Solar PV Testing Lab Organisation OS
solving real-world problems for 5-10 year old labs.

TARGET PROBLEMS SOLVED:
- High manpower costs → Automation
- Long TAT (Turnaround Time) → Efficiency tracking
- Manual errors → AI validation & automated checks
- Scaling difficulties → Modular architecture
- Brand reputation risks → Quality assurance & audit trails

TECH STACK:
- Frontend: Streamlit
- Data: pandas, numpy
- Visualization: plotly, altair
- State: st.session_state
"""

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
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

MODULE_ID = "CORE_LAB_OS_SESSION1"
VERSION = "1.0.0"

# User Roles with Hierarchical Permissions
USER_ROLES = {
    'Super Admin': {
        'level': 6,
        'permissions': ['all'],
        'description': 'Full system access, organization management'
    },
    'Lab Manager': {
        'level': 5,
        'permissions': ['manage_tests', 'manage_staff', 'manage_equipment', 'view_reports', 'approve_reports'],
        'description': 'Manages lab operations and resources'
    },
    'QA Manager': {
        'level': 4,
        'permissions': ['review_tests', 'approve_reports', 'view_reports', 'manage_quality'],
        'description': 'Quality assurance and report approval'
    },
    'Senior Technician': {
        'level': 3,
        'permissions': ['conduct_tests', 'view_tests', 'create_reports', 'manage_samples'],
        'description': 'Conducts tests and creates reports'
    },
    'Technician': {
        'level': 2,
        'permissions': ['conduct_tests', 'view_tests', 'manage_samples'],
        'description': 'Conducts tests under supervision'
    },
    'Client User': {
        'level': 1,
        'permissions': ['view_own_reports', 'submit_requests'],
        'description': 'Limited access to own test results'
    }
}

# Test Standards for Solar PV
TEST_STANDARDS = {
    'IEC 61215': 'Crystalline Silicon Terrestrial PV Modules - Design Qualification',
    'IEC 61730': 'PV Module Safety Qualification',
    'IEC 61701': 'Salt Mist Corrosion Testing',
    'IEC 62716': 'Ammonia Corrosion Testing',
    'UL 1703': 'Flat-Plate Photovoltaic Modules and Panels',
    'IEEE 1547': 'Interconnection and Interoperability',
    'ASTM E948': 'Electrical Performance of PV Cells',
    'ISO 9001': 'Quality Management System',
    'ISO 17025': 'Testing and Calibration Laboratories'
}

# Equipment Categories
EQUIPMENT_CATEGORIES = [
    'Solar Simulator',
    'Environmental Chamber',
    'Insulation Tester',
    'Thermal Imaging Camera',
    'Multimeter/Data Logger',
    'UV Exposure Unit',
    'Mechanical Testing Equipment',
    'Safety Testing Equipment',
    'Calibration Equipment'
]

# Test Types
TEST_TYPES = [
    'Performance Testing',
    'Safety Testing',
    'Environmental Testing',
    'Mechanical Testing',
    'Electrical Testing',
    'Thermal Testing',
    'UV Testing',
    'Salt Mist Testing',
    'Humidity Freeze Testing',
    'Hail Impact Testing'
]

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_lab_os_session_state():
    """
    Initialize all session state variables for Lab OS
    Centralized state management with caching for performance
    """
    defaults = {
        # Organization & Lab Setup
        'lab_organization': None,
        'lab_branches': [],
        'lab_clients': [],
        'lab_capacity_config': {},

        # User Management
        'lab_users': [],
        'current_lab_user': None,
        'user_sessions': [],
        'user_audit_trail': [],

        # Dashboard Data
        'active_tests': [],
        'pending_reports': [],
        'completed_tests': [],
        'tat_metrics': {},
        'equipment_utilization': {},
        'revenue_metrics': {},
        'client_satisfaction_scores': [],

        # Equipment & Resources
        'lab_equipment': [],
        'equipment_maintenance': [],
        'equipment_calibration': [],
        'equipment_bookings': [],

        # Staff & Manpower
        'lab_staff': [],
        'staff_certifications': [],
        'staff_availability': [],
        'staff_workload': [],

        # Test Records
        'test_records': [],
        'test_samples': [],
        'test_protocols': [],
        'test_results': [],

        # Reports & Documents
        'test_reports': [],
        'certificates': [],
        'report_templates': [],

        # Alerts & Notifications
        'lab_alerts': [],
        'maintenance_alerts': [],
        'calibration_alerts': [],
        'tat_alerts': [],

        # System Settings
        'lab_os_initialized': False,
        'current_view': 'Dashboard',
        'breadcrumb': [],
        'search_index': {},
        'theme': 'solar_green'
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# ============================================================================
# SAMPLE DATA GENERATION (5-10 YEAR OLD LAB)
# ============================================================================

def generate_sample_lab_organization():
    """Generate sample organization profile for a mature lab (5-10 years old)"""
    return {
        'org_id': 'ORG-SPV-001',
        'lab_name': 'SolarTech Testing & Certification Laboratory',
        'established_date': '2015-03-15',
        'address': {
            'street': '123 Innovation Drive',
            'city': 'Bangalore',
            'state': 'Karnataka',
            'country': 'India',
            'pincode': '560100'
        },
        'contact': {
            'phone': '+91-80-12345678',
            'email': 'info@solartechlab.com',
            'website': 'www.solartechlab.com'
        },
        'accreditations': [
            {'type': 'NABL', 'cert_no': 'TC-8756', 'valid_until': '2026-12-31', 'scope': 'Solar PV Testing'},
            {'type': 'ISO 17025', 'cert_no': 'ISO-17025-2023', 'valid_until': '2026-06-30', 'scope': 'Testing & Calibration'},
            {'type': 'ISO 9001', 'cert_no': 'ISO-9001-2022', 'valid_until': '2025-12-31', 'scope': 'Quality Management'}
        ],
        'lab_capacity': {
            'max_concurrent_tests': 25,
            'avg_monthly_throughput': 80,
            'staff_count': 15,
            'equipment_count': 32,
            'floor_area_sqm': 2500
        },
        'operating_hours': {
            'weekdays': '09:00-18:00',
            'saturday': '09:00-14:00',
            'sunday': 'Closed'
        },
        'revenue_annual': 15000000,  # INR 1.5 Crores
        'clients_served_total': 150,
        'tests_completed_total': 2800
    }

def generate_sample_branches():
    """Generate sample branch locations"""
    return [
        {
            'branch_id': 'BR-001',
            'branch_name': 'Main Laboratory - Bangalore',
            'location': 'Bangalore, Karnataka',
            'type': 'Headquarters',
            'established': '2015-03-15',
            'staff_count': 10,
            'active': True
        },
        {
            'branch_id': 'BR-002',
            'branch_name': 'Regional Lab - Chennai',
            'location': 'Chennai, Tamil Nadu',
            'type': 'Regional',
            'established': '2018-08-20',
            'staff_count': 5,
            'active': True
        }
    ]

def generate_sample_clients(count=20):
    """Generate realistic client data"""
    client_types = ['Manufacturer', 'Distributor', 'EPC Contractor', 'Developer', 'Utility']
    locations = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Ahmedabad']

    clients = []
    base_date = datetime.now() - timedelta(days=1800)  # ~5 years ago

    for i in range(count):
        onboard_date = base_date + timedelta(days=np.random.randint(0, 1500))
        clients.append({
            'client_id': f'CLT-{str(i+1).zfill(4)}',
            'client_name': f'{np.random.choice(["Solar", "Green", "Sun", "Eco", "Power"])} {np.random.choice(["Tech", "Energy", "Systems", "Solutions", "Industries"])} Pvt Ltd',
            'client_type': np.random.choice(client_types),
            'location': np.random.choice(locations),
            'onboarding_date': onboard_date.strftime('%Y-%m-%d'),
            'contact_person': f'Contact Person {i+1}',
            'email': f'contact{i+1}@client.com',
            'phone': f'+91-{np.random.randint(70,99)}{np.random.randint(10000000,99999999)}',
            'total_tests_ordered': np.random.randint(5, 150),
            'active': np.random.choice([True, True, True, False]),  # 75% active
            'satisfaction_score': round(np.random.uniform(3.5, 5.0), 1),
            'payment_terms': np.random.choice(['30 days', '45 days', '60 days', 'Advance']),
            'outstanding_amount': np.random.randint(0, 500000)
        })

    return clients

def generate_sample_equipment(count=10):
    """Generate realistic equipment data"""
    base_date = datetime.now()

    equipment_list = []
    for i in range(count):
        purchase_date = base_date - timedelta(days=np.random.randint(365, 3650))  # 1-10 years old
        last_calibration = base_date - timedelta(days=np.random.randint(30, 365))
        next_calibration = last_calibration + timedelta(days=365)

        category = np.random.choice(EQUIPMENT_CATEGORIES)

        equipment_list.append({
            'equipment_id': f'EQ-{str(i+1).zfill(4)}',
            'equipment_name': f'{category} {np.random.choice(["Pro", "Plus", "Advanced", "Elite"])}',
            'category': category,
            'manufacturer': np.random.choice(['Spire', 'Pasan', 'Meyer Burger', 'Newport', 'Halm']),
            'model': f'Model-{np.random.randint(100,999)}',
            'serial_number': f'SN{np.random.randint(100000,999999)}',
            'purchase_date': purchase_date.strftime('%Y-%m-%d'),
            'purchase_cost': np.random.randint(500000, 15000000),
            'status': np.random.choice(['Available', 'Available', 'Available', 'In Use', 'Under Maintenance']),
            'location': np.random.choice(['Main Lab', 'Environmental Testing Hall', 'Electrical Testing Room']),
            'last_calibration_date': last_calibration.strftime('%Y-%m-%d'),
            'next_calibration_date': next_calibration.strftime('%Y-%m-%d'),
            'calibration_frequency_days': 365,
            'utilization_hours_total': np.random.randint(1000, 15000),
            'maintenance_cost_annual': np.random.randint(50000, 500000),
            'downtime_hours_ytd': np.random.randint(10, 200)
        })

    return equipment_list

def generate_sample_staff(count=15):
    """Generate realistic staff data"""
    roles = list(USER_ROLES.keys())
    qualifications = ['B.Tech', 'M.Tech', 'Diploma', 'B.Sc', 'M.Sc', 'PhD']
    specializations = ['Electrical', 'Electronics', 'Renewable Energy', 'Materials Science', 'Mechanical']

    staff_list = []
    base_date = datetime.now()

    for i in range(count):
        join_date = base_date - timedelta(days=np.random.randint(180, 3650))  # 6 months to 10 years

        # Role distribution (realistic hierarchy)
        if i == 0:
            role = 'Super Admin'
        elif i < 2:
            role = 'Lab Manager'
        elif i < 4:
            role = 'QA Manager'
        elif i < 8:
            role = 'Senior Technician'
        else:
            role = 'Technician'

        staff_list.append({
            'staff_id': f'STF-{str(i+1).zfill(4)}',
            'name': f'{np.random.choice(["Rajesh", "Priya", "Amit", "Sneha", "Vijay", "Anita", "Suresh", "Kavita"])} {np.random.choice(["Kumar", "Sharma", "Patel", "Singh", "Reddy", "Nair"])}',
            'role': role,
            'qualification': np.random.choice(qualifications),
            'specialization': np.random.choice(specializations),
            'join_date': join_date.strftime('%Y-%m-%d'),
            'experience_years': round((base_date - join_date).days / 365, 1),
            'email': f'staff{i+1}@solartechlab.com',
            'phone': f'+91-{np.random.randint(70,99)}{np.random.randint(10000000,99999999)}',
            'certifications': np.random.randint(1, 5),
            'active_tests': np.random.randint(0, 5),
            'tests_completed_ytd': np.random.randint(10, 200),
            'performance_rating': round(np.random.uniform(3.5, 5.0), 1),
            'available': np.random.choice([True, True, True, False])
        })

    return staff_list

def generate_sample_test_records(count=50):
    """Generate realistic historical test records (past 3 years)"""
    test_records = []
    base_date = datetime.now()

    for i in range(count):
        start_date = base_date - timedelta(days=np.random.randint(30, 1095))  # Last 3 years
        duration_days = np.random.randint(7, 45)
        end_date = start_date + timedelta(days=duration_days)

        status = np.random.choice([
            'Completed', 'Completed', 'Completed', 'Completed',
            'In Progress', 'Pending Report', 'Under Review'
        ])

        tat_target = 30
        tat_actual = duration_days
        tat_status = 'On Time' if tat_actual <= tat_target else 'Delayed'

        test_records.append({
            'test_id': f'TST-{str(i+1).zfill(5)}',
            'client_id': f'CLT-{str(np.random.randint(1,21)).zfill(4)}',
            'sample_id': f'SPL-{str(i+1).zfill(5)}',
            'test_type': np.random.choice(TEST_TYPES),
            'standard': np.random.choice(list(TEST_STANDARDS.keys())),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'target_end_date': (start_date + timedelta(days=tat_target)).strftime('%Y-%m-%d'),
            'actual_end_date': end_date.strftime('%Y-%m-%d') if status == 'Completed' else None,
            'status': status,
            'tat_target_days': tat_target,
            'tat_actual_days': tat_actual if status == 'Completed' else None,
            'tat_status': tat_status if status == 'Completed' else 'In Progress',
            'assigned_technician': f'STF-{str(np.random.randint(1,16)).zfill(4)}',
            'equipment_used': f'EQ-{str(np.random.randint(1,11)).zfill(4)}',
            'test_result': np.random.choice(['Pass', 'Pass', 'Pass', 'Fail', 'Conditional Pass']) if status == 'Completed' else None,
            'revenue': np.random.randint(50000, 500000),
            'priority': np.random.choice(['High', 'Medium', 'Low']),
            'report_status': np.random.choice(['Draft', 'Under Review', 'Approved', 'Issued']) if status == 'Completed' else 'Not Started'
        })

    return test_records

def initialize_sample_data():
    """Initialize all sample data for a 5-10 year old lab"""
    if not st.session_state.lab_os_initialized:
        st.session_state.lab_organization = generate_sample_lab_organization()
        st.session_state.lab_branches = generate_sample_branches()
        st.session_state.lab_clients = generate_sample_clients(20)
        st.session_state.lab_equipment = generate_sample_equipment(10)
        st.session_state.lab_staff = generate_sample_staff(15)
        st.session_state.test_records = generate_sample_test_records(50)

        # Set default user
        if st.session_state.lab_staff:
            st.session_state.current_lab_user = st.session_state.lab_staff[0]  # Super Admin

        st.session_state.lab_os_initialized = True

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def calculate_tat_metrics():
    """Calculate Turn-Around Time metrics"""
    if not st.session_state.test_records:
        return {
            'avg_tat_days': 0,
            'on_time_percentage': 0,
            'delayed_count': 0,
            'avg_delay_days': 0
        }

    df = pd.DataFrame(st.session_state.test_records)
    completed = df[df['status'] == 'Completed']

    if len(completed) == 0:
        return {
            'avg_tat_days': 0,
            'on_time_percentage': 0,
            'delayed_count': 0,
            'avg_delay_days': 0
        }

    avg_tat = completed['tat_actual_days'].mean()
    on_time_count = len(completed[completed['tat_status'] == 'On Time'])
    on_time_pct = (on_time_count / len(completed)) * 100
    delayed = completed[completed['tat_status'] == 'Delayed']
    delayed_count = len(delayed)
    avg_delay = (delayed['tat_actual_days'] - delayed['tat_target_days']).mean() if delayed_count > 0 else 0

    return {
        'avg_tat_days': round(avg_tat, 1),
        'on_time_percentage': round(on_time_pct, 1),
        'delayed_count': delayed_count,
        'avg_delay_days': round(avg_delay, 1) if avg_delay > 0 else 0
    }

def calculate_equipment_utilization():
    """Calculate equipment utilization metrics"""
    if not st.session_state.lab_equipment:
        return {}

    utilization = {}
    for eq in st.session_state.lab_equipment:
        # Calculate utilization percentage (assuming 2000 hours/year as 100%)
        total_hours = eq['utilization_hours_total']
        years_old = (datetime.now() - datetime.strptime(eq['purchase_date'], '%Y-%m-%d')).days / 365
        expected_hours = years_old * 2000
        util_pct = (total_hours / expected_hours * 100) if expected_hours > 0 else 0

        utilization[eq['equipment_id']] = {
            'name': eq['equipment_name'],
            'utilization_pct': min(round(util_pct, 1), 100),
            'status': eq['status'],
            'downtime_hours': eq['downtime_hours_ytd']
        }

    return utilization

def calculate_revenue_metrics():
    """Calculate revenue metrics"""
    if not st.session_state.test_records:
        return {
            'daily': 0,
            'monthly': 0,
            'ytd': 0,
            'trend': []
        }

    df = pd.DataFrame(st.session_state.test_records)
    completed = df[df['status'] == 'Completed'].copy()

    if len(completed) == 0:
        return {'daily': 0, 'monthly': 0, 'ytd': 0, 'trend': []}

    completed['end_date'] = pd.to_datetime(completed['actual_end_date'])

    # Daily revenue (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent = completed[completed['end_date'] >= thirty_days_ago]
    daily_avg = recent['revenue'].sum() / 30 if len(recent) > 0 else 0

    # Monthly revenue (current month)
    current_month = datetime.now().month
    current_year = datetime.now().year
    monthly = completed[
        (completed['end_date'].dt.month == current_month) &
        (completed['end_date'].dt.year == current_year)
    ]['revenue'].sum()

    # YTD revenue
    ytd = completed[completed['end_date'].dt.year == current_year]['revenue'].sum()

    return {
        'daily': round(daily_avg, 2),
        'monthly': monthly,
        'ytd': ytd,
        'trend': []  # Can be expanded with monthly trend data
    }

def get_active_alerts():
    """Get all active alerts"""
    alerts = []

    # Check for overdue tests
    if st.session_state.test_records:
        df = pd.DataFrame(st.session_state.test_records)
        in_progress = df[df['status'].isin(['In Progress', 'Pending Report'])]
        for _, test in in_progress.iterrows():
            target_date = datetime.strptime(test['target_end_date'], '%Y-%m-%d')
            if target_date < datetime.now():
                days_overdue = (datetime.now() - target_date).days
                alerts.append({
                    'type': 'Overdue Test',
                    'severity': 'High',
                    'message': f"Test {test['test_id']} is {days_overdue} days overdue",
                    'test_id': test['test_id']
                })

    # Check for equipment calibration due
    if st.session_state.lab_equipment:
        for eq in st.session_state.lab_equipment:
            next_cal = datetime.strptime(eq['next_calibration_date'], '%Y-%m-%d')
            days_until = (next_cal - datetime.now()).days
            if days_until < 30:
                alerts.append({
                    'type': 'Calibration Due',
                    'severity': 'Medium' if days_until > 7 else 'High',
                    'message': f"{eq['equipment_name']} calibration due in {days_until} days",
                    'equipment_id': eq['equipment_id']
                })

    # Check for staff certification expiry (if data available)
    # Can be expanded

    return alerts

def check_user_permission(permission):
    """Check if current user has a specific permission"""
    if not st.session_state.current_lab_user:
        return False

    user_role = st.session_state.current_lab_user.get('role', 'Client User')
    role_permissions = USER_ROLES.get(user_role, {}).get('permissions', [])

    if 'all' in role_permissions:
        return True

    return permission in role_permissions

# ============================================================================
# DASHBOARD COMPONENTS
# ============================================================================

def render_kpi_metrics():
    """Render real-time KPI metrics"""
    st.subheader("📊 Real-Time KPIs")

    # Calculate metrics
    active_tests_count = len([t for t in st.session_state.test_records if t['status'] in ['In Progress', 'Pending Report']])
    pending_reports_count = len([t for t in st.session_state.test_records if t['report_status'] in ['Draft', 'Under Review']])
    tat_metrics = calculate_tat_metrics()
    revenue = calculate_revenue_metrics()

    # Display metrics in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Active Tests",
            value=active_tests_count,
            delta=f"{len([t for t in st.session_state.test_records if t['status'] == 'In Progress'])} in progress"
        )

    with col2:
        st.metric(
            label="Pending Reports",
            value=pending_reports_count,
            delta=f"{len([t for t in st.session_state.test_records if t['report_status'] == 'Draft'])} drafts"
        )

    with col3:
        st.metric(
            label="Avg TAT (days)",
            value=tat_metrics['avg_tat_days'],
            delta=f"{tat_metrics['on_time_percentage']}% on-time",
            delta_color="normal" if tat_metrics['on_time_percentage'] >= 80 else "inverse"
        )

    with col4:
        st.metric(
            label="Monthly Revenue",
            value=f"₹{revenue['monthly']:,.0f}",
            delta=f"₹{revenue['daily']:,.0f}/day"
        )

    with col5:
        alerts = get_active_alerts()
        high_severity = len([a for a in alerts if a['severity'] == 'High'])
        st.metric(
            label="Active Alerts",
            value=len(alerts),
            delta=f"{high_severity} high priority",
            delta_color="inverse" if high_severity > 0 else "off"
        )

def render_charts():
    """Render interactive Plotly charts"""
    st.subheader("📈 Analytics & Visualizations")

    tab1, tab2, tab3, tab4 = st.tabs(["Test Overview", "Equipment Utilization", "Revenue Trends", "TAT Analysis"])

    with tab1:
        render_test_overview_chart()

    with tab2:
        render_equipment_utilization_chart()

    with tab3:
        render_revenue_trends_chart()

    with tab4:
        render_tat_analysis_chart()

def render_test_overview_chart():
    """Render test overview chart"""
    if not st.session_state.test_records:
        st.info("No test data available")
        return

    df = pd.DataFrame(st.session_state.test_records)

    # Test status distribution
    col1, col2 = st.columns(2)

    with col1:
        status_counts = df['status'].value_counts()
        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Test Status Distribution",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        test_type_counts = df['test_type'].value_counts().head(8)
        fig = px.bar(
            x=test_type_counts.values,
            y=test_type_counts.index,
            orientation='h',
            title="Top Test Types",
            labels={'x': 'Count', 'y': 'Test Type'},
            color=test_type_counts.values,
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

def render_equipment_utilization_chart():
    """Render equipment utilization chart"""
    if not st.session_state.lab_equipment:
        st.info("No equipment data available")
        return

    utilization = calculate_equipment_utilization()

    if not utilization:
        st.info("No utilization data available")
        return

    # Prepare data
    eq_names = [v['name'] for v in utilization.values()]
    util_pcts = [v['utilization_pct'] for v in utilization.values()]
    statuses = [v['status'] for v in utilization.values()]

    # Create bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=eq_names,
        y=util_pcts,
        text=[f"{u}%" for u in util_pcts],
        textposition='auto',
        marker=dict(
            color=util_pcts,
            colorscale='RdYlGn',
            cmin=0,
            cmax=100,
            showscale=True,
            colorbar=dict(title="Utilization %")
        ),
        hovertemplate='<b>%{x}</b><br>Utilization: %{y}%<extra></extra>'
    ))

    fig.update_layout(
        title="Equipment Utilization",
        xaxis_title="Equipment",
        yaxis_title="Utilization %",
        yaxis=dict(range=[0, 100]),
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Equipment status summary
    col1, col2, col3 = st.columns(3)
    available = len([s for s in statuses if s == 'Available'])
    in_use = len([s for s in statuses if s == 'In Use'])
    maintenance = len([s for s in statuses if s == 'Under Maintenance'])

    with col1:
        st.metric("Available", available, f"{available/len(statuses)*100:.0f}%")
    with col2:
        st.metric("In Use", in_use, f"{in_use/len(statuses)*100:.0f}%")
    with col3:
        st.metric("Maintenance", maintenance, f"{maintenance/len(statuses)*100:.0f}%")

def render_revenue_trends_chart():
    """Render revenue trends chart"""
    if not st.session_state.test_records:
        st.info("No revenue data available")
        return

    df = pd.DataFrame(st.session_state.test_records)
    completed = df[df['status'] == 'Completed'].copy()

    if len(completed) == 0:
        st.info("No completed tests available")
        return

    completed['end_date'] = pd.to_datetime(completed['actual_end_date'])
    completed['month'] = completed['end_date'].dt.to_period('M').astype(str)

    # Monthly revenue
    monthly_revenue = completed.groupby('month')['revenue'].sum().reset_index()
    monthly_revenue = monthly_revenue.sort_values('month')

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=monthly_revenue['month'],
        y=monthly_revenue['revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='green', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(0,128,0,0.1)'
    ))

    fig.update_layout(
        title="Monthly Revenue Trend",
        xaxis_title="Month",
        yaxis_title="Revenue (₹)",
        hovermode='x unified',
        height=400
    )

    st.plotly_chart(fig, use_container_width=True)

    # Revenue by test type
    test_type_revenue = completed.groupby('test_type')['revenue'].sum().sort_values(ascending=False).head(8)

    fig2 = px.bar(
        x=test_type_revenue.index,
        y=test_type_revenue.values,
        title="Revenue by Test Type",
        labels={'x': 'Test Type', 'y': 'Revenue (₹)'},
        color=test_type_revenue.values,
        color_continuous_scale='Greens'
    )

    st.plotly_chart(fig2, use_container_width=True)

def render_tat_analysis_chart():
    """Render TAT analysis chart"""
    if not st.session_state.test_records:
        st.info("No TAT data available")
        return

    df = pd.DataFrame(st.session_state.test_records)
    completed = df[df['status'] == 'Completed'].copy()

    if len(completed) == 0:
        st.info("No completed tests available")
        return

    # TAT status distribution
    col1, col2 = st.columns(2)

    with col1:
        tat_status_counts = completed['tat_status'].value_counts()
        fig = px.pie(
            values=tat_status_counts.values,
            names=tat_status_counts.index,
            title="TAT Performance",
            hole=0.4,
            color_discrete_map={'On Time': 'green', 'Delayed': 'red'}
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # TAT distribution
        fig = px.histogram(
            completed,
            x='tat_actual_days',
            nbins=20,
            title="TAT Distribution",
            labels={'tat_actual_days': 'TAT (days)', 'count': 'Number of Tests'},
            color_discrete_sequence=['green']
        )
        fig.add_vline(x=30, line_dash="dash", line_color="red", annotation_text="Target (30 days)")
        st.plotly_chart(fig, use_container_width=True)

    # TAT by test type
    tat_by_type = completed.groupby('test_type')['tat_actual_days'].mean().sort_values(ascending=False).head(8)

    fig2 = px.bar(
        x=tat_by_type.index,
        y=tat_by_type.values,
        title="Average TAT by Test Type",
        labels={'x': 'Test Type', 'y': 'Average TAT (days)'},
        color=tat_by_type.values,
        color_continuous_scale='RdYlGn_r'
    )
    fig2.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Target")
    st.plotly_chart(fig2, use_container_width=True)

def render_alerts_panel():
    """Render alerts and notifications panel"""
    st.subheader("🔔 Alerts & Notifications")

    alerts = get_active_alerts()

    if not alerts:
        st.success("✅ No active alerts")
        return

    # Group by severity
    high_alerts = [a for a in alerts if a['severity'] == 'High']
    medium_alerts = [a for a in alerts if a['severity'] == 'Medium']

    if high_alerts:
        st.error(f"🚨 {len(high_alerts)} High Priority Alerts")
        for alert in high_alerts:
            st.warning(f"**{alert['type']}**: {alert['message']}")

    if medium_alerts:
        st.warning(f"⚠️ {len(medium_alerts)} Medium Priority Alerts")
        with st.expander("View Medium Priority Alerts"):
            for alert in medium_alerts:
                st.info(f"**{alert['type']}**: {alert['message']}")

def render_quick_actions():
    """Render quick action buttons"""
    st.subheader("⚡ Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🧪 Start New Test", use_container_width=True):
            st.session_state.current_view = "New Test"
            st.rerun()

    with col2:
        if st.button("📄 View Reports", use_container_width=True):
            st.session_state.current_view = "Reports"
            st.rerun()

    with col3:
        if st.button("👥 Manage Staff", use_container_width=True):
            st.session_state.current_view = "Staff Management"
            st.rerun()

    with col4:
        if st.button("🔧 Equipment Status", use_container_width=True):
            st.session_state.current_view = "Equipment"
            st.rerun()

# ============================================================================
# NAVIGATION FRAMEWORK
# ============================================================================

def render_sidebar_navigation():
    """Render sidebar navigation with role-based menu"""
    with st.sidebar:
        # Lab branding
        if st.session_state.lab_organization:
            st.title(st.session_state.lab_organization['lab_name'])
            st.caption(f"Est. {st.session_state.lab_organization['established_date']}")
            st.divider()

        # User info
        if st.session_state.current_lab_user:
            user = st.session_state.current_lab_user
            st.write(f"👤 **{user['name']}**")
            st.caption(f"Role: {user['role']}")
            st.divider()

        # Navigation menu
        st.subheader("📍 Navigation")

        menu_items = {
            "Dashboard": "📊",
            "Test Management": "🧪",
            "Client Management": "👥",
            "Equipment": "🔧",
            "Staff Management": "👨‍🔬",
            "Reports": "📄",
            "Analytics": "📈",
            "Settings": "⚙️"
        }

        for item, icon in menu_items.items():
            if st.button(f"{icon} {item}", key=f"nav_{item}", use_container_width=True):
                st.session_state.current_view = item
                st.rerun()

        st.divider()

        # System info
        st.caption(f"**Module:** {MODULE_ID}")
        st.caption(f"**Version:** {VERSION}")
        st.caption(f"**Users:** {len(st.session_state.lab_staff)}")
        st.caption(f"**Active Tests:** {len([t for t in st.session_state.test_records if t['status'] in ['In Progress']])}")

def render_breadcrumb():
    """Render breadcrumb navigation"""
    current_view = st.session_state.get('current_view', 'Dashboard')
    st.caption(f"🏠 Home / {current_view}")
    st.divider()

def render_global_search():
    """Render global search functionality"""
    search_query = st.text_input("🔍 Search", placeholder="Search tests, clients, equipment...")

    if search_query:
        # Simple search implementation
        results = []

        # Search in test records
        for test in st.session_state.test_records:
            if search_query.lower() in str(test.get('test_id', '')).lower():
                results.append(('Test', test['test_id'], test))

        # Search in clients
        for client in st.session_state.lab_clients:
            if search_query.lower() in client.get('client_name', '').lower():
                results.append(('Client', client['client_name'], client))

        # Search in equipment
        for eq in st.session_state.lab_equipment:
            if search_query.lower() in eq.get('equipment_name', '').lower():
                results.append(('Equipment', eq['equipment_name'], eq))

        if results:
            st.success(f"Found {len(results)} results")
            for result_type, result_name, result_data in results[:10]:
                st.write(f"**{result_type}**: {result_name}")
        else:
            st.info("No results found")

# ============================================================================
# MAIN VIEWS
# ============================================================================

def render_dashboard_view():
    """Render main dashboard view"""
    st.title("📊 Laboratory Dashboard")
    render_breadcrumb()

    # Quick search
    with st.expander("🔍 Quick Search", expanded=False):
        render_global_search()

    # KPI Metrics
    render_kpi_metrics()

    st.divider()

    # Charts
    render_charts()

    st.divider()

    # Alerts
    col1, col2 = st.columns([2, 1])

    with col1:
        render_alerts_panel()

    with col2:
        render_quick_actions()

def render_test_management_view():
    """Render test management view"""
    st.title("🧪 Test Management")
    render_breadcrumb()

    tab1, tab2, tab3 = st.tabs(["Active Tests", "Test History", "New Test"])

    with tab1:
        st.subheader("Active Tests")
        active_tests = [t for t in st.session_state.test_records if t['status'] in ['In Progress', 'Pending Report']]

        if active_tests:
            df = pd.DataFrame(active_tests)
            st.dataframe(
                df[['test_id', 'client_id', 'test_type', 'status', 'start_date', 'target_end_date', 'priority']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No active tests")

    with tab2:
        st.subheader("Test History")
        if st.session_state.test_records:
            df = pd.DataFrame(st.session_state.test_records)

            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                status_filter = st.multiselect("Status", df['status'].unique())
            with col2:
                test_type_filter = st.multiselect("Test Type", df['test_type'].unique())
            with col3:
                date_range = st.date_input("Date Range", [])

            # Apply filters
            filtered_df = df.copy()
            if status_filter:
                filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
            if test_type_filter:
                filtered_df = filtered_df[filtered_df['test_type'].isin(test_type_filter)]

            st.dataframe(
                filtered_df[['test_id', 'client_id', 'test_type', 'status', 'start_date', 'tat_actual_days', 'revenue']],
                use_container_width=True,
                hide_index=True
            )

            # Export
            if st.button("📥 Export to CSV"):
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="test_records.csv",
                    mime="text/csv"
                )
        else:
            st.info("No test records available")

    with tab3:
        st.subheader("Create New Test")
        st.info("New test creation form would go here")
        # Form implementation can be added

def render_client_management_view():
    """Render client management view"""
    st.title("👥 Client Management")
    render_breadcrumb()

    if not st.session_state.lab_clients:
        st.info("No clients available")
        return

    # Client summary
    col1, col2, col3, col4 = st.columns(4)
    total_clients = len(st.session_state.lab_clients)
    active_clients = len([c for c in st.session_state.lab_clients if c['active']])
    avg_satisfaction = np.mean([c['satisfaction_score'] for c in st.session_state.lab_clients])
    total_outstanding = sum([c['outstanding_amount'] for c in st.session_state.lab_clients])

    with col1:
        st.metric("Total Clients", total_clients)
    with col2:
        st.metric("Active Clients", active_clients)
    with col3:
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/5.0")
    with col4:
        st.metric("Outstanding", f"₹{total_outstanding:,.0f}")

    st.divider()

    # Client list
    df = pd.DataFrame(st.session_state.lab_clients)
    st.dataframe(
        df[['client_id', 'client_name', 'client_type', 'location', 'total_tests_ordered', 'satisfaction_score', 'active']],
        use_container_width=True,
        hide_index=True
    )

def render_equipment_view():
    """Render equipment management view"""
    st.title("🔧 Equipment Management")
    render_breadcrumb()

    if not st.session_state.lab_equipment:
        st.info("No equipment available")
        return

    # Equipment summary
    col1, col2, col3, col4 = st.columns(4)
    total_eq = len(st.session_state.lab_equipment)
    available_eq = len([e for e in st.session_state.lab_equipment if e['status'] == 'Available'])
    maintenance_eq = len([e for e in st.session_state.lab_equipment if e['status'] == 'Under Maintenance'])
    calibration_due = len([e for e in st.session_state.lab_equipment if (datetime.strptime(e['next_calibration_date'], '%Y-%m-%d') - datetime.now()).days < 30])

    with col1:
        st.metric("Total Equipment", total_eq)
    with col2:
        st.metric("Available", available_eq, f"{available_eq/total_eq*100:.0f}%")
    with col3:
        st.metric("Under Maintenance", maintenance_eq)
    with col4:
        st.metric("Calibration Due", calibration_due, delta_color="inverse" if calibration_due > 0 else "off")

    st.divider()

    # Equipment list
    df = pd.DataFrame(st.session_state.lab_equipment)
    st.dataframe(
        df[['equipment_id', 'equipment_name', 'category', 'status', 'location', 'next_calibration_date']],
        use_container_width=True,
        hide_index=True
    )

def render_staff_management_view():
    """Render staff management view"""
    st.title("👨‍🔬 Staff Management")
    render_breadcrumb()

    if not st.session_state.lab_staff:
        st.info("No staff data available")
        return

    # Staff summary
    col1, col2, col3, col4 = st.columns(4)
    total_staff = len(st.session_state.lab_staff)
    available_staff = len([s for s in st.session_state.lab_staff if s['available']])
    avg_rating = np.mean([s['performance_rating'] for s in st.session_state.lab_staff])
    active_tests_total = sum([s['active_tests'] for s in st.session_state.lab_staff])

    with col1:
        st.metric("Total Staff", total_staff)
    with col2:
        st.metric("Available", available_staff)
    with col3:
        st.metric("Avg Rating", f"{avg_rating:.1f}/5.0")
    with col4:
        st.metric("Active Tests", active_tests_total)

    st.divider()

    # Staff list
    df = pd.DataFrame(st.session_state.lab_staff)
    st.dataframe(
        df[['staff_id', 'name', 'role', 'qualification', 'experience_years', 'active_tests', 'performance_rating', 'available']],
        use_container_width=True,
        hide_index=True
    )

def render_reports_view():
    """Render reports view"""
    st.title("📄 Reports & Analytics")
    render_breadcrumb()

    st.info("Comprehensive reporting functionality will be implemented here")

    # Report types
    report_types = [
        "Monthly Performance Report",
        "Client Satisfaction Report",
        "Equipment Utilization Report",
        "Staff Productivity Report",
        "Revenue Analysis Report",
        "TAT Performance Report"
    ]

    selected_report = st.selectbox("Select Report Type", report_types)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    if st.button("Generate Report", type="primary"):
        st.success(f"Generating {selected_report}...")
        # Report generation logic would go here

def render_analytics_view():
    """Render analytics view"""
    st.title("📈 Advanced Analytics")
    render_breadcrumb()

    # Reuse dashboard charts
    render_charts()

def render_settings_view():
    """Render settings view"""
    st.title("⚙️ Settings")
    render_breadcrumb()

    tab1, tab2, tab3 = st.tabs(["Organization", "Users", "System"])

    with tab1:
        st.subheader("Organization Profile")
        if st.session_state.lab_organization:
            org = st.session_state.lab_organization
            st.write(f"**Lab Name:** {org['lab_name']}")
            st.write(f"**Established:** {org['established_date']}")
            st.write(f"**Location:** {org['address']['city']}, {org['address']['state']}")
            st.write(f"**Email:** {org['contact']['email']}")

            st.subheader("Accreditations")
            for acc in org['accreditations']:
                st.write(f"- **{acc['type']}**: {acc['cert_no']} (Valid until: {acc['valid_until']})")

    with tab2:
        st.subheader("User Roles & Permissions")
        for role, details in USER_ROLES.items():
            with st.expander(f"{role} (Level {details['level']})"):
                st.write(f"**Description:** {details['description']}")
                st.write(f"**Permissions:** {', '.join(details['permissions'])}")

    with tab3:
        st.subheader("System Information")
        st.write(f"**Module ID:** {MODULE_ID}")
        st.write(f"**Version:** {VERSION}")
        st.write(f"**Total Tests:** {len(st.session_state.test_records)}")
        st.write(f"**Total Clients:** {len(st.session_state.lab_clients)}")
        st.write(f"**Total Equipment:** {len(st.session_state.lab_equipment)}")
        st.write(f"**Total Staff:** {len(st.session_state.lab_staff)}")

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""

    # Initialize session state
    init_lab_os_session_state()

    # Initialize sample data
    initialize_sample_data()

    # Render navigation sidebar
    render_sidebar_navigation()

    # Render main content based on current view
    current_view = st.session_state.get('current_view', 'Dashboard')

    if current_view == 'Dashboard':
        render_dashboard_view()
    elif current_view == 'Test Management':
        render_test_management_view()
    elif current_view == 'Client Management':
        render_client_management_view()
    elif current_view == 'Equipment':
        render_equipment_view()
    elif current_view == 'Staff Management':
        render_staff_management_view()
    elif current_view == 'Reports':
        render_reports_view()
    elif current_view == 'Analytics':
        render_analytics_view()
    elif current_view == 'Settings':
        render_settings_view()
    else:
        render_dashboard_view()

if __name__ == "__main__":
    # Page Configuration
    st.set_page_config(
        page_title="Solar PV Lab OS",
        page_icon="☀️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for Professional Solar/Green Theme
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #2E7D32;
            --secondary-color: #66BB6A;
            --accent-color: #FFA726;
            --background-light: #F1F8F4;
        }

        /* Metric containers */
        div[data-testid="metric-container"] {
            background-color: #F1F8F4;
            border: 2px solid #66BB6A;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Headers */
        h1, h2, h3 {
            color: #2E7D32;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #F1F8F4;
            padding: 10px;
            border-radius: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
            background-color: white;
            border-radius: 5px;
            border: 1px solid #66BB6A;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #2E7D32;
            color: white;
        }

        /* Buttons */
        .stButton > button {
            background-color: #2E7D32;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 8px 16px;
            font-weight: 500;
        }

        .stButton > button:hover {
            background-color: #1B5E20;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #F1F8F4;
        }

        /* Dataframes */
        .dataframe {
            border: 2px solid #66BB6A !important;
            border-radius: 5px;
        }

        /* Alert boxes */
        .stAlert {
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Run main application
    main()
