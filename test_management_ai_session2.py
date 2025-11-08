"""
INTELLIGENT TEST MANAGEMENT AI SYSTEM
MODULE_ID: TEST_MANAGEMENT_AI_SESSION2

Production-ready test management system for Solar PV testing labs
Built for integration with the consolidated Solar PV Project Management App
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Any
import io
import base64

# Module identification
MODULE_ID = "TEST_MANAGEMENT_AI_SESSION2"
MODULE_VERSION = "1.0.0"

# Import core modules
from modules.test_management.protocols import ProtocolLibrary
from modules.test_management.sample_tracking import SampleTracker
from modules.test_management.scheduling import AIScheduler
from modules.test_management.test_execution import TestExecutor
from modules.test_management.data_ingestion import DataIngestor
from modules.test_management.equipment import EquipmentManager
from modules.test_management.ai_engine import AIEngine
from modules.test_management.models import (
    TestStandard, SampleStatus, TestStatus, EquipmentStatus, Priority
)


def initialize_test_management():
    """Initialize test management system in session state"""

    if 'test_mgmt_initialized' not in st.session_state:
        # Initialize all components
        st.session_state.protocol_library = ProtocolLibrary()
        st.session_state.sample_tracker = SampleTracker()
        st.session_state.ai_scheduler = AIScheduler()
        st.session_state.test_executor = TestExecutor()
        st.session_state.data_ingestor = DataIngestor()
        st.session_state.equipment_manager = EquipmentManager()
        st.session_state.ai_engine = AIEngine()

        # Load sample data
        load_sample_data()

        st.session_state.test_mgmt_initialized = True


def load_sample_data():
    """Load sample test data for demonstration"""

    # Register sample modules
    for i in range(10):
        st.session_state.sample_tracker.register_sample(
            sample_name=f"PV Module {i+1}",
            sample_type="Module",
            manufacturer=["SunPower", "Trina Solar", "JA Solar", "Canadian Solar"][i % 4],
            model=f"Model-{400+i*10}W",
            batch_number=f"BATCH-2024-{100+i:03d}",
            serial_number=f"SN-{1000+i:04d}",
            quantity=1,
            customer=["ABC Corp", "XYZ Inc", "Solar Farm LLC"][i % 3],
            project_id=f"PROJ-{2024}-{i+1:02d}",
            registered_by="Lab Technician",
            metadata={"rated_power": 400 + i*10}
        )


# ===================== Dashboard =====================

def render_dashboard():
    """Main dashboard with KPIs and overview"""
    st.title("🎯 Test Management Dashboard")
    st.markdown(f"**Module ID:** `{MODULE_ID}` | **Version:** `{MODULE_VERSION}`")

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)

    sample_stats = st.session_state.sample_tracker.get_statistics()
    schedule_stats = st.session_state.ai_scheduler.get_statistics()
    exec_stats = st.session_state.test_executor.get_statistics()
    equipment_stats = st.session_state.equipment_manager.get_statistics()

    with col1:
        st.metric(
            "Total Samples",
            sample_stats['total_samples'],
            delta=f"{sample_stats['by_status'].get('Registered', 0)} new"
        )

    with col2:
        st.metric(
            "Scheduled Tests",
            schedule_stats['by_status'].get('Scheduled', 0),
            delta=f"{schedule_stats['by_status'].get('In Progress', 0)} active"
        )

    with col3:
        st.metric(
            "Completed Tests",
            exec_stats['total_completed_tests'],
            delta=f"{exec_stats['pass_fail_statistics'].get('pass_rate', 0):.1f}% pass rate"
        )

    with col4:
        st.metric(
            "Equipment Status",
            f"{equipment_stats['by_status'].get('Available', 0)}/{equipment_stats['total_equipment']}",
            delta=f"{equipment_stats.get('overdue_calibrations', 0)} cal due"
        )

    st.divider()

    # Charts Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Sample Status Distribution")
        status_data = sample_stats['by_status']
        fig = px.pie(
            values=list(status_data.values()),
            names=list(status_data.keys()),
            title="Sample Distribution by Status"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📅 Test Schedule Timeline")
        schedules = st.session_state.ai_scheduler.get_all_schedules()
        if schedules:
            schedule_df = pd.DataFrame([
                {
                    'Test': s.schedule_id[:12],
                    'Start': s.scheduled_start,
                    'End': s.scheduled_end,
                    'Priority': s.priority.value if hasattr(s.priority, 'value') else s.priority,
                    'Status': s.status.value if hasattr(s.status, 'value') else s.status
                } for s in schedules[:10]
            ])

            fig = px.timeline(
                schedule_df,
                x_start='Start',
                x_end='End',
                y='Test',
                color='Priority',
                title="Upcoming Test Schedule"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No scheduled tests")

    # Charts Row 2
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔧 Equipment Availability")
        eq_status = equipment_stats['by_status']
        fig = go.Figure(data=[go.Bar(
            x=list(eq_status.keys()),
            y=list(eq_status.values()),
            marker_color=['green', 'orange', 'red', 'yellow', 'gray']
        )])
        fig.update_layout(title="Equipment by Status")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("📈 Test Execution Trend")
        # Generate mock trend data
        dates = pd.date_range(end=datetime.now(), periods=7)
        trend_data = pd.DataFrame({
            'Date': dates,
            'Tests Completed': [5, 7, 6, 8, 9, 7, 10]
        })
        fig = px.line(trend_data, x='Date', y='Tests Completed', title="7-Day Test Completion Trend")
        st.plotly_chart(fig, use_container_width=True)


# ===================== Protocol Library =====================

def render_protocol_library():
    """Protocol library management"""
    st.title("📚 Test Protocol Library")

    tabs = st.tabs(["Browse Protocols", "AI Suggestions", "Statistics"])

    with tabs[0]:
        st.subheader("Available Test Protocols")

        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            standard_filter = st.selectbox(
                "Filter by Standard",
                ["All"] + [s.value for s in TestStandard]
            )
        with col2:
            search_query = st.text_input("Search protocols", "")
        with col3:
            st.write("")  # Spacing

        # Get protocols
        protocols = st.session_state.protocol_library.get_all_protocols()

        if standard_filter != "All":
            protocols = [p for p in protocols if p.standard.value == standard_filter]

        if search_query:
            protocols = st.session_state.protocol_library.search_protocols(search_query)

        # Display protocols
        for protocol in protocols:
            with st.expander(f"{protocol.name} ({protocol.standard.value})"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**Description:** {protocol.description}")
                    st.markdown(f"**Version:** {protocol.version}")
                    st.markdown(f"**Duration:** {protocol.estimated_duration} minutes")

                with col2:
                    st.markdown("**Required Equipment:**")
                    for eq in protocol.required_equipment:
                        st.markdown(f"- {eq}")

                st.markdown("**Test Steps:**")
                for step in protocol.steps:
                    st.markdown(f"{step['step']}. {step['description']} ({step['duration']} min)")

    with tabs[1]:
        st.subheader("🤖 AI-Powered Protocol Suggestions")

        sample_type = st.selectbox(
            "Sample Type",
            ["Module", "Cell", "String", "Inverter"]
        )

        reliability_test = st.checkbox("Reliability Testing Required")
        outdoor_use = st.checkbox("Outdoor Use Application")

        if st.button("Get AI Suggestions"):
            requirements = {
                'reliability_test': reliability_test,
                'outdoor_use': outdoor_use
            }

            suggestions = st.session_state.protocol_library.suggest_protocols(
                sample_type,
                requirements
            )

            st.success(f"Found {len(suggestions)} recommended protocols")

            for suggestion in suggestions:
                protocol = suggestion['protocol']
                with st.container():
                    col1, col2 = st.columns([3, 1])

                    with col1:
                        st.markdown(f"### {protocol.name}")
                        st.markdown(f"**Standard:** {protocol.standard.value}")
                        st.markdown(f"**Reason:** {suggestion['reason']}")

                    with col2:
                        st.metric("Confidence", f"{suggestion['confidence']*100:.0f}%")

                    st.divider()

    with tabs[2]:
        st.subheader("📊 Protocol Statistics")

        stats = st.session_state.protocol_library.get_protocol_statistics()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Protocols", stats['total_protocols'])
        with col2:
            st.metric("Active Protocols", stats['active_protocols'])
        with col3:
            st.metric("Avg Duration (min)", f"{stats['avg_duration_minutes']:.0f}")

        st.markdown("**Protocols by Standard:**")
        by_standard = stats['by_standard']
        fig = px.bar(
            x=list(by_standard.keys()),
            y=list(by_standard.values()),
            labels={'x': 'Standard', 'y': 'Count'},
            title="Protocol Distribution by Standard"
        )
        st.plotly_chart(fig, use_container_width=True)


# ===================== Sample Tracking =====================

def render_sample_tracking():
    """Sample tracking with QR codes and chain of custody"""
    st.title("🏷️ Sample Tracking & Chain of Custody")

    tabs = st.tabs(["Register Sample", "Track Samples", "Chain of Custody", "Inventory"])

    with tabs[0]:
        st.subheader("Register New Sample")

        with st.form("register_sample"):
            col1, col2 = st.columns(2)

            with col1:
                sample_name = st.text_input("Sample Name*")
                sample_type = st.selectbox("Sample Type*", ["Module", "Cell", "String", "Inverter"])
                manufacturer = st.text_input("Manufacturer*")
                model = st.text_input("Model*")

            with col2:
                batch_number = st.text_input("Batch Number*")
                serial_number = st.text_input("Serial Number*")
                customer = st.text_input("Customer")
                quantity = st.number_input("Quantity", min_value=1, value=1)

            submitted = st.form_submit_button("Register Sample")

            if submitted:
                if sample_name and manufacturer and model and batch_number and serial_number:
                    sample = st.session_state.sample_tracker.register_sample(
                        sample_name=sample_name,
                        sample_type=sample_type,
                        manufacturer=manufacturer,
                        model=model,
                        batch_number=batch_number,
                        serial_number=serial_number,
                        quantity=quantity,
                        customer=customer,
                        registered_by=st.session_state.get('current_user', 'Lab User')
                    )
                    st.success(f"✅ Sample registered: {sample.sample_id}")

                    # Show QR code
                    st.markdown("**QR Code Generated:**")
                    st.code(sample.sample_id)
                else:
                    st.error("Please fill in all required fields")

    with tabs[1]:
        st.subheader("Track Samples")

        # Search
        search = st.text_input("🔍 Search samples")

        if search:
            samples = st.session_state.sample_tracker.search_samples(search)
        else:
            samples = st.session_state.sample_tracker.get_all_samples()

        # Display samples table
        if samples:
            sample_data = []
            for s in samples:
                sample_data.append({
                    'ID': s.sample_id,
                    'Name': s.sample_name,
                    'Type': s.sample_type,
                    'Manufacturer': s.manufacturer,
                    'Status': s.status.value if hasattr(s.status, 'value') else s.status,
                    'Location': s.current_location,
                    'Customer': s.customer
                })

            df = pd.DataFrame(sample_data)
            st.dataframe(df, use_container_width=True)

            # Sample actions
            selected_sample_id = st.selectbox("Select sample for actions", [s['ID'] for s in sample_data])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Details"):
                    sample = st.session_state.sample_tracker.get_sample(selected_sample_id)
                    if sample:
                        st.json(sample.to_dict())

            with col2:
                new_location = st.text_input("Move to location")
                if st.button("Move Sample") and new_location:
                    success = st.session_state.sample_tracker.move_sample(
                        selected_sample_id,
                        new_location,
                        st.session_state.get('current_user', 'Lab User')
                    )
                    if success:
                        st.success(f"Sample moved to {new_location}")
                        st.rerun()
        else:
            st.info("No samples found")

    with tabs[2]:
        st.subheader("🔗 Blockchain Chain of Custody")

        samples = st.session_state.sample_tracker.get_all_samples()
        if samples:
            selected_id = st.selectbox("Select Sample", [s.sample_id for s in samples])

            chain = st.session_state.sample_tracker.get_chain_of_custody(selected_id)
            integrity = st.session_state.sample_tracker.verify_chain_integrity(selected_id)

            # Integrity check
            if integrity['valid']:
                st.success(f"✅ Chain Integrity Verified ({integrity['total_records']} records)")
            else:
                st.error(f"❌ Chain Integrity Compromised")
                for error in integrity['errors']:
                    st.error(error)

            # Display chain
            st.markdown("**Chain of Custody Records:**")
            for i, record in enumerate(chain):
                with st.expander(f"Record {i+1}: {record.event_type} ({record.timestamp.strftime('%Y-%m-%d %H:%M')})"):
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**From:** {record.from_location}")
                        st.markdown(f"**To:** {record.to_location}")
                        st.markdown(f"**Handled By:** {record.handled_by}")

                    with col2:
                        st.markdown(f"**Hash:** `{record.current_hash[:16]}...`")
                        if record.previous_hash:
                            st.markdown(f"**Prev Hash:** `{record.previous_hash[:16]}...`")

                    if record.notes:
                        st.markdown(f"**Notes:** {record.notes}")

    with tabs[3]:
        st.subheader("📦 Inventory by Location")

        inventory = st.session_state.sample_tracker.get_location_inventory()

        for location, samples in inventory.items():
            with st.expander(f"{location} ({len(samples)} samples)"):
                for sample in samples:
                    st.markdown(f"- **{sample.sample_name}** ({sample.sample_id}) - {sample.status.value if hasattr(sample.status, 'value') else sample.status}")


# ===================== AI Scheduling =====================

def render_ai_scheduling():
    """AI-powered test scheduling"""
    st.title("🤖 AI-Powered Test Scheduling")

    tabs = st.tabs(["Schedule Test", "View Queue", "Calendar", "Analytics"])

    with tabs[0]:
        st.subheader("Schedule New Test")

        with st.form("schedule_test"):
            # Get available samples and protocols
            samples = st.session_state.sample_tracker.get_all_samples()
            protocols = st.session_state.protocol_library.get_all_protocols()

            if samples and protocols:
                col1, col2 = st.columns(2)

                with col1:
                    selected_sample = st.selectbox(
                        "Select Sample",
                        options=[s.sample_id for s in samples],
                        format_func=lambda x: next((s.sample_name for s in samples if s.sample_id == x), x)
                    )

                    selected_protocol = st.selectbox(
                        "Select Protocol",
                        options=[p.protocol_id for p in protocols],
                        format_func=lambda x: next((p.name for p in protocols if p.protocol_id == x), x)
                    )

                with col2:
                    priority = st.selectbox("Priority", ["Critical", "High", "Medium", "Low"])
                    requested_date = st.date_input("Preferred Start Date")

                # Show AI prediction
                protocol = next((p for p in protocols if p.protocol_id == selected_protocol), None)
                if protocol:
                    queue_status = st.session_state.ai_scheduler.get_queue_status()
                    tat_prediction = st.session_state.ai_engine.predict_tat(
                        protocol.estimated_duration,
                        priority,
                        queue_status['total_scheduled']
                    )

                    st.info(f"🤖 AI Prediction: Estimated TAT: {tat_prediction['predicted_tat_hours']:.1f} hours "
                           f"(Confidence: {tat_prediction['confidence_score']*100:.0f}%)")

                submitted = st.form_submit_button("Schedule Test")

                if submitted:
                    sample = next((s for s in samples if s.sample_id == selected_sample), None)
                    protocol_obj = next((p for p in protocols if p.protocol_id == selected_protocol), None)

                    if sample and protocol_obj:
                        priority_enum = Priority(priority)
                        requested_datetime = datetime.combine(requested_date, datetime.min.time())

                        schedule, conflicts = st.session_state.ai_scheduler.schedule_test(
                            sample=sample,
                            protocol=protocol_obj,
                            priority=priority_enum,
                            requested_date=requested_datetime
                        )

                        if conflicts:
                            st.warning(f"⚠️ {len(conflicts)} conflicts detected")
                            for conflict in conflicts:
                                st.error(f"{conflict.conflict_type} conflict: {conflict.resource_id}")
                        else:
                            st.success(f"✅ Test scheduled: {schedule.schedule_id}")
                            st.rerun()
            else:
                st.warning("Please register samples and ensure protocols are loaded")

    with tabs[1]:
        st.subheader("📋 Test Queue")

        queue_status = st.session_state.ai_scheduler.get_queue_status()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Scheduled Tests", queue_status['total_scheduled'])
        with col2:
            st.metric("In Progress", queue_status['in_progress'])
        with col3:
            if queue_status['oldest_scheduled']:
                st.metric("Oldest Test", queue_status['oldest_scheduled'].strftime('%Y-%m-%d'))

        # Display queue
        schedules = st.session_state.ai_scheduler.get_schedules_by_status(TestStatus.SCHEDULED)

        if schedules:
            queue_data = []
            for s in schedules:
                queue_data.append({
                    'ID': s.schedule_id,
                    'Sample': s.sample_id,
                    'Protocol': s.protocol_id,
                    'Priority': s.priority.value if hasattr(s.priority, 'value') else s.priority,
                    'Scheduled Start': s.scheduled_start.strftime('%Y-%m-%d %H:%M'),
                    'Duration (h)': s.estimated_tat
                })

            df = pd.DataFrame(queue_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Queue is empty")

    with tabs[2]:
        st.subheader("📅 Test Calendar")

        # Calendar view (simplified)
        all_schedules = st.session_state.ai_scheduler.get_all_schedules()

        if all_schedules:
            calendar_data = []
            for s in all_schedules:
                calendar_data.append({
                    'Test': s.schedule_id[:12],
                    'Start': s.scheduled_start,
                    'End': s.scheduled_end,
                    'Status': s.status.value if hasattr(s.status, 'value') else s.status
                })

            df = pd.DataFrame(calendar_data)
            fig = px.timeline(df, x_start='Start', x_end='End', y='Test', color='Status')
            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No scheduled tests")

    with tabs[3]:
        st.subheader("📊 Scheduling Analytics")

        stats = st.session_state.ai_scheduler.get_statistics()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Schedule Status Distribution**")
            fig = px.pie(
                values=list(stats['by_status'].values()),
                names=list(stats['by_status'].keys()),
                title="Tests by Status"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**Resource Utilization**")
            st.metric("Total Equipment Bookings", stats['total_equipment_bookings'])
            st.metric("Total Staff Bookings", stats['total_staff_bookings'])
            st.metric("Overdue Tests", stats['overdue_count'])

            if stats['avg_completion_time_hours']:
                st.metric("Avg Completion Time (h)", f"{stats['avg_completion_time_hours']:.1f}")


# ===================== Equipment Management =====================

def render_equipment_management():
    """Equipment monitoring and management"""
    st.title("🔧 Equipment Management")

    tabs = st.tabs(["Equipment List", "Calibration Alerts", "Performance", "Usage Logs"])

    with tabs[0]:
        st.subheader("Equipment Inventory")

        equipment_list = st.session_state.equipment_manager.get_all_equipment()

        if equipment_list:
            eq_data = []
            for eq in equipment_list:
                eq_data.append({
                    'ID': eq.equipment_id,
                    'Name': eq.name,
                    'Type': eq.equipment_type,
                    'Status': eq.status.value if hasattr(eq.status, 'value') else eq.status,
                    'Location': eq.location,
                    'Usage (h)': f"{eq.usage_hours:.1f}",
                    'Cal Due': eq.calibration_due_date.strftime('%Y-%m-%d')
                })

            df = pd.DataFrame(eq_data)

            # Color code status
            def highlight_status(row):
                if row['Status'] == 'Available':
                    return ['background-color: lightgreen'] * len(row)
                elif row['Status'] == 'In Use':
                    return ['background-color: lightyellow'] * len(row)
                elif row['Status'] == 'Maintenance':
                    return ['background-color: lightcoral'] * len(row)
                return [''] * len(row)

            st.dataframe(df, use_container_width=True)

        else:
            st.info("No equipment registered")

    with tabs[1]:
        st.subheader("⚠️ Calibration Alerts")

        days_threshold = st.slider("Alert threshold (days)", 7, 90, 30)

        alerts = st.session_state.equipment_manager.get_calibration_alerts(days_threshold)

        if alerts:
            for alert in alerts:
                if alert['status'] == 'OVERDUE':
                    st.error(f"🔴 {alert['equipment_name']}: OVERDUE by {abs(alert['days_until_due'])} days")
                else:
                    st.warning(f"🟡 {alert['equipment_name']}: Due in {alert['days_until_due']} days")
        else:
            st.success("✅ All equipment calibrations are current")

    with tabs[2]:
        st.subheader("📊 Equipment Performance")

        equipment_list = st.session_state.equipment_manager.get_all_equipment()

        if equipment_list:
            selected_eq = st.selectbox(
                "Select Equipment",
                options=[eq.equipment_id for eq in equipment_list],
                format_func=lambda x: next((eq.name for eq in equipment_list if eq.equipment_id == x), x)
            )

            performance = st.session_state.equipment_manager.get_equipment_performance(selected_eq)

            if 'error' not in performance:
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Usage", f"{performance['total_usage_hours']:.1f} h")
                with col2:
                    st.metric("Utilization Rate", f"{performance['utilization_rate_percent']:.1f}%")
                with col3:
                    st.metric("Usage Sessions", performance['total_usage_sessions'])
                with col4:
                    st.metric("Cal Status", performance['calibration_status'])

                st.divider()

                st.markdown("**Performance Metrics:**")
                for key, value in performance.get('performance_metrics', {}).items():
                    st.markdown(f"- **{key}:** {value}")

    with tabs[3]:
        st.subheader("📝 Usage Logs")

        equipment_list = st.session_state.equipment_manager.get_all_equipment()

        if equipment_list:
            selected_eq = st.selectbox(
                "Select Equipment for logs",
                options=[eq.equipment_id for eq in equipment_list],
                format_func=lambda x: next((eq.name for eq in equipment_list if eq.equipment_id == x), x),
                key="usage_logs_eq"
            )

            stats = st.session_state.equipment_manager.get_usage_statistics(selected_eq, days=30)

            if 'error' not in stats:
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Sessions (30 days)", stats['total_sessions'])
                with col2:
                    st.metric("Total Hours", f"{stats['total_usage_hours']:.1f}")
                with col3:
                    st.metric("Avg Session", f"{stats['avg_session_duration_hours']:.1f} h")


# ===================== Main Module Entry Point =====================

def main():
    """Main entry point for Test Management AI module"""

    # Initialize system
    initialize_test_management()

    # Page navigation
    st.sidebar.title(f"🧪 Test Management AI")
    st.sidebar.markdown(f"**Module:** `{MODULE_ID}`")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Protocol Library",
            "Sample Tracking",
            "AI Scheduling",
            "Equipment Management"
        ]
    )

    st.sidebar.divider()

    # System stats in sidebar
    st.sidebar.markdown("**Quick Stats**")
    sample_stats = st.session_state.sample_tracker.get_statistics()
    st.sidebar.metric("Samples", sample_stats['total_samples'])

    schedule_stats = st.session_state.ai_scheduler.get_statistics()
    st.sidebar.metric("Scheduled", schedule_stats['by_status'].get('Scheduled', 0))

    # Route to selected page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Protocol Library":
        render_protocol_library()
    elif page == "Sample Tracking":
        render_sample_tracking()
    elif page == "AI Scheduling":
        render_ai_scheduling()
    elif page == "Equipment Management":
        render_equipment_management()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Test Management AI",
        page_icon="🧪",
        layout="wide"
    )
    main()
