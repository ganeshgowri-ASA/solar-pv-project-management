# Approval Automation System - Quick Start Guide

**Module ID:** `APPROVAL_AUTOMATION_SESSION4`

## 🚀 Quick Start

### Run the Demo Application

```bash
streamlit run demo_approval_integration.py
```

### Run Standalone Module

```bash
streamlit run approval_automation.py
```

## 📁 Files Included

| File | Description |
|------|-------------|
| `approval_automation.py` | Main module with all approval automation functionality |
| `demo_approval_integration.py` | Complete demo application showing integration |
| `APPROVAL_AUTOMATION_README.md` | Comprehensive documentation |
| `APPROVAL_AUTOMATION_QUICKSTART.md` | This quick start guide |

## 🔧 Integration Steps

### Step 1: Import the Module

Add to your `app.py`:

```python
from approval_automation import (
    initialize_approval_automation_state,
    render_approval_dashboard,
    render_approval_form,
    render_automation_rules_panel,
    render_notifications_panel,
    route_for_approval
)
```

### Step 2: Initialize

In your initialization function:

```python
# Call this once during app initialization
initialize_approval_automation_state()
```

### Step 3: Add UI Components

Add anywhere in your Streamlit app:

```python
# Approval Dashboard
render_approval_dashboard()

# Approval Form for reviewers
render_approval_form()

# Automation Rules Management
render_automation_rules_panel()

# Notifications Panel
render_notifications_panel()
```

### Step 4: Route Test Results for Approval

When a test is completed:

```python
# After a test is completed
test_result = {
    'id': 'TEST-001',
    'test_type': 'Solar Panel Efficiency Test',
    'test_date': datetime.now(),
    'result': 'Pass',
    'efficiency': 18.5,
    'technician': 'John Doe',
    'status': 'Completed'
}

# Route for approval
workflow = route_for_approval(test_result)
st.success(f"Approval workflow created: {workflow['approval_id']}")
```

## ✨ Key Features

### 1. Multi-Level Approval Workflow

- **4 Approval Levels**: Technician → QA Manager → Project Manager → Director
- **Digital Signatures**: SHA-256 hash-based signatures for each approval
- **Rejection Workflow**: Allows re-submission with feedback
- **Audit Trail**: Complete logging of all actions

### 2. Automation Rules

Pre-configured automation rules:

```python
# Automatically triggers when:
- Test overdue > 2 days → Alert manager
- Approval pending > 3 days → Escalate to next level
- Critical test failure → Immediate notification
- Weekly schedule → Send summary report
```

### 3. Notification System

- **In-App Notifications**: Real-time in-app alerts
- **Email Integration**: Configurable email notifications
- **Priority Levels**: Critical, High, Medium, Low
- **Action Tracking**: Mark as read/unread, action required flags

## 📊 Sample Data

The module includes sample data:
- ✅ 4 pre-configured automation rules
- ✅ 2 sample notifications
- ✅ Approval level configuration

## 🎯 Common Use Cases

### Create Test Approval

```python
from approval_automation import route_for_approval

test_result = {
    'id': 'TEST-001',
    'test_type': 'Efficiency Test',
    'test_date': datetime.now(),
    'result': 'Pass'
}

workflow = route_for_approval(test_result)
```

### Approve a Test

```python
from approval_automation import process_approval_action

process_approval_action(
    approval_id='APR-0001',
    action='approved',
    reviewer_name='Jane Smith',
    comments='Approved - all tests passed',
    level=1
)
```

### Reject a Test

```python
from approval_automation import process_approval_action

process_approval_action(
    approval_id='APR-0001',
    action='rejected',
    reviewer_name='John Doe',
    comments='Test results incomplete - resubmit with additional data',
    level=2
)
```

### Resubmit After Rejection

```python
from approval_automation import resubmit_for_approval

updated_test_result = {
    'id': 'TEST-001',
    'test_type': 'Efficiency Test',
    'test_date': datetime.now(),
    'result': 'Pass',
    'additional_data': 'New measurements added'
}

resubmit_for_approval(
    approval_id='APR-0001',
    updated_test_result=updated_test_result,
    submitter_comments='Added additional measurement data as requested'
)
```

### Check Notifications

```python
from approval_automation import get_unread_notification_count

unread_count = get_unread_notification_count()
st.write(f"You have {unread_count} unread notifications")
```

### Run Automation Check

```python
from approval_automation import evaluate_automation_rules

# Call periodically (e.g., every hour)
evaluate_automation_rules()
```

## 🔍 Session State Variables

The module uses these session state variables:

```python
st.session_state.approval_workflows        # List of approval workflows
st.session_state.automation_rules          # List of automation rules
st.session_state.notifications             # List of notifications
st.session_state.approval_audit_trail      # List of audit events
st.session_state.notification_preferences  # Notification settings
st.session_state.approval_config           # Approval configuration
```

## ⚙️ Configuration

### Approval Configuration

```python
st.session_state.approval_config = {
    'auto_escalation_days': 3,           # Auto-escalate after 3 days
    'reminder_days': 2,                   # Send reminder after 2 days
    'require_digital_signature': True     # Require digital signatures
}
```

### Notification Preferences

```python
st.session_state.notification_preferences = {
    'in_app': True,                       # Enable in-app notifications
    'email': True,                        # Enable email notifications
    'email_list': [                       # Email recipients
        'manager@solarpv.com',
        'qa@solarpv.com'
    ]
}
```

## 📈 Testing

### Create Test Workflow

```python
from approval_automation import create_test_approval_workflow

# Creates a test workflow with sample data
workflow = create_test_approval_workflow()
```

### View Audit Trail

```python
from approval_automation import get_audit_trail

# Get all audit events
all_events = get_audit_trail()

# Get events for specific approval
approval_events = get_audit_trail(approval_id='APR-0001')

# Get events in date range
from datetime import datetime, timedelta
recent_events = get_audit_trail(
    start_date=datetime.now() - timedelta(days=7)
)
```

## 🎨 UI Components

### Approval Dashboard

```python
render_approval_dashboard()
```

Shows:
- Summary metrics (total, pending, approved, rejected)
- Pending approvals with current level
- Approval history with filtering
- Approval timeline chart
- User action items

### Approval Form

```python
render_approval_form()
```

Provides:
- Select approval to review
- View complete approval details
- View test data and previous approvals
- Approve/Reject/Request Info actions
- Digital signature generation

### Automation Rules Panel

```python
render_automation_rules_panel()
```

Features:
- View all automation rules
- Create new rules
- Enable/disable rules
- Delete rules
- Manual rule evaluation

### Notifications Panel

```python
render_notifications_panel()
```

Includes:
- Summary metrics
- Filter by read/unread, priority
- Sort by date
- Mark as read functionality
- Action required indicators

## 🔐 Security Features

- **Digital Signatures**: SHA-256 hash-based signatures
- **Audit Trail**: Complete logging with timestamps and user info
- **Signature Verification**: `verify_signature()` function
- **User Tracking**: All actions logged with user information

## 📚 Additional Resources

- **Complete Documentation**: See `APPROVAL_AUTOMATION_README.md`
- **Demo Application**: Run `demo_approval_integration.py`
- **Module Source**: See `approval_automation.py`

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Module not initializing | Call `initialize_approval_automation_state()` first |
| Notifications not appearing | Check `st.session_state.notification_preferences` |
| Automation rules not triggering | Call `evaluate_automation_rules()` manually |
| Digital signatures not generating | Verify `require_digital_signature` is True |

## 💡 Tips

1. **Call `initialize_approval_automation_state()` once** during app startup
2. **Use the demo app** to see all features in action
3. **Check session state** to debug issues
4. **Review audit trail** for complete history
5. **Test with sample data** before production use

## 📞 Support

For questions or issues:
1. Check the comprehensive documentation in `APPROVAL_AUTOMATION_README.md`
2. Run the demo application for examples
3. Review the code comments in `approval_automation.py`
4. Check session state variables for data

---

**Version:** 1.0.0
**Module ID:** APPROVAL_AUTOMATION_SESSION4
**Last Updated:** 2025-11-07
