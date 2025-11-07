"""
Demo/Test Script for Manpower & Test Protocols Module
MODULE_ID: MANPOWER_PROTOCOLS_SESSION3

This script demonstrates how to integrate and use the manpower and test protocol functions.
It can be used as a standalone Streamlit app or integrated into app.py.

Usage:
    streamlit run demo_manpower_protocols.py
"""

import streamlit as st
from manpower_protocols_session3 import (
    MODULE_ID,
    initialize_manpower_protocols_data,
    render_manpower_dashboard,
    render_availability_calendar,
    assign_task_to_staff,
    render_test_selection,
    render_protocol_entry_sheet,
    render_test_results_table,
    get_staff_by_id,
    check_certification_expiry
)

# Page configuration
st.set_page_config(
    page_title=f"Demo - {MODULE_ID}",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #cccccc;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize data
initialize_manpower_protocols_data()

# Main title
st.title("🔬 Solar PV Manpower & Test Protocols Demo")
st.markdown(f"**Module ID:** `{MODULE_ID}`")
st.divider()

# Sidebar navigation
with st.sidebar:
    st.header("📋 Navigation")
    st.markdown("---")

    page = st.radio(
        "Select View",
        options=[
            "🏠 Overview",
            "👥 Manpower Dashboard",
            "📅 Availability Calendar",
            "🔬 Test Selection",
            "📝 Protocol Entry",
            "📊 Test Results",
            "🧪 Task Assignment Demo"
        ]
    )

    st.markdown("---")
    st.markdown("### 📈 Quick Stats")

    # Display quick stats
    if 'staff_registry' in st.session_state and st.session_state.staff_registry:
        total_staff = len(st.session_state.staff_registry)
        available = sum(1 for s in st.session_state.staff_registry if s['is_available'])
        st.metric("Total Staff", total_staff)
        st.metric("Available", available)

    if 'test_results' in st.session_state and st.session_state.test_results:
        total_tests = len(st.session_state.test_results)
        passed = sum(1 for r in st.session_state.test_results if r['compliance_status'] == 'PASS')
        st.metric("Total Tests", total_tests)
        st.metric("Pass Rate", f"{(passed/total_tests*100):.0f}%" if total_tests > 0 else "0%")

# Main content area
if page == "🏠 Overview":
    st.header("📖 Module Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👥 Manpower Management Features")
        st.markdown("""
        - **Staff Registry**: Comprehensive staff profiles with expertise, certifications, and availability
        - **Performance Metrics**: Quality, speed, and reliability tracking
        - **Workload Analysis**: Real-time capacity and utilization monitoring
        - **Availability Calendar**: Visual scheduling with holidays, shifts, and assignments
        - **Skill-Based Assignment**: Automated task assignment based on expertise
        - **Certification Tracking**: Expiration alerts and compliance monitoring
        """)

        st.success(f"✅ {len(st.session_state.staff_registry)} staff members registered")

    with col2:
        st.markdown("### 🔬 Test Protocol Features")
        st.markdown("""
        - **Test Standards Database**: IEC 61215, IEC 61730, ISO standards
        - **Protocol Templates**: Structured test procedures with steps
        - **Test Selection**: Search and filter test methods
        - **Protocol Entry Sheet**: Guided data entry with validation
        - **Auto-Validation**: Automatic compliance checking
        - **Result Tracking**: Version control and audit trail
        - **Compliance Reporting**: Pass/fail analysis with detailed reports
        """)

        st.success(f"✅ {len(st.session_state.test_standards)} test standards available")
        st.success(f"✅ {len(st.session_state.test_protocols)} protocols defined")

    st.divider()

    st.markdown("### 🚀 Quick Start Guide")

    with st.expander("How to Integrate into app.py", expanded=True):
        st.code("""
# 1. Import the module at the top of app.py
from manpower_protocols_session3 import (
    initialize_manpower_protocols_data,
    render_manpower_dashboard,
    render_availability_calendar,
    render_test_selection,
    render_protocol_entry_sheet,
    render_test_results_table
)

# 2. Initialize data in your session state initialization
initialize_manpower_protocols_data()

# 3. Add tabs or pages for each function
tab1, tab2, tab3 = st.tabs(["Manpower", "Test Protocols", "Results"])

with tab1:
    render_manpower_dashboard()
    render_availability_calendar()

with tab2:
    render_test_selection()
    render_protocol_entry_sheet()

with tab3:
    render_test_results_table()
        """, language="python")

    with st.expander("Sample Data Included"):
        st.markdown("""
        The module comes with sample data for immediate testing:
        - **5 Staff Members**: Diverse roles and expertise levels
        - **3 Test Standards**: IEC 61215 Thermal Cycling, IEC 61215 Humidity Freeze, IEC 61730 Safety
        - **2 Protocol Templates**: Detailed step-by-step procedures
        - **Calendar Events**: Sample holidays, assignments, and training
        """)

elif page == "👥 Manpower Dashboard":
    render_manpower_dashboard()

elif page == "📅 Availability Calendar":
    render_availability_calendar()

elif page == "🔬 Test Selection":
    render_test_selection()

elif page == "📝 Protocol Entry":
    render_protocol_entry_sheet()

elif page == "📊 Test Results":
    render_test_results_table()

elif page == "🧪 Task Assignment Demo":
    st.header("🎯 Automated Task Assignment Demo")

    st.markdown("""
    This demonstrates the skill-based task assignment logic that automatically matches tasks
    to the most suitable staff member based on:
    - Required skills/expertise
    - Current availability
    - Workload/capacity
    - Performance metrics
    """)

    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Define Task")

        with st.form("task_assignment_form"):
            task_name = st.text_input(
                "Task Name*",
                placeholder="e.g., Perform IEC 61215 Thermal Cycling Test"
            )

            required_skills = st.multiselect(
                "Required Skills",
                options=[
                    'IEC 61215 Testing',
                    'Thermal Cycling',
                    'UV Testing',
                    'Humidity Freeze',
                    'Mechanical Load',
                    'Visual Inspection',
                    'Data Analysis',
                    'Quality Control',
                    'All IEC Standards',
                    'ISO Compliance'
                ]
            )

            preferred_staff = st.selectbox(
                "Preferred Staff (Optional)",
                options=['Auto-assign'] + [s['staff_id'] for s in st.session_state.staff_registry],
                format_func=lambda x: x if x == 'Auto-assign' else f"{get_staff_by_id(x)['name']} - {get_staff_by_id(x)['role']}"
            )

            assign_button = st.form_submit_button("Assign Task", type="primary")

            if assign_button:
                if not task_name:
                    st.error("❌ Task name is required")
                else:
                    # Perform assignment
                    preferred_id = None if preferred_staff == 'Auto-assign' else preferred_staff

                    result = assign_task_to_staff(
                        task_name=task_name,
                        required_skills=required_skills if required_skills else None,
                        preferred_staff_id=preferred_id
                    )

                    if result['success']:
                        st.success(f"✅ {result['message']}")

                        if 'score' in result:
                            st.info(f"Match Score: {result['score']:.2f} | Skill Match: {result['skill_match']*100:.0f}%")

                        # Show assigned staff details
                        assigned_staff = get_staff_by_id(result['staff_id'])
                        if assigned_staff:
                            st.markdown("**Assigned to:**")
                            st.json({
                                'Name': assigned_staff['name'],
                                'Role': assigned_staff['role'],
                                'New Load': f"{assigned_staff['current_load']}/{assigned_staff['capacity']}",
                                'Expertise': assigned_staff['expertise_areas']
                            })
                    else:
                        st.error(f"❌ {result['message']}")

    with col2:
        st.subheader("Current Staff Status")

        for staff in st.session_state.staff_registry:
            with st.container():
                col_s1, col_s2, col_s3 = st.columns([2, 1, 1])

                with col_s1:
                    st.markdown(f"**{staff['name']}**")
                    st.caption(staff['role'])

                with col_s2:
                    utilization = (staff['current_load'] / staff['capacity'] * 100) if staff['capacity'] > 0 else 0
                    st.metric("Load", f"{staff['current_load']}/{staff['capacity']}")

                with col_s3:
                    if not staff['is_available']:
                        st.error("Unavailable")
                    elif utilization >= 80:
                        st.warning("High")
                    else:
                        st.success("Available")

                # Show expertise
                st.caption(f"Skills: {', '.join(staff['expertise_areas'][:3])}")

                # Check for expiring certifications
                expiring = check_certification_expiry(staff['staff_id'], days_ahead=60)
                if expiring:
                    st.warning(f"⚠️ {len(expiring)} certification(s) expiring soon")

                st.divider()

# Footer
st.markdown("---")
st.markdown(f"**Module:** {MODULE_ID} | **Version:** 1.0.0 | **Status:** ✅ Production Ready")
