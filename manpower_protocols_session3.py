"""
Solar PV Project Management - Manpower & Test Protocols Module
MODULE_ID: MANPOWER_PROTOCOLS_SESSION3

This module provides advanced manpower management and test methods/protocol system functionality.
Features:
- Staff registry with comprehensive tracking
- Performance metrics and workload analysis
- Availability calendar with shift management
- Test standards database (IEC-61215, IEC-61730, ISO)
- Protocol templates with auto-validation
- Test results tracking and compliance reporting
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import uuid

MODULE_ID = 'MANPOWER_PROTOCOLS_SESSION3'

# ============================================================================
# DATA INITIALIZATION & SAMPLE DATA
# ============================================================================

def initialize_manpower_protocols_data():
    """
    Initialize session state variables for manpower and test protocols.
    Creates sample data if not already present.
    """
    # Initialize staff registry
    if 'staff_registry' not in st.session_state:
        st.session_state.staff_registry = []

    # Initialize test standards/protocols
    if 'test_standards' not in st.session_state:
        st.session_state.test_standards = []

    # Initialize test protocols
    if 'test_protocols' not in st.session_state:
        st.session_state.test_protocols = []

    # Initialize test results
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []

    # Initialize staff assignments
    if 'staff_assignments' not in st.session_state:
        st.session_state.staff_assignments = []

    # Initialize holidays/shifts
    if 'staff_calendar_events' not in st.session_state:
        st.session_state.staff_calendar_events = []

    # Load sample data if empty
    if len(st.session_state.staff_registry) == 0:
        _load_sample_staff_data()

    if len(st.session_state.test_standards) == 0:
        _load_sample_test_standards()

    if len(st.session_state.test_protocols) == 0:
        _load_sample_test_protocols()


def _load_sample_staff_data():
    """Load sample staff members into the registry"""
    sample_staff = [
        {
            'staff_id': 'STF-001',
            'name': 'Dr. Sarah Chen',
            'role': 'Senior Test Engineer',
            'expertise_areas': ['IEC 61215 Testing', 'Thermal Cycling', 'Mechanical Load'],
            'certifications': [
                {'cert_name': 'IEC 61215 Certification', 'expiry_date': '2025-12-31'},
                {'cert_name': 'ISO 9001 Auditor', 'expiry_date': '2026-06-30'}
            ],
            'is_available': True,
            'tasks_completed': 145,
            'quality_score': 96,
            'speed_score': 88,
            'reliability': 98,
            'current_load': 6,
            'capacity': 10,
            'email': 'sarah.chen@example.com',
            'phone': '+1-555-0101'
        },
        {
            'staff_id': 'STF-002',
            'name': 'James Rodriguez',
            'role': 'Test Technician',
            'expertise_areas': ['UV Testing', 'Humidity Freeze', 'Visual Inspection'],
            'certifications': [
                {'cert_name': 'IEC 61730 Safety Testing', 'expiry_date': '2025-08-15'},
                {'cert_name': 'Electrical Safety', 'expiry_date': '2025-11-20'}
            ],
            'is_available': True,
            'tasks_completed': 203,
            'quality_score': 92,
            'speed_score': 94,
            'reliability': 95,
            'current_load': 8,
            'capacity': 10,
            'email': 'james.rodriguez@example.com',
            'phone': '+1-555-0102'
        },
        {
            'staff_id': 'STF-003',
            'name': 'Maria Santos',
            'role': 'Laboratory Manager',
            'expertise_areas': ['Quality Control', 'All IEC Standards', 'ISO Compliance'],
            'certifications': [
                {'cert_name': 'Lab Management Cert', 'expiry_date': '2026-03-15'},
                {'cert_name': 'ISO 17025 Lead Assessor', 'expiry_date': '2025-09-30'}
            ],
            'is_available': False,  # On vacation
            'tasks_completed': 98,
            'quality_score': 99,
            'speed_score': 85,
            'reliability': 99,
            'current_load': 0,
            'capacity': 8,
            'email': 'maria.santos@example.com',
            'phone': '+1-555-0103'
        },
        {
            'staff_id': 'STF-004',
            'name': 'Michael Zhang',
            'role': 'Junior Test Engineer',
            'expertise_areas': ['Data Analysis', 'Report Generation', 'Sample Preparation'],
            'certifications': [
                {'cert_name': 'Basic PV Testing', 'expiry_date': '2025-07-01'}
            ],
            'is_available': True,
            'tasks_completed': 67,
            'quality_score': 87,
            'speed_score': 91,
            'reliability': 89,
            'current_load': 4,
            'capacity': 8,
            'email': 'michael.zhang@example.com',
            'phone': '+1-555-0104'
        },
        {
            'staff_id': 'STF-005',
            'name': 'Emily Johnson',
            'role': 'Quality Assurance Specialist',
            'expertise_areas': ['Data Validation', 'Protocol Compliance', 'Audit Support'],
            'certifications': [
                {'cert_name': 'QA Professional', 'expiry_date': '2026-01-15'},
                {'cert_name': 'Six Sigma Green Belt', 'expiry_date': '2025-10-10'}
            ],
            'is_available': True,
            'tasks_completed': 178,
            'quality_score': 98,
            'speed_score': 87,
            'reliability': 97,
            'current_load': 5,
            'capacity': 10,
            'email': 'emily.johnson@example.com',
            'phone': '+1-555-0105'
        }
    ]

    st.session_state.staff_registry.extend(sample_staff)

    # Add some sample calendar events
    sample_events = [
        {
            'event_id': 'EVT-001',
            'staff_id': 'STF-003',
            'event_type': 'Holiday',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'description': 'Annual Leave'
        },
        {
            'event_id': 'EVT-002',
            'staff_id': 'STF-001',
            'event_type': 'Assignment',
            'start_date': datetime.now().strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'description': 'IEC 61215 Module Testing - Project Alpha'
        },
        {
            'event_id': 'EVT-003',
            'staff_id': 'STF-002',
            'event_type': 'Training',
            'start_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d'),
            'description': 'Advanced UV Testing Workshop'
        }
    ]

    st.session_state.staff_calendar_events.extend(sample_events)


def _load_sample_test_standards():
    """Load sample test standards (IEC, ISO)"""
    sample_standards = [
        {
            'test_id': 'IEC-61215-001',
            'standard_name': 'IEC 61215',
            'version': '2021',
            'method_number': '10.8',
            'test_name': 'Thermal Cycling Test',
            'description': 'Test to determine the ability of the module to withstand thermal mismatch, fatigue and other stresses caused by repeated temperature changes.',
            'category': 'Environmental',
            'duration_hours': 200,
            'equipment_required': ['Thermal Chamber', 'Temperature Logger', 'I-V Tracer']
        },
        {
            'test_id': 'IEC-61215-002',
            'standard_name': 'IEC 61215',
            'version': '2021',
            'method_number': '10.13',
            'test_name': 'Humidity Freeze Test',
            'description': 'Test to determine the ability of the module to withstand the effects of high temperature and humidity followed by sub-zero temperatures.',
            'category': 'Environmental',
            'duration_hours': 240,
            'equipment_required': ['Climate Chamber', 'Humidity Sensor', 'I-V Tracer']
        },
        {
            'test_id': 'IEC-61730-001',
            'standard_name': 'IEC 61730',
            'version': '2016',
            'method_number': 'MST-01',
            'test_name': 'Module Safety Test - Electrical',
            'description': 'Safety qualification test for photovoltaic modules - Electrical safety requirements.',
            'category': 'Safety',
            'duration_hours': 48,
            'equipment_required': ['High Voltage Tester', 'Insulation Tester', 'Safety Monitor']
        }
    ]

    st.session_state.test_standards.extend(sample_standards)


def _load_sample_test_protocols():
    """Load sample test protocol templates"""
    sample_protocols = [
        {
            'protocol_id': 'PROT-TC-001',
            'test_id': 'IEC-61215-001',
            'protocol_name': 'Thermal Cycling Protocol - Standard Modules',
            'version': '1.2',
            'steps': [
                {'step': 1, 'instruction': 'Visual inspection and photograph the module', 'duration_min': 15},
                {'step': 2, 'instruction': 'Perform initial I-V curve measurement at STC', 'duration_min': 30},
                {'step': 3, 'instruction': 'Install module in thermal chamber with proper mounting', 'duration_min': 20},
                {'step': 4, 'instruction': 'Connect temperature sensors to module surface and junction box', 'duration_min': 10},
                {'step': 5, 'instruction': 'Run 200 thermal cycles: -40°C to +85°C', 'duration_min': 12000},
                {'step': 6, 'instruction': 'Remove module and perform final I-V curve measurement', 'duration_min': 30},
                {'step': 7, 'instruction': 'Visual inspection for defects (delamination, cracks, etc.)', 'duration_min': 15}
            ],
            'expected_results': {
                'max_power_degradation': 5,  # Maximum allowed % degradation
                'visual_defects': 'None',
                'insulation_resistance': '>40 MΩ'
            },
            'pass_criteria': {
                'power_degradation_limit': 5.0,  # %
                'no_visual_defects': True,
                'min_insulation_resistance': 40  # MΩ
            },
            'operator_instructions': 'Ensure thermal chamber is calibrated. Monitor temperature uniformity. Record any anomalies during cycling.',
            'safety_notes': 'High temperature hazard. Use protective equipment. Allow cool-down before handling.',
            'created_date': '2024-01-15',
            'approved_by': 'Maria Santos'
        },
        {
            'protocol_id': 'PROT-HF-001',
            'test_id': 'IEC-61215-002',
            'protocol_name': 'Humidity Freeze Protocol - Standard Modules',
            'version': '1.1',
            'steps': [
                {'step': 1, 'instruction': 'Visual inspection and document initial condition', 'duration_min': 15},
                {'step': 2, 'instruction': 'Measure initial I-V characteristics at STC', 'duration_min': 30},
                {'step': 3, 'instruction': 'Place module in climate chamber', 'duration_min': 15},
                {'step': 4, 'instruction': 'Run 10 humidity-freeze cycles per IEC 61215', 'duration_min': 14400},
                {'step': 5, 'instruction': 'Final I-V measurement at STC', 'duration_min': 30},
                {'step': 6, 'instruction': 'Final visual inspection for moisture ingress or damage', 'duration_min': 20}
            ],
            'expected_results': {
                'max_power_degradation': 5,
                'visual_defects': 'None',
                'moisture_ingress': 'None'
            },
            'pass_criteria': {
                'power_degradation_limit': 5.0,
                'no_visual_defects': True,
                'no_moisture_ingress': True
            },
            'operator_instructions': 'Monitor humidity levels carefully. Ensure proper defrost cycles. Check for condensation.',
            'safety_notes': 'Low temperature and high humidity hazards. Use proper PPE.',
            'created_date': '2024-02-10',
            'approved_by': 'Maria Santos'
        }
    ]

    st.session_state.test_protocols.extend(sample_protocols)


# ============================================================================
# MANPOWER MANAGEMENT FUNCTIONS
# ============================================================================

def render_manpower_dashboard():
    """
    Render comprehensive manpower dashboard with overview, workload, and utilization metrics.
    """
    st.subheader("👥 Manpower Dashboard")

    initialize_manpower_protocols_data()

    staff_data = st.session_state.staff_registry

    if not staff_data:
        st.warning("No staff members in registry. Please add staff members first.")
        return

    # Calculate aggregate metrics
    total_staff = len(staff_data)
    available_staff = sum(1 for s in staff_data if s['is_available'])
    total_capacity = sum(s['capacity'] for s in staff_data)
    total_current_load = sum(s['current_load'] for s in staff_data)
    avg_utilization = (total_current_load / total_capacity * 100) if total_capacity > 0 else 0
    avg_quality_score = np.mean([s['quality_score'] for s in staff_data])
    avg_speed_score = np.mean([s['speed_score'] for s in staff_data])
    avg_reliability = np.mean([s['reliability'] for s in staff_data])

    # Display key metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Staff", total_staff)
    with col2:
        st.metric("Available Staff", available_staff, delta=f"{available_staff}/{total_staff}")
    with col3:
        st.metric("Utilization", f"{avg_utilization:.1f}%",
                 delta=f"{total_current_load}/{total_capacity} tasks")
    with col4:
        st.metric("Avg Quality Score", f"{avg_quality_score:.1f}",
                 delta=f"±{np.std([s['quality_score'] for s in staff_data]):.1f}")
    with col5:
        st.metric("Avg Reliability", f"{avg_reliability:.1f}%")

    st.divider()

    # Workload Analysis Section
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### 📊 Workload Analysis")

        # Create workload bar chart
        df_workload = pd.DataFrame([
            {
                'Name': s['name'],
                'Current Load': s['current_load'],
                'Capacity': s['capacity'],
                'Utilization %': (s['current_load'] / s['capacity'] * 100) if s['capacity'] > 0 else 0,
                'Available': s['is_available']
            }
            for s in staff_data
        ])

        fig_workload = go.Figure()

        fig_workload.add_trace(go.Bar(
            name='Current Load',
            x=df_workload['Name'],
            y=df_workload['Current Load'],
            marker_color='#FF6B6B'
        ))

        fig_workload.add_trace(go.Bar(
            name='Available Capacity',
            x=df_workload['Name'],
            y=df_workload['Capacity'] - df_workload['Current Load'],
            marker_color='#4ECDC4'
        ))

        fig_workload.update_layout(
            barmode='stack',
            title='Staff Workload Distribution',
            xaxis_title='Staff Member',
            yaxis_title='Task Count',
            height=400,
            showlegend=True,
            hovermode='x unified'
        )

        st.plotly_chart(fig_workload, use_container_width=True)

    with col_right:
        st.markdown("### 🎯 Performance Metrics")

        # Create performance radar chart
        df_performance = pd.DataFrame([
            {
                'Name': s['name'],
                'Quality': s['quality_score'],
                'Speed': s['speed_score'],
                'Reliability': s['reliability']
            }
            for s in staff_data
        ])

        # Create grouped bar chart for performance
        fig_performance = go.Figure()

        fig_performance.add_trace(go.Bar(
            name='Quality Score',
            x=df_performance['Name'],
            y=df_performance['Quality'],
            marker_color='#95E1D3'
        ))

        fig_performance.add_trace(go.Bar(
            name='Speed Score',
            x=df_performance['Name'],
            y=df_performance['Speed'],
            marker_color='#F38181'
        ))

        fig_performance.add_trace(go.Bar(
            name='Reliability',
            x=df_performance['Name'],
            y=df_performance['Reliability'],
            marker_color='#AA96DA'
        ))

        fig_performance.update_layout(
            barmode='group',
            title='Staff Performance Comparison',
            xaxis_title='Staff Member',
            yaxis_title='Score (0-100)',
            height=400,
            showlegend=True,
            yaxis_range=[0, 105]
        )

        st.plotly_chart(fig_performance, use_container_width=True)

    st.divider()

    # Staff Details Table
    st.markdown("### 📋 Staff Details & Utilization")

    # Create detailed staff table
    staff_table_data = []
    for staff in staff_data:
        utilization_pct = (staff['current_load'] / staff['capacity'] * 100) if staff['capacity'] > 0 else 0
        capacity_remaining = staff['capacity'] - staff['current_load']

        # Check for expiring certifications (within 60 days)
        expiring_certs = []
        for cert in staff['certifications']:
            try:
                expiry_date = datetime.strptime(cert['expiry_date'], '%Y-%m-%d')
                days_until_expiry = (expiry_date - datetime.now()).days
                if 0 < days_until_expiry <= 60:
                    expiring_certs.append(f"{cert['cert_name']} ({days_until_expiry}d)")
            except:
                pass

        staff_table_data.append({
            'ID': staff['staff_id'],
            'Name': staff['name'],
            'Role': staff['role'],
            'Status': '✅ Available' if staff['is_available'] else '❌ Unavailable',
            'Current Load': staff['current_load'],
            'Capacity': staff['capacity'],
            'Utilization %': f"{utilization_pct:.1f}%",
            'Remaining': capacity_remaining,
            'Quality': staff['quality_score'],
            'Speed': staff['speed_score'],
            'Reliability': staff['reliability'],
            'Tasks Done': staff['tasks_completed'],
            'Expiring Certs': ', '.join(expiring_certs) if expiring_certs else 'None'
        })

    df_staff_table = pd.DataFrame(staff_table_data)

    # Color code by utilization
    def highlight_utilization(row):
        util_str = row['Utilization %'].rstrip('%')
        util_val = float(util_str)
        if util_val >= 80:
            return ['background-color: #FFE5E5'] * len(row)
        elif util_val >= 60:
            return ['background-color: #FFF4E5'] * len(row)
        else:
            return ['background-color: #E5FFE5'] * len(row)

    st.dataframe(
        df_staff_table.style.apply(highlight_utilization, axis=1),
        use_container_width=True,
        height=400
    )

    # Certification Alerts
    st.markdown("### ⚠️ Certification Expiration Alerts")

    alerts = []
    for staff in staff_data:
        for cert in staff['certifications']:
            try:
                expiry_date = datetime.strptime(cert['expiry_date'], '%Y-%m-%d')
                days_until_expiry = (expiry_date - datetime.now()).days

                if days_until_expiry < 0:
                    alert_level = "🔴 EXPIRED"
                elif days_until_expiry <= 30:
                    alert_level = "🟠 CRITICAL"
                elif days_until_expiry <= 60:
                    alert_level = "🟡 WARNING"
                else:
                    continue

                alerts.append({
                    'Alert': alert_level,
                    'Staff': staff['name'],
                    'Certification': cert['cert_name'],
                    'Expiry Date': cert['expiry_date'],
                    'Days Remaining': days_until_expiry
                })
            except:
                pass

    if alerts:
        df_alerts = pd.DataFrame(alerts)
        st.dataframe(df_alerts, use_container_width=True)
    else:
        st.success("✅ No certifications expiring in the next 60 days")

    # Skill Matrix
    st.markdown("### 🎓 Expertise & Skills Matrix")

    # Collect all unique skills
    all_skills = set()
    for staff in staff_data:
        all_skills.update(staff['expertise_areas'])

    # Create skill matrix
    skill_matrix_data = []
    for staff in staff_data:
        row = {'Staff': staff['name']}
        for skill in sorted(all_skills):
            row[skill] = '✓' if skill in staff['expertise_areas'] else ''
        skill_matrix_data.append(row)

    df_skills = pd.DataFrame(skill_matrix_data)
    st.dataframe(df_skills, use_container_width=True)


def render_availability_calendar():
    """
    Render staff availability calendar with shifts, holidays, and assignments.
    """
    st.subheader("📅 Staff Availability Calendar")

    initialize_manpower_protocols_data()

    staff_data = st.session_state.staff_registry
    calendar_events = st.session_state.staff_calendar_events

    if not staff_data:
        st.warning("No staff members in registry.")
        return

    # Calendar view controls
    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:
        view_mode = st.selectbox("View Mode", ["Timeline", "Monthly Grid", "Staff Schedule"])

    with col2:
        selected_month = st.date_input("Select Month", datetime.now())

    with col3:
        filter_staff = st.multiselect(
            "Filter by Staff",
            options=[s['name'] for s in staff_data],
            default=[s['name'] for s in staff_data]
        )

    st.divider()

    # Timeline View
    if view_mode == "Timeline":
        st.markdown("### 📊 Event Timeline")

        # Prepare timeline data
        timeline_data = []
        for event in calendar_events:
            # Find staff name
            staff_name = next((s['name'] for s in staff_data if s['staff_id'] == event['staff_id']), 'Unknown')

            if staff_name in filter_staff:
                timeline_data.append({
                    'Task': f"{staff_name} - {event['event_type']}",
                    'Start': event['start_date'],
                    'Finish': event['end_date'],
                    'Resource': staff_name,
                    'Description': event['description'],
                    'Type': event['event_type']
                })

        if timeline_data:
            df_timeline = pd.DataFrame(timeline_data)

            # Color mapping for event types
            color_map = {
                'Holiday': '#FF6B6B',
                'Assignment': '#4ECDC4',
                'Training': '#95E1D3',
                'Shift': '#F38181',
                'Meeting': '#AA96DA'
            }

            df_timeline['Color'] = df_timeline['Type'].map(color_map)

            fig_timeline = px.timeline(
                df_timeline,
                x_start='Start',
                x_end='Finish',
                y='Task',
                color='Type',
                hover_data=['Description'],
                title='Staff Availability Timeline',
                color_discrete_map=color_map
            )

            fig_timeline.update_layout(
                height=max(400, len(timeline_data) * 30),
                xaxis_title='Date',
                yaxis_title='Staff & Event Type'
            )

            st.plotly_chart(fig_timeline, use_container_width=True)
        else:
            st.info("No events found for selected filters")

    # Monthly Grid View
    elif view_mode == "Monthly Grid":
        st.markdown("### 📆 Monthly Calendar Grid")

        # Generate calendar grid for the month
        start_of_month = selected_month.replace(day=1)
        if start_of_month.month == 12:
            end_of_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            end_of_month = start_of_month.replace(month=start_of_month.month + 1, day=1) - timedelta(days=1)

        # Create calendar grid
        st.markdown(f"**{start_of_month.strftime('%B %Y')}**")

        # Week day headers
        weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        cols = st.columns(7)
        for i, day in enumerate(weekdays):
            cols[i].markdown(f"**{day}**")

        # Get first day of month (0=Monday, 6=Sunday)
        first_weekday = start_of_month.weekday()

        # Generate days
        current_date = start_of_month
        week_cols = st.columns(7)
        day_index = first_weekday

        while current_date <= end_of_month:
            if day_index >= 7:
                day_index = 0
                week_cols = st.columns(7)

            # Check if there are events on this day
            date_str = current_date.strftime('%Y-%m-%d')
            events_today = [
                e for e in calendar_events
                if e['start_date'] <= date_str <= e['end_date']
            ]

            # Filter by selected staff
            events_today = [
                e for e in events_today
                if next((s['name'] for s in staff_data if s['staff_id'] == e['staff_id']), '') in filter_staff
            ]

            event_count = len(events_today)

            with week_cols[day_index]:
                if event_count > 0:
                    st.markdown(f"**{current_date.day}** 🔴")
                    for evt in events_today[:2]:  # Show max 2 events
                        staff_name = next((s['name'] for s in staff_data if s['staff_id'] == evt['staff_id']), 'Unknown')
                        st.caption(f"{evt['event_type'][:3]}: {staff_name[:10]}")
                else:
                    st.markdown(f"{current_date.day}")

            current_date += timedelta(days=1)
            day_index += 1

    # Staff Schedule View
    else:  # Staff Schedule
        st.markdown("### 👤 Individual Staff Schedules")

        for staff in staff_data:
            if staff['name'] not in filter_staff:
                continue

            with st.expander(f"📋 {staff['name']} - {staff['role']}", expanded=True):
                col_info, col_status = st.columns([2, 1])

                with col_info:
                    st.markdown(f"**Status:** {'✅ Available' if staff['is_available'] else '❌ Unavailable'}")
                    st.markdown(f"**Current Load:** {staff['current_load']}/{staff['capacity']} tasks")
                    st.markdown(f"**Utilization:** {(staff['current_load']/staff['capacity']*100):.1f}%")

                with col_status:
                    utilization = (staff['current_load'] / staff['capacity'] * 100) if staff['capacity'] > 0 else 0
                    if utilization >= 80:
                        st.error("🔴 High Load")
                    elif utilization >= 60:
                        st.warning("🟡 Medium Load")
                    else:
                        st.success("🟢 Low Load")

                # Show events for this staff member
                staff_events = [e for e in calendar_events if e['staff_id'] == staff['staff_id']]

                if staff_events:
                    st.markdown("**Upcoming Events:**")
                    for evt in staff_events:
                        event_icon = {
                            'Holiday': '🏖️',
                            'Assignment': '📋',
                            'Training': '📚',
                            'Shift': '⏰',
                            'Meeting': '👥'
                        }.get(evt['event_type'], '📌')

                        st.markdown(
                            f"{event_icon} **{evt['event_type']}**: {evt['description']} "
                            f"({evt['start_date']} to {evt['end_date']})"
                        )
                else:
                    st.info("No scheduled events")

    st.divider()

    # Add New Event Form
    st.markdown("### ➕ Add New Calendar Event")

    with st.form("new_event_form"):
        col1, col2 = st.columns(2)

        with col1:
            event_staff = st.selectbox(
                "Select Staff Member*",
                options=[s['staff_id'] for s in staff_data],
                format_func=lambda x: next((s['name'] for s in staff_data if s['staff_id'] == x), x)
            )
            event_type = st.selectbox(
                "Event Type*",
                options=['Holiday', 'Assignment', 'Training', 'Shift', 'Meeting', 'Other']
            )
            event_description = st.text_input("Description*", placeholder="Brief description of the event")

        with col2:
            event_start = st.date_input("Start Date*", datetime.now())
            event_end = st.date_input("End Date*", datetime.now() + timedelta(days=1))

        submit_event = st.form_submit_button("Add Event", type="primary")

        if submit_event:
            # Validation
            if not event_description:
                st.error("❌ Description is required")
            elif event_start > event_end:
                st.error("❌ Start date must be before or equal to end date")
            else:
                new_event = {
                    'event_id': f'EVT-{str(uuid.uuid4())[:8]}',
                    'staff_id': event_staff,
                    'event_type': event_type,
                    'start_date': event_start.strftime('%Y-%m-%d'),
                    'end_date': event_end.strftime('%Y-%m-%d'),
                    'description': event_description
                }

                st.session_state.staff_calendar_events.append(new_event)
                st.success(f"✅ Event added successfully for {next((s['name'] for s in staff_data if s['staff_id'] == event_staff), 'staff member')}")
                st.rerun()


def assign_task_to_staff(task_name, required_skills=None, preferred_staff_id=None):
    """
    Skill-based task assignment logic.
    Automatically suggests best staff member based on skills, availability, and workload.

    Args:
        task_name: Name/description of the task
        required_skills: List of required expertise areas
        preferred_staff_id: Optional specific staff member to assign to

    Returns:
        dict: Assignment result with staff_id and reason
    """
    initialize_manpower_protocols_data()

    staff_data = st.session_state.staff_registry

    if not staff_data:
        return {'success': False, 'message': 'No staff members available'}

    # If preferred staff specified, try to assign to them
    if preferred_staff_id:
        staff = next((s for s in staff_data if s['staff_id'] == preferred_staff_id), None)
        if staff:
            if not staff['is_available']:
                return {'success': False, 'message': f"{staff['name']} is not available"}
            if staff['current_load'] >= staff['capacity']:
                return {'success': False, 'message': f"{staff['name']} is at full capacity"}

            # Assign task
            staff['current_load'] += 1
            return {
                'success': True,
                'staff_id': staff['staff_id'],
                'staff_name': staff['name'],
                'message': f"Task assigned to {staff['name']}"
            }

    # Otherwise, find best match based on skills and availability
    candidates = []

    for staff in staff_data:
        if not staff['is_available']:
            continue
        if staff['current_load'] >= staff['capacity']:
            continue

        # Calculate match score
        skill_match = 0
        if required_skills:
            skill_match = len(set(required_skills) & set(staff['expertise_areas'])) / len(required_skills)

        utilization = staff['current_load'] / staff['capacity']
        availability_score = 1 - utilization

        # Composite score
        composite_score = (
            skill_match * 0.5 +
            availability_score * 0.2 +
            (staff['quality_score'] / 100) * 0.15 +
            (staff['reliability'] / 100) * 0.15
        )

        candidates.append({
            'staff': staff,
            'score': composite_score,
            'skill_match': skill_match,
            'availability': availability_score
        })

    if not candidates:
        return {'success': False, 'message': 'No available staff members with capacity'}

    # Select best candidate
    best_candidate = max(candidates, key=lambda x: x['score'])
    staff = best_candidate['staff']

    # Assign task
    staff['current_load'] += 1

    return {
        'success': True,
        'staff_id': staff['staff_id'],
        'staff_name': staff['name'],
        'score': best_candidate['score'],
        'skill_match': best_candidate['skill_match'],
        'message': f"Task assigned to {staff['name']} (match score: {best_candidate['score']:.2f})"
    }


# ============================================================================
# TEST METHODS & PROTOCOL FUNCTIONS
# ============================================================================

def render_test_selection():
    """
    Render test method selection interface with search and filtering.
    """
    st.subheader("🔬 Test Method Selection")

    initialize_manpower_protocols_data()

    test_standards = st.session_state.test_standards

    if not test_standards:
        st.warning("No test standards available in database.")
        return

    # Search and filter controls
    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        search_query = st.text_input("🔍 Search test methods", placeholder="Enter test name or standard...")

    with col2:
        filter_standard = st.multiselect(
            "Filter by Standard",
            options=list(set(t['standard_name'] for t in test_standards)),
            default=list(set(t['standard_name'] for t in test_standards))
        )

    with col3:
        filter_category = st.multiselect(
            "Filter by Category",
            options=list(set(t.get('category', 'General') for t in test_standards)),
            default=list(set(t.get('category', 'General') for t in test_standards))
        )

    st.divider()

    # Filter tests
    filtered_tests = test_standards

    if search_query:
        filtered_tests = [
            t for t in filtered_tests
            if search_query.lower() in t['test_name'].lower() or
               search_query.lower() in t['description'].lower() or
               search_query.lower() in t['standard_name'].lower()
        ]

    if filter_standard:
        filtered_tests = [t for t in filtered_tests if t['standard_name'] in filter_standard]

    if filter_category:
        filtered_tests = [t for t in filtered_tests if t.get('category', 'General') in filter_category]

    # Display test methods
    st.markdown(f"### 📋 Available Test Methods ({len(filtered_tests)} found)")

    if not filtered_tests:
        st.info("No test methods match your search criteria")
        return

    # Display as cards
    for test in filtered_tests:
        with st.expander(f"**{test['test_name']}** - {test['standard_name']} {test['version']}", expanded=False):
            col_info, col_details = st.columns([2, 1])

            with col_info:
                st.markdown(f"**Test ID:** `{test['test_id']}`")
                st.markdown(f"**Method Number:** {test['method_number']}")
                st.markdown(f"**Category:** {test.get('category', 'General')}")
                st.markdown(f"**Description:**")
                st.info(test['description'])

            with col_details:
                st.markdown(f"**Duration:** {test.get('duration_hours', 'N/A')} hours")
                st.markdown("**Required Equipment:**")
                for eq in test.get('equipment_required', []):
                    st.markdown(f"- {eq}")

            # Check if protocols exist for this test
            related_protocols = [
                p for p in st.session_state.test_protocols
                if p['test_id'] == test['test_id']
            ]

            if related_protocols:
                st.success(f"✅ {len(related_protocols)} protocol(s) available")
                for protocol in related_protocols:
                    st.markdown(f"- {protocol['protocol_name']} (v{protocol['version']})")
            else:
                st.warning("⚠️ No protocols defined for this test")

            # Action button
            if st.button(f"Select {test['test_name']}", key=f"select_{test['test_id']}"):
                st.session_state['selected_test_id'] = test['test_id']
                st.success(f"✅ Selected: {test['test_name']}")


def render_protocol_entry_sheet(protocol_id=None):
    """
    Render protocol entry sheet for operators to input test results.
    Includes form validation and auto-compliance checking.

    Args:
        protocol_id: Optional specific protocol to display. If None, shows selection.
    """
    st.subheader("📝 Test Protocol Entry Sheet")

    initialize_manpower_protocols_data()

    test_protocols = st.session_state.test_protocols
    test_standards = st.session_state.test_standards

    if not test_protocols:
        st.warning("No test protocols available. Please create protocols first.")
        return

    # Protocol selection
    if protocol_id is None:
        selected_protocol_id = st.selectbox(
            "Select Test Protocol",
            options=[p['protocol_id'] for p in test_protocols],
            format_func=lambda x: next((p['protocol_name'] for p in test_protocols if p['protocol_id'] == x), x)
        )
    else:
        selected_protocol_id = protocol_id

    protocol = next((p for p in test_protocols if p['protocol_id'] == selected_protocol_id), None)

    if not protocol:
        st.error("Protocol not found")
        return

    # Get associated test standard
    test_standard = next((t for t in test_standards if t['test_id'] == protocol['test_id']), None)

    st.divider()

    # Display protocol information
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"### {protocol['protocol_name']}")
        st.markdown(f"**Version:** {protocol['version']} | **Protocol ID:** `{protocol['protocol_id']}`")
        if test_standard:
            st.markdown(f"**Test Standard:** {test_standard['standard_name']} - {test_standard['test_name']}")

    with col2:
        st.markdown("**Approved By:**")
        st.info(protocol.get('approved_by', 'N/A'))

    with col3:
        st.markdown("**Created:**")
        st.info(protocol.get('created_date', 'N/A'))

    st.divider()

    # Safety Notes
    if protocol.get('safety_notes'):
        st.warning(f"⚠️ **Safety Notes:** {protocol['safety_notes']}")

    # Operator Instructions
    if protocol.get('operator_instructions'):
        st.info(f"ℹ️ **Operator Instructions:** {protocol['operator_instructions']}")

    st.divider()

    # Test Entry Form
    st.markdown("### 📊 Test Data Entry")

    with st.form(f"protocol_entry_{protocol['protocol_id']}"):
        # Basic Information
        st.markdown("#### Basic Information")

        col_basic1, col_basic2, col_basic3 = st.columns(3)

        with col_basic1:
            sample_id = st.text_input("Sample ID*", placeholder="e.g., SAMPLE-001")
            operator_name = st.text_input("Operator Name*", placeholder="Your name")

        with col_basic2:
            test_date = st.date_input("Test Date*", datetime.now())
            equipment_id = st.text_input("Equipment ID", placeholder="e.g., CHAMBER-01")

        with col_basic3:
            batch_number = st.text_input("Batch Number", placeholder="Optional")
            environmental_conditions = st.text_input("Environmental Conditions", placeholder="e.g., 23°C, 45% RH")

        st.divider()

        # Protocol Steps
        st.markdown("#### Protocol Steps Completion")

        step_completion = {}
        for step in protocol['steps']:
            st.markdown(f"**Step {step['step']}:** {step['instruction']}")
            st.caption(f"_Estimated duration: {step['duration_min']} minutes_")

            col_step1, col_step2 = st.columns([3, 1])

            with col_step1:
                step_notes = st.text_area(
                    f"Notes for Step {step['step']}",
                    key=f"step_{step['step']}_notes",
                    placeholder="Enter observations, measurements, or notes...",
                    height=80
                )

            with col_step2:
                step_complete = st.checkbox(
                    f"Step {step['step']} Complete",
                    key=f"step_{step['step']}_complete"
                )

            step_completion[step['step']] = {
                'notes': step_notes,
                'complete': step_complete
            }

        st.divider()

        # Results Entry (based on pass criteria)
        st.markdown("#### Test Results")

        pass_criteria = protocol.get('pass_criteria', {})

        results = {}

        # Power degradation (if applicable)
        if 'power_degradation_limit' in pass_criteria:
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                initial_power = st.number_input("Initial Power (W)*", min_value=0.0, format="%.2f")
            with col_r2:
                final_power = st.number_input("Final Power (W)*", min_value=0.0, format="%.2f")

            if initial_power > 0:
                power_degradation = ((initial_power - final_power) / initial_power) * 100
                results['power_degradation'] = power_degradation
                results['initial_power'] = initial_power
                results['final_power'] = final_power

                # Show calculated degradation
                if power_degradation <= pass_criteria['power_degradation_limit']:
                    st.success(f"✅ Power Degradation: {power_degradation:.2f}% (Limit: {pass_criteria['power_degradation_limit']}%)")
                else:
                    st.error(f"❌ Power Degradation: {power_degradation:.2f}% (Limit: {pass_criteria['power_degradation_limit']}%)")

        # Visual defects check
        if 'no_visual_defects' in pass_criteria:
            visual_defects = st.radio(
                "Visual Defects Observed?*",
                options=['No', 'Yes'],
                horizontal=True
            )
            results['visual_defects'] = visual_defects

            if visual_defects == 'Yes':
                defect_description = st.text_area("Describe Visual Defects*", placeholder="Detail any cracks, delamination, discoloration, etc.")
                results['defect_description'] = defect_description

        # Insulation resistance (if applicable)
        if 'min_insulation_resistance' in pass_criteria:
            insulation_resistance = st.number_input(
                f"Insulation Resistance (MΩ)* - Min: {pass_criteria['min_insulation_resistance']}",
                min_value=0.0,
                format="%.1f"
            )
            results['insulation_resistance'] = insulation_resistance

            if insulation_resistance >= pass_criteria['min_insulation_resistance']:
                st.success(f"✅ Insulation Resistance: {insulation_resistance} MΩ (Min: {pass_criteria['min_insulation_resistance']} MΩ)")
            else:
                st.error(f"❌ Insulation Resistance: {insulation_resistance} MΩ (Min: {pass_criteria['min_insulation_resistance']} MΩ)")

        # Moisture ingress (if applicable)
        if 'no_moisture_ingress' in pass_criteria:
            moisture_ingress = st.radio(
                "Moisture Ingress Detected?*",
                options=['No', 'Yes'],
                horizontal=True
            )
            results['moisture_ingress'] = moisture_ingress

        st.divider()

        # Additional observations
        st.markdown("#### Additional Information")

        additional_observations = st.text_area(
            "Additional Observations",
            placeholder="Any additional notes, anomalies, or observations...",
            height=100
        )
        results['additional_observations'] = additional_observations

        # Attachments
        uploaded_files = st.file_uploader(
            "Attach Files (photos, data files, etc.)",
            accept_multiple_files=True,
            type=['jpg', 'jpeg', 'png', 'pdf', 'csv', 'xlsx']
        )

        # Submit button
        submit_results = st.form_submit_button("Submit Test Results", type="primary")

        if submit_results:
            # Validation
            errors = []

            if not sample_id:
                errors.append("Sample ID is required")
            if not operator_name:
                errors.append("Operator name is required")

            # Check all steps completed
            incomplete_steps = [s for s, data in step_completion.items() if not data['complete']]
            if incomplete_steps:
                errors.append(f"Steps {', '.join(map(str, incomplete_steps))} are not marked as complete")

            # Validate results based on criteria
            if 'power_degradation_limit' in pass_criteria:
                if initial_power == 0 or final_power == 0:
                    errors.append("Initial and final power measurements are required")

            if 'no_visual_defects' in pass_criteria:
                if visual_defects == 'Yes' and not results.get('defect_description'):
                    errors.append("Please describe the visual defects observed")

            if errors:
                st.error("❌ Please fix the following errors:")
                for error in errors:
                    st.error(f"- {error}")
            else:
                # Auto-validate against pass criteria
                compliance_status = validate_test_results(results, pass_criteria)

                # Save results
                test_result = {
                    'result_id': f'RESULT-{str(uuid.uuid4())[:8]}',
                    'protocol_id': protocol['protocol_id'],
                    'sample_id': sample_id,
                    'operator_name': operator_name,
                    'test_date': test_date.strftime('%Y-%m-%d'),
                    'equipment_id': equipment_id,
                    'batch_number': batch_number,
                    'environmental_conditions': environmental_conditions,
                    'step_completion': step_completion,
                    'results': results,
                    'compliance_status': compliance_status['status'],
                    'compliance_details': compliance_status['details'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'version': protocol['version'],
                    'attachments': [f.name for f in uploaded_files] if uploaded_files else []
                }

                st.session_state.test_results.append(test_result)

                # Display result
                if compliance_status['status'] == 'PASS':
                    st.success(f"✅ Test PASSED - Results saved with ID: {test_result['result_id']}")
                elif compliance_status['status'] == 'FAIL':
                    st.error(f"❌ Test FAILED - Results saved with ID: {test_result['result_id']}")
                else:
                    st.warning(f"⚠️ Test results recorded with warnings - ID: {test_result['result_id']}")

                # Show compliance details
                st.markdown("**Compliance Check:**")
                for detail in compliance_status['details']:
                    if detail['pass']:
                        st.success(f"✅ {detail['criterion']}: {detail['message']}")
                    else:
                        st.error(f"❌ {detail['criterion']}: {detail['message']}")

                st.balloons()


def validate_test_results(results, pass_criteria):
    """
    Auto-validate test results against pass criteria.

    Args:
        results: Dictionary of test results
        pass_criteria: Dictionary of pass/fail criteria

    Returns:
        dict: Validation result with status and details
    """
    compliance_details = []
    all_passed = True

    # Check power degradation
    if 'power_degradation_limit' in pass_criteria:
        limit = pass_criteria['power_degradation_limit']
        actual = results.get('power_degradation', 0)

        passed = actual <= limit
        all_passed = all_passed and passed

        compliance_details.append({
            'criterion': 'Power Degradation',
            'pass': passed,
            'expected': f'≤ {limit}%',
            'actual': f'{actual:.2f}%',
            'message': f'Degradation {actual:.2f}% (limit: {limit}%)'
        })

    # Check visual defects
    if 'no_visual_defects' in pass_criteria:
        has_defects = results.get('visual_defects') == 'Yes'
        passed = not has_defects
        all_passed = all_passed and passed

        compliance_details.append({
            'criterion': 'Visual Defects',
            'pass': passed,
            'expected': 'None',
            'actual': 'Defects found' if has_defects else 'None',
            'message': 'No visual defects' if passed else f'Visual defects observed: {results.get("defect_description", "N/A")}'
        })

    # Check insulation resistance
    if 'min_insulation_resistance' in pass_criteria:
        min_required = pass_criteria['min_insulation_resistance']
        actual = results.get('insulation_resistance', 0)

        passed = actual >= min_required
        all_passed = all_passed and passed

        compliance_details.append({
            'criterion': 'Insulation Resistance',
            'pass': passed,
            'expected': f'≥ {min_required} MΩ',
            'actual': f'{actual} MΩ',
            'message': f'Resistance {actual} MΩ (minimum: {min_required} MΩ)'
        })

    # Check moisture ingress
    if 'no_moisture_ingress' in pass_criteria:
        has_moisture = results.get('moisture_ingress') == 'Yes'
        passed = not has_moisture
        all_passed = all_passed and passed

        compliance_details.append({
            'criterion': 'Moisture Ingress',
            'pass': passed,
            'expected': 'None',
            'actual': 'Detected' if has_moisture else 'None',
            'message': 'No moisture ingress' if passed else 'Moisture ingress detected'
        })

    return {
        'status': 'PASS' if all_passed else 'FAIL',
        'details': compliance_details,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def render_test_results_table():
    """
    Render comprehensive test results table with compliance status and filtering.
    """
    st.subheader("📊 Test Results & Compliance Status")

    initialize_manpower_protocols_data()

    test_results = st.session_state.test_results

    if not test_results:
        st.info("No test results recorded yet. Use the Protocol Entry Sheet to record test results.")
        return

    # Filter controls
    col1, col2, col3 = st.columns(3)

    with col1:
        filter_status = st.multiselect(
            "Filter by Status",
            options=['PASS', 'FAIL'],
            default=['PASS', 'FAIL']
        )

    with col2:
        filter_protocol = st.multiselect(
            "Filter by Protocol",
            options=list(set(r['protocol_id'] for r in test_results)),
            default=list(set(r['protocol_id'] for r in test_results))
        )

    with col3:
        date_range = st.date_input(
            "Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now())
        )

    st.divider()

    # Apply filters
    filtered_results = [
        r for r in test_results
        if r['compliance_status'] in filter_status and
           r['protocol_id'] in filter_protocol
    ]

    # Date filtering
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_results = [
            r for r in filtered_results
            if start_date <= datetime.strptime(r['test_date'], '%Y-%m-%d').date() <= end_date
        ]

    # Summary metrics
    total_tests = len(filtered_results)
    passed_tests = sum(1 for r in filtered_results if r['compliance_status'] == 'PASS')
    failed_tests = sum(1 for r in filtered_results if r['compliance_status'] == 'FAIL')
    pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    with col_m1:
        st.metric("Total Tests", total_tests)
    with col_m2:
        st.metric("Passed", passed_tests, delta=f"{pass_rate:.1f}%")
    with col_m3:
        st.metric("Failed", failed_tests, delta=f"{100-pass_rate:.1f}%", delta_color="inverse")
    with col_m4:
        st.metric("Pass Rate", f"{pass_rate:.1f}%")

    st.divider()

    # Results table
    st.markdown("### 📋 Detailed Results")

    if not filtered_results:
        st.info("No results match your filter criteria")
        return

    # Create results table
    results_table_data = []

    for result in filtered_results:
        # Get protocol name
        protocol = next(
            (p for p in st.session_state.test_protocols if p['protocol_id'] == result['protocol_id']),
            None
        )
        protocol_name = protocol['protocol_name'] if protocol else result['protocol_id']

        # Extract key results
        power_deg = result['results'].get('power_degradation', 'N/A')
        if isinstance(power_deg, (int, float)):
            power_deg = f"{power_deg:.2f}%"

        visual_def = result['results'].get('visual_defects', 'N/A')

        results_table_data.append({
            'Result ID': result['result_id'],
            'Sample ID': result['sample_id'],
            'Protocol': protocol_name,
            'Test Date': result['test_date'],
            'Operator': result['operator_name'],
            'Status': '✅ PASS' if result['compliance_status'] == 'PASS' else '❌ FAIL',
            'Power Deg.': power_deg,
            'Visual Defects': visual_def,
            'Version': result.get('version', 'N/A'),
            'Timestamp': result['timestamp']
        })

    df_results = pd.DataFrame(results_table_data)

    # Color code by status
    def highlight_status(row):
        if '✅ PASS' in row['Status']:
            return ['background-color: #E5FFE5'] * len(row)
        else:
            return ['background-color: #FFE5E5'] * len(row)

    st.dataframe(
        df_results.style.apply(highlight_status, axis=1),
        use_container_width=True,
        height=400
    )

    # Export options
    st.markdown("### 📥 Export Options")

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        # Export to CSV
        csv_data = df_results.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv_data,
            file_name=f"test_results_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with col_exp2:
        # Export to JSON
        json_data = json.dumps(filtered_results, indent=2)
        st.download_button(
            label="Download as JSON",
            data=json_data,
            file_name=f"test_results_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

    st.divider()

    # Detailed view
    st.markdown("### 🔍 Detailed Result View")

    selected_result_id = st.selectbox(
        "Select Result to View Details",
        options=[r['result_id'] for r in filtered_results],
        format_func=lambda x: f"{x} - {next((r['sample_id'] for r in filtered_results if r['result_id'] == x), x)}"
    )

    selected_result = next((r for r in filtered_results if r['result_id'] == selected_result_id), None)

    if selected_result:
        with st.expander("View Full Details", expanded=True):
            col_det1, col_det2 = st.columns(2)

            with col_det1:
                st.markdown("#### Test Information")
                st.json({
                    'Result ID': selected_result['result_id'],
                    'Sample ID': selected_result['sample_id'],
                    'Protocol ID': selected_result['protocol_id'],
                    'Test Date': selected_result['test_date'],
                    'Operator': selected_result['operator_name'],
                    'Equipment': selected_result.get('equipment_id', 'N/A'),
                    'Batch': selected_result.get('batch_number', 'N/A'),
                    'Environment': selected_result.get('environmental_conditions', 'N/A')
                })

            with col_det2:
                st.markdown("#### Compliance Status")

                if selected_result['compliance_status'] == 'PASS':
                    st.success("✅ TEST PASSED")
                else:
                    st.error("❌ TEST FAILED")

                st.markdown("**Compliance Details:**")
                for detail in selected_result['compliance_details']:
                    icon = "✅" if detail['pass'] else "❌"
                    st.markdown(f"{icon} **{detail['criterion']}**: {detail['message']}")

            st.markdown("#### Test Results")
            st.json(selected_result['results'])

            st.markdown("#### Step Completion")
            for step_num, step_data in selected_result['step_completion'].items():
                status_icon = "✅" if step_data['complete'] else "❌"
                st.markdown(f"{status_icon} **Step {step_num}**: {step_data['notes'] if step_data['notes'] else 'No notes'}")

            if selected_result.get('attachments'):
                st.markdown("#### Attachments")
                for attachment in selected_result['attachments']:
                    st.markdown(f"📎 {attachment}")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_staff_by_id(staff_id):
    """Get staff member details by ID"""
    return next((s for s in st.session_state.staff_registry if s['staff_id'] == staff_id), None)


def get_protocol_by_id(protocol_id):
    """Get protocol details by ID"""
    return next((p for p in st.session_state.test_protocols if p['protocol_id'] == protocol_id), None)


def get_test_standard_by_id(test_id):
    """Get test standard details by ID"""
    return next((t for t in st.session_state.test_standards if t['test_id'] == test_id), None)


def check_certification_expiry(staff_id, days_ahead=60):
    """
    Check if any certifications are expiring soon for a staff member.

    Args:
        staff_id: Staff member ID
        days_ahead: Number of days to check ahead (default 60)

    Returns:
        list: List of expiring certifications
    """
    staff = get_staff_by_id(staff_id)
    if not staff:
        return []

    expiring = []
    for cert in staff['certifications']:
        try:
            expiry_date = datetime.strptime(cert['expiry_date'], '%Y-%m-%d')
            days_until_expiry = (expiry_date - datetime.now()).days

            if 0 < days_until_expiry <= days_ahead:
                expiring.append({
                    'cert_name': cert['cert_name'],
                    'expiry_date': cert['expiry_date'],
                    'days_remaining': days_until_expiry
                })
        except:
            pass

    return expiring


# ============================================================================
# MODULE METADATA
# ============================================================================

__version__ = '1.0.0'
__author__ = 'Solar PV Project Management System'
__module_id__ = MODULE_ID
__description__ = 'Advanced Manpower Management and Test Protocol System'

# Export public functions
__all__ = [
    'MODULE_ID',
    'initialize_manpower_protocols_data',
    'render_manpower_dashboard',
    'render_availability_calendar',
    'assign_task_to_staff',
    'render_test_selection',
    'render_protocol_entry_sheet',
    'validate_test_results',
    'render_test_results_table',
    'get_staff_by_id',
    'get_protocol_by_id',
    'get_test_standard_by_id',
    'check_certification_expiry'
]
