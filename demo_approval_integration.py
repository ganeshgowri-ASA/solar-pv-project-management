"""
APPROVAL AUTOMATION INTEGRATION DEMO
Module ID: APPROVAL_AUTOMATION_SESSION4

This demo script shows how to integrate the approval automation module
with the existing Solar PV Test Project Management application.

Usage:
    streamlit run demo_approval_integration.py
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# Import the approval automation module
from approval_automation import (
    # Initialization
    initialize_approval_automation_state,

    # UI Rendering Functions
    render_approval_dashboard,
    render_approval_form,
    render_automation_rules_panel,
    render_notifications_panel,

    # Core Functions
    route_for_approval,
    process_approval_action,
    resubmit_for_approval,
    evaluate_automation_rules,

    # Notification Functions
    mark_notification_read,
    get_unread_notification_count,

    # Audit Functions
    get_audit_trail,

    # Digital Signature
    generate_digital_signature,
    verify_signature,

    # Test Functions
    create_test_approval_workflow,

    # Constants
    MODULE_ID,
    APPROVAL_LEVELS
)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Approval Automation Demo",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM CSS
# ============================================================================

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
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        border: 1px solid #cccccc;
        padding: 10px;
        border-radius: 5px;
        margin: 5px;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #FF9800;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================================
# INITIALIZATION
# ============================================================================

def init_demo():
    """Initialize the demo application"""
    # Initialize the approval automation module
    initialize_approval_automation_state()

    # Initialize demo-specific session state
    if 'demo_initialized' not in st.session_state:
        st.session_state.demo_initialized = True
        st.session_state.current_user = 'Demo User'
        st.session_state.user_role = 'Admin'


# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.title("☀️ Approval Automation")
        st.markdown(f"**Module ID:** `{MODULE_ID}`")
        st.markdown("---")

        # Notification badge
        unread_count = get_unread_notification_count()
        if unread_count > 0:
            st.markdown(f"🔔 **{unread_count}** unread notifications")
            st.markdown("---")

        # Navigation
        st.header("Navigation")
        page = st.radio("Select Page", [
            "🏠 Home",
            "📋 Approval Dashboard",
            "✍️ Approval Form",
            "⚙️ Automation Rules",
            "🔔 Notifications",
            "📊 Analytics",
            "🧪 Testing & Demo",
            "📚 Documentation"
        ])

        st.markdown("---")

        # Quick Stats
        st.header("Quick Stats")

        pending = len([w for w in st.session_state.approval_workflows if w['status'] == 'pending'])
        approved = len([w for w in st.session_state.approval_workflows if w['status'] == 'approved'])

        st.metric("Pending Approvals", pending)
        st.metric("Approved Today", approved)
        st.metric("Unread Notifications", unread_count)

        st.markdown("---")

        # User Info
        st.header("User Info")
        st.write(f"**User:** {st.session_state.current_user}")
        st.write(f"**Role:** {st.session_state.user_role}")

        return page


# ============================================================================
# HOME PAGE
# ============================================================================

def render_home_page():
    """Render home page with overview"""
    st.title("🏠 Approval Automation System")
    st.markdown("### Multi-Level Approval Workflow & Automation")

    st.markdown("""
    <div class="info-box">
    <h4>Welcome to the Approval Automation System!</h4>
    <p>This module provides comprehensive approval workflow management, automation rules,
    and notifications for the Solar PV Test Project Management application.</p>
    </div>
    """, unsafe_allow_html=True)

    # Feature overview
    st.markdown("---")
    st.header("Key Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 📋 Multi-Level Approvals")
        st.write("- 4-level approval chain")
        st.write("- Technician → QA → PM → Director")
        st.write("- Digital signatures")
        st.write("- Rejection workflow")
        st.write("- Audit trail")

    with col2:
        st.markdown("### ⚙️ Automation Rules")
        st.write("- Trigger-based automation")
        st.write("- Overdue test alerts")
        st.write("- Auto-escalation")
        st.write("- Custom rule creation")
        st.write("- Summary reports")

    with col3:
        st.markdown("### 🔔 Notifications")
        st.write("- In-app notifications")
        st.write("- Email integration")
        st.write("- Priority levels")
        st.write("- Action tracking")
        st.write("- Smart filtering")

    # Approval levels
    st.markdown("---")
    st.header("Approval Levels Configuration")

    levels_df = pd.DataFrame(APPROVAL_LEVELS)
    st.dataframe(levels_df, use_container_width=True, hide_index=True)

    # Quick actions
    st.markdown("---")
    st.header("Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Create Test Approval", use_container_width=True):
            workflow = create_test_approval_workflow()
            st.success(f"✅ Created: {workflow['approval_id']}")
            st.rerun()

    with col2:
        if st.button("Run Automation Check", use_container_width=True):
            evaluate_automation_rules()
            st.success("✅ Automation rules evaluated")
            st.rerun()

    with col3:
        if st.button("Mark All Read", use_container_width=True):
            for notification in st.session_state.notifications:
                notification['read'] = True
            st.success("✅ All notifications marked read")
            st.rerun()

    with col4:
        if st.button("View Documentation", use_container_width=True):
            st.session_state.nav_page = "📚 Documentation"
            st.rerun()


# ============================================================================
# ANALYTICS PAGE
# ============================================================================

def render_analytics_page():
    """Render analytics and reporting page"""
    st.title("📊 Analytics & Reporting")

    # Overall statistics
    st.header("Overall Statistics")

    col1, col2, col3, col4 = st.columns(4)

    total_workflows = len(st.session_state.approval_workflows)
    pending = len([w for w in st.session_state.approval_workflows if w['status'] == 'pending'])
    approved = len([w for w in st.session_state.approval_workflows if w['status'] == 'approved'])
    rejected = len([w for w in st.session_state.approval_workflows if w['status'] == 'rejected'])

    col1.metric("Total Workflows", total_workflows)
    col2.metric("Pending", pending)
    col3.metric("Approved", approved)
    col4.metric("Rejected", rejected)

    # Charts
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Workflow Status", "Automation Performance", "Audit Trail"])

    with tab1:
        if st.session_state.approval_workflows:
            # Status distribution
            status_counts = {
                'Pending': pending,
                'Approved': approved,
                'Rejected': rejected
            }

            import plotly.graph_objects as go

            fig = go.Figure(data=[go.Pie(
                labels=list(status_counts.keys()),
                values=list(status_counts.values()),
                hole=.3
            )])

            fig.update_layout(title="Workflow Status Distribution")
            st.plotly_chart(fig, use_container_width=True)

            # Workflows by test type
            test_types = {}
            for wf in st.session_state.approval_workflows:
                test_type = wf.get('test_type', 'Unknown')
                test_types[test_type] = test_types.get(test_type, 0) + 1

            if test_types:
                fig2 = go.Figure(data=[go.Bar(
                    x=list(test_types.keys()),
                    y=list(test_types.values())
                )])

                fig2.update_layout(title="Workflows by Test Type")
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No workflow data available")

    with tab2:
        if st.session_state.automation_rules:
            # Rule trigger counts
            rule_data = []
            for rule in st.session_state.automation_rules:
                rule_data.append({
                    'Rule': rule['trigger_name'],
                    'Status': rule['status'],
                    'Trigger Count': rule.get('trigger_count', 0),
                    'Last Triggered': rule.get('last_triggered', 'Never')
                })

            df = pd.DataFrame(rule_data)
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Trigger count chart
            fig = go.Figure(data=[go.Bar(
                x=[r['trigger_name'] for r in st.session_state.automation_rules],
                y=[r.get('trigger_count', 0) for r in st.session_state.automation_rules]
            )])

            fig.update_layout(title="Automation Rule Trigger Counts")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No automation rules configured")

    with tab3:
        # Audit trail
        audit_events = get_audit_trail()

        if audit_events:
            st.write(f"**Total Events:** {len(audit_events)}")

            # Recent events
            st.markdown("### Recent Events (Last 10)")
            for event in audit_events[:10]:
                with st.expander(f"{event['action']} - {event['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                    st.write(f"**User:** {event['user']}")
                    st.write(f"**Approval ID:** {event.get('approval_id', 'N/A')}")
                    st.write(f"**Details:** {event['details']}")

            # Export audit trail
            if st.button("Export Audit Trail (CSV)"):
                df = pd.DataFrame(audit_events)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"audit_trail_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("No audit events recorded")


# ============================================================================
# TESTING & DEMO PAGE
# ============================================================================

def render_testing_page():
    """Render testing and demo page"""
    st.title("🧪 Testing & Demo Functions")

    st.markdown("""
    <div class="warning-box">
    <h4>⚠️ Demo Mode</h4>
    <p>This page provides testing functions to demonstrate the approval automation system.
    Use these functions to generate sample data and test workflows.</p>
    </div>
    """, unsafe_allow_html=True)

    # Test functions
    st.header("Test Functions")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Create Test Data")

        if st.button("Create Test Approval Workflow", use_container_width=True):
            workflow = create_test_approval_workflow()
            st.success(f"✅ Created workflow: {workflow['approval_id']}")
            st.json({k: str(v) if isinstance(v, datetime) else v for k, v in workflow.items()})

        if st.button("Create Multiple Test Workflows (5)", use_container_width=True):
            for i in range(5):
                test_result = {
                    'id': f'TEST-{100+i}',
                    'test_type': ['Efficiency Test', 'Durability Test', 'Safety Test', 'Performance Test'][i % 4],
                    'test_date': datetime.now() - timedelta(days=i),
                    'result': 'Pass',
                    'status': 'Completed'
                }
                route_for_approval(test_result)
            st.success("✅ Created 5 test workflows")
            st.rerun()

        if st.button("Trigger Automation Rules", use_container_width=True):
            evaluate_automation_rules()
            st.success("✅ Automation rules evaluated")
            st.rerun()

    with col2:
        st.subheader("Simulate Actions")

        # Approve first pending
        if st.button("Approve First Pending Workflow", use_container_width=True):
            pending = [w for w in st.session_state.approval_workflows if w['status'] == 'pending']
            if pending:
                workflow = pending[0]
                success = process_approval_action(
                    approval_id=workflow['approval_id'],
                    action='approved',
                    reviewer_name='Demo Reviewer',
                    comments='Approved for testing',
                    level=workflow.get('current_level', 1)
                )
                if success:
                    st.success(f"✅ Approved: {workflow['approval_id']}")
                    st.rerun()
            else:
                st.info("No pending workflows to approve")

        # Reject first pending
        if st.button("Reject First Pending Workflow", use_container_width=True):
            pending = [w for w in st.session_state.approval_workflows if w['status'] == 'pending']
            if pending:
                workflow = pending[0]
                success = process_approval_action(
                    approval_id=workflow['approval_id'],
                    action='rejected',
                    reviewer_name='Demo Reviewer',
                    comments='Rejected for testing purposes',
                    level=workflow.get('current_level', 1)
                )
                if success:
                    st.error(f"❌ Rejected: {workflow['approval_id']}")
                    st.rerun()
            else:
                st.info("No pending workflows to reject")

        # Clear all data
        if st.button("⚠️ Clear All Test Data", use_container_width=True):
            st.session_state.approval_workflows = []
            st.session_state.notifications = []
            st.session_state.approval_audit_trail = []
            st.success("✅ All test data cleared")
            st.rerun()

    # Session state viewer
    st.markdown("---")
    st.header("Session State Viewer")

    view_option = st.selectbox("Select Data to View", [
        "Approval Workflows",
        "Automation Rules",
        "Notifications",
        "Audit Trail",
        "Configuration"
    ])

    if view_option == "Approval Workflows":
        st.json([{k: str(v) if isinstance(v, datetime) else v for k, v in w.items()}
                for w in st.session_state.approval_workflows])

    elif view_option == "Automation Rules":
        st.json([{k: str(v) if isinstance(v, datetime) else v for k, v in r.items()}
                for r in st.session_state.automation_rules])

    elif view_option == "Notifications":
        st.json([{k: str(v) if isinstance(v, datetime) else v for k, v in n.items()}
                for n in st.session_state.notifications])

    elif view_option == "Audit Trail":
        st.json([{k: str(v) if isinstance(v, datetime) else v for k, v in e.items()}
                for e in st.session_state.approval_audit_trail])

    elif view_option == "Configuration":
        st.json({
            'approval_config': st.session_state.approval_config,
            'notification_preferences': st.session_state.notification_preferences
        })


# ============================================================================
# DOCUMENTATION PAGE
# ============================================================================

def render_documentation_page():
    """Render documentation page"""
    st.title("📚 Documentation")

    st.markdown("""
    ## Approval Automation System Documentation

    ### Quick Start Guide

    #### 1. Initialize the Module
    ```python
    from approval_automation import initialize_approval_automation_state

    initialize_approval_automation_state()
    ```

    #### 2. Create an Approval Workflow
    ```python
    from approval_automation import route_for_approval

    test_result = {
        'id': 'TEST-001',
        'test_type': 'Solar Panel Efficiency Test',
        'test_date': datetime.now(),
        'result': 'Pass'
    }

    workflow = route_for_approval(test_result)
    ```

    #### 3. Process Approvals
    ```python
    from approval_automation import process_approval_action

    process_approval_action(
        approval_id='APR-0001',
        action='approved',
        reviewer_name='Jane Smith',
        comments='All tests passed',
        level=1
    )
    ```

    #### 4. Render UI Components
    ```python
    from approval_automation import (
        render_approval_dashboard,
        render_approval_form,
        render_automation_rules_panel,
        render_notifications_panel
    )

    # In your Streamlit app
    render_approval_dashboard()
    render_approval_form()
    render_automation_rules_panel()
    render_notifications_panel()
    ```

    ### Integration with Existing App

    To integrate with your existing `app.py`:

    1. **Import the module** at the top of your file
    2. **Initialize** in your init function
    3. **Add UI components** where needed
    4. **Route test results** for approval when tests complete

    See `APPROVAL_AUTOMATION_README.md` for complete documentation.

    ### Approval Levels

    The system uses a 4-level approval hierarchy:

    1. **Technician** - Initial review and technical verification
    2. **QA Manager** - Quality assurance review
    3. **Project Manager** - Project-level approval
    4. **Director** - Final executive approval

    ### Automation Rules

    Pre-configured automation rules:

    - **Test Overdue Alert**: Triggers when tests exceed 2 days
    - **Approval Pending Escalation**: Auto-escalates approvals pending >3 days
    - **Critical Test Failure**: Immediate notification for critical failures
    - **Weekly Summary Report**: Generates weekly project summaries

    ### Digital Signatures

    All approvals include SHA-256 hash-based digital signatures for:

    - Compliance and audit requirements
    - Data integrity verification
    - Non-repudiation

    ### API Reference

    See `APPROVAL_AUTOMATION_README.md` for complete API documentation.
    """)

    # Download documentation
    st.markdown("---")
    st.header("Download Documentation")

    try:
        with open('APPROVAL_AUTOMATION_README.md', 'r') as f:
            readme_content = f.read()

        st.download_button(
            label="📥 Download Complete Documentation (Markdown)",
            data=readme_content,
            file_name="APPROVAL_AUTOMATION_README.md",
            mime="text/markdown"
        )
    except FileNotFoundError:
        st.warning("Documentation file not found. Please ensure APPROVAL_AUTOMATION_README.md is in the same directory.")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point"""
    # Initialize
    init_demo()

    # Render sidebar and get selected page
    page = render_sidebar()

    # Render selected page
    if page == "🏠 Home":
        render_home_page()
    elif page == "📋 Approval Dashboard":
        render_approval_dashboard()
    elif page == "✍️ Approval Form":
        render_approval_form()
    elif page == "⚙️ Automation Rules":
        render_automation_rules_panel()
    elif page == "🔔 Notifications":
        render_notifications_panel()
    elif page == "📊 Analytics":
        render_analytics_page()
    elif page == "🧪 Testing & Demo":
        render_testing_page()
    elif page == "📚 Documentation":
        render_documentation_page()


if __name__ == "__main__":
    main()
