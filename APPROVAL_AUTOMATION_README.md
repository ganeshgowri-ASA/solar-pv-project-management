# Approval Automation & Notification System

**Module ID:** `APPROVAL_AUTOMATION_SESSION4`

## Overview

This module provides a comprehensive multi-level approval workflow system with automation rules engine and notification management for the Solar PV Test Project Management application.

## Features

### 1. Multi-Level Approval Workflow
- **Approval Levels**: Technician → QA Manager → Project Manager → Director
- **Workflow Routing Engine**: Automatically routes test results through approval chain
- **Digital Signatures**: Hash-based signature system for compliance
- **Rejection Workflow**: Allows re-submission with feedback
- **Audit Trail**: Complete logging of all approval actions

### 2. Automation Rules Engine
- **Trigger-based Rules**: Define conditions and actions
- **Pre-configured Rules**:
  - Test Overdue Alert (>2 days)
  - Approval Pending Escalation (>3 days)
  - Critical Test Failure Notification
  - Weekly Summary Reports
- **Custom Rule Creation**: Build your own automation rules

### 3. Notification System
- **In-App Notifications**: Real-time notifications in the application
- **Email Support**: Configurable email notifications
- **Priority Levels**: Critical, High, Medium, Low
- **Action Tracking**: Mark notifications as read/unread
- **Smart Filtering**: Filter by status, priority, and type

## Installation & Integration

### Option 1: Standalone Application

Run the module as a standalone Streamlit app:

```bash
streamlit run approval_automation.py
```

### Option 2: Integration with Main App

To integrate with your existing `app.py`, add the following code:

```python
# At the top of app.py, import the module
from approval_automation import (
    initialize_approval_automation_state,
    render_approval_dashboard,
    render_approval_form,
    render_automation_rules_panel,
    render_notifications_panel,
    route_for_approval,
    evaluate_automation_rules
)

# In your initialization function, call:
initialize_approval_automation_state()

# In your UI where you want to display approvals:
render_approval_dashboard()

# In your UI where you want the approval form:
render_approval_form()

# For automation rules:
render_automation_rules_panel()

# For notifications:
render_notifications_panel()

# When a test result needs approval:
test_result = {
    'id': 'TEST-001',
    'test_type': 'Solar Panel Efficiency Test',
    'result': 'Pass',
    'test_date': datetime.now()
}
workflow = route_for_approval(test_result)
```

## API Reference

### Core Functions

#### `initialize_approval_automation_state()`
Initialize all session state variables required by the module.

```python
initialize_approval_automation_state()
```

#### `route_for_approval(test_result, approval_config=None)`
Route a test result through the multi-level approval workflow.

**Parameters:**
- `test_result` (Dict): Test result data to be approved
- `approval_config` (Dict, optional): Configuration for approval routing

**Returns:**
- `Dict`: Created approval workflow record

**Example:**
```python
test_result = {
    'id': 'TEST-001',
    'test_type': 'Solar Panel Efficiency Test',
    'test_date': datetime.now(),
    'result': 'Pass',
    'technician': 'John Doe'
}

workflow = route_for_approval(test_result)
print(f"Created workflow: {workflow['approval_id']}")
```

#### `process_approval_action(approval_id, action, reviewer_name, comments='', level=1)`
Process an approval action (approve/reject/request_info).

**Parameters:**
- `approval_id` (str): ID of the approval workflow
- `action` (str): Action to take ('approved', 'rejected', 'request_info')
- `reviewer_name` (str): Name of the reviewer
- `comments` (str, optional): Comments from reviewer
- `level` (int): Current approval level

**Returns:**
- `bool`: True if action processed successfully

**Example:**
```python
success = process_approval_action(
    approval_id='APR-0001',
    action='approved',
    reviewer_name='Jane Smith',
    comments='All tests passed successfully',
    level=1
)
```

#### `resubmit_for_approval(approval_id, updated_test_result, submitter_comments='')`
Resubmit a rejected test result for approval.

**Parameters:**
- `approval_id` (str): Original approval ID
- `updated_test_result` (Dict): Updated test result data
- `submitter_comments` (str, optional): Comments about changes made

**Returns:**
- `bool`: True if resubmitted successfully

### UI Rendering Functions

#### `render_approval_dashboard()`
Render the approval dashboard showing pending approvals and history.

**Features:**
- Summary metrics (Total, Pending, Approved, Rejected)
- Pending approvals with current level
- Approval history with filtering
- Approval timeline visualization
- User action items

#### `render_approval_form()`
Render approval form for reviewers to approve/reject with comments.

**Features:**
- Select approval to review
- View complete approval details
- View test data
- View previous approvals in chain
- Approve/Reject/Request Info actions
- Digital signature generation

#### `render_automation_rules_panel()`
Render automation rules management panel.

**Features:**
- View all automation rules
- Create new rules
- Enable/disable rules
- Delete rules
- Manual rule evaluation trigger

#### `render_notifications_panel()`
Render notifications panel with read/unread tracking.

**Features:**
- Summary metrics
- Filter by read/unread status
- Filter by priority
- Sort by date
- Mark as read functionality
- Action required indicators

### Automation Functions

#### `evaluate_automation_rules()`
Evaluate all active automation rules and trigger actions.

**Example:**
```python
# Call periodically (e.g., every hour)
evaluate_automation_rules()
```

### Notification Functions

#### `mark_notification_read(notification_id)`
Mark a notification as read.

**Parameters:**
- `notification_id` (str): ID of notification to mark as read

**Returns:**
- `bool`: True if successful

#### `get_unread_notification_count()`
Get count of unread notifications.

**Returns:**
- `int`: Count of unread notifications

### Digital Signature Functions

#### `generate_digital_signature(data, reviewer_name, timestamp)`
Generate a hash-based digital signature for compliance.

**Parameters:**
- `data` (Dict): Approval data to sign
- `reviewer_name` (str): Name of the reviewer
- `timestamp` (datetime): Timestamp of the signature

**Returns:**
- `str`: SHA-256 hash signature

#### `verify_signature(approval_data)`
Verify the integrity of a digital signature.

**Parameters:**
- `approval_data` (Dict): Approval data containing signature

**Returns:**
- `bool`: True if signature is valid

### Audit Functions

#### `get_audit_trail(approval_id=None, start_date=None, end_date=None)`
Retrieve audit trail with optional filtering.

**Parameters:**
- `approval_id` (str, optional): Filter by approval ID
- `start_date` (datetime, optional): Filter by start date
- `end_date` (datetime, optional): Filter by end date

**Returns:**
- `List[Dict]`: List of audit events

## Data Structures

### Approval Workflow
```python
{
    'approval_id': 'APR-0001',
    'test_result_id': 'TEST-001',
    'test_type': 'Solar Panel Efficiency Test',
    'current_level': 1,
    'total_levels': 4,
    'status': 'pending',  # pending, approved, rejected, info_requested
    'created_date': datetime,
    'created_by': 'User Name',
    'approval_chain': [...],
    'test_data': {...},
    'escalation_date': datetime,
    'module_id': 'APPROVAL_AUTOMATION_SESSION4'
}
```

### Approval Record
```python
{
    'approval_id': 'APR-0001',
    'test_result_id': 'TEST-001',
    'reviewer_name': 'Jane Smith',
    'level': 1,
    'role': 'Technician',
    'status': 'approved',  # approved, rejected, request_info
    'comments': 'All tests passed',
    'timestamp': datetime,
    'signature_hash': 'abc123...'
}
```

### Automation Rule
```python
{
    'id': 'uuid',
    'trigger_name': 'Test Overdue Alert',
    'condition': 'test_overdue > 2 days',
    'action': 'alert_manager',
    'status': 'Active',  # Active, Inactive
    'created_date': datetime,
    'last_triggered': datetime,
    'trigger_count': 12
}
```

### Notification
```python
{
    'id': 'uuid',
    'type': 'Approval Required',
    'title': 'Test Result Approval Needed',
    'message': 'Solar panel efficiency test requires your approval',
    'priority': 'High',  # Critical, High, Medium, Low
    'timestamp': datetime,
    'read': False,
    'action_required': True,
    'related_id': 'TEST-001'
}
```

## Session State Variables

The module uses the following session state variables:

- `st.session_state.approval_workflows`: List of approval workflows
- `st.session_state.automation_rules`: List of automation rules
- `st.session_state.notifications`: List of notifications
- `st.session_state.approval_audit_trail`: List of audit events
- `st.session_state.notification_preferences`: Notification settings
- `st.session_state.approval_config`: Approval configuration

## Configuration

### Approval Configuration
```python
st.session_state.approval_config = {
    'auto_escalation_days': 3,      # Auto-escalate after N days
    'reminder_days': 2,              # Send reminder after N days
    'require_digital_signature': True  # Require signatures
}
```

### Notification Preferences
```python
st.session_state.notification_preferences = {
    'in_app': True,
    'email': True,
    'email_list': ['manager@solarpv.com', 'qa@solarpv.com']
}
```

## Sample Data

The module automatically initializes with sample data including:
- 4 pre-configured automation rules
- 2 sample notifications
- Approval level configuration

## Usage Examples

### Example 1: Create Approval Workflow for Test Result

```python
import streamlit as st
from datetime import datetime
from approval_automation import initialize_approval_automation_state, route_for_approval

# Initialize
initialize_approval_automation_state()

# Create test result
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

### Example 2: Process Approval

```python
from approval_automation import process_approval_action

success = process_approval_action(
    approval_id='APR-0001',
    action='approved',
    reviewer_name='Jane Smith',
    comments='Test results look good. Approved.',
    level=1
)

if success:
    st.success("Approval processed successfully!")
```

### Example 3: Create Custom Automation Rule

```python
import uuid
from datetime import datetime

new_rule = {
    'id': str(uuid.uuid4()),
    'trigger_name': 'Daily Test Summary',
    'condition': 'schedule = daily',
    'action': 'send_summary_report',
    'status': 'Active',
    'created_date': datetime.now(),
    'last_triggered': None,
    'trigger_count': 0
}

st.session_state.automation_rules.append(new_rule)
st.success("New automation rule created!")
```

### Example 4: Send Notification

```python
from approval_automation import _create_notification

_create_notification(
    notification_type='Alert',
    title='Test Equipment Calibration Due',
    message='Solar panel tester calibration is due next week',
    priority='Medium',
    related_id='EQUIP-001',
    action_required=True
)
```

### Example 5: Query Audit Trail

```python
from approval_automation import get_audit_trail
from datetime import datetime, timedelta

# Get last 7 days of audit events
start_date = datetime.now() - timedelta(days=7)
audit_events = get_audit_trail(start_date=start_date)

for event in audit_events:
    st.write(f"{event['timestamp']}: {event['action']} by {event['user']}")
    st.write(f"Details: {event['details']}")
```

## Testing

### Run Standalone Module

```bash
streamlit run approval_automation.py
```

This will launch the module interface with test functions available.

### Test Functions

```python
from approval_automation import create_test_approval_workflow

# Create a test approval workflow with sample data
workflow = create_test_approval_workflow()
print(f"Test workflow created: {workflow['approval_id']}")
```

## Error Handling

The module includes comprehensive error handling:
- All functions have try-except blocks
- Errors are logged using Python's logging module
- User-friendly error messages displayed in UI
- Audit trail for debugging

## Logging

The module uses Python's standard logging:

```python
import logging
logger = logging.getLogger('APPROVAL_AUTOMATION_SESSION4')
logger.info("Approval workflow created")
logger.error("Error processing approval")
```

## Security Considerations

1. **Digital Signatures**: SHA-256 hash-based signatures for approval integrity
2. **Audit Trail**: Complete logging of all actions with timestamps and user info
3. **Signature Verification**: `verify_signature()` function to validate approval data
4. **User Authentication**: Integrates with session_state user management

## Performance

- Efficient data structures using Python dictionaries and lists
- Session state for fast in-memory operations
- Minimal external dependencies
- Optimized for Streamlit's caching mechanisms

## Dependencies

```
streamlit
pandas
numpy
plotly
```

All dependencies are included in the project's `requirements.txt`.

## Future Enhancements

Potential improvements for future versions:
- Database persistence (SQLite, PostgreSQL)
- Advanced email integration (SendGrid, AWS SES)
- SMS notifications
- Role-based access control (RBAC)
- Custom approval level configuration
- Advanced reporting and analytics
- Integration with external project management tools
- Mobile app notifications

## Troubleshooting

### Issue: Module not initializing
**Solution:** Ensure `initialize_approval_automation_state()` is called before using any functions.

### Issue: Notifications not appearing
**Solution:** Check that notification preferences are enabled in `st.session_state.notification_preferences`.

### Issue: Automation rules not triggering
**Solution:** Call `evaluate_automation_rules()` periodically or manually trigger from the UI.

### Issue: Digital signatures not generating
**Solution:** Verify `require_digital_signature` is True in `st.session_state.approval_config`.

## Support

For issues, questions, or contributions:
- Check the documentation
- Review the code comments
- Test with the standalone module first
- Check session state variables

## License

Part of the Solar PV Test Project Management System.

## Version

**Version:** 1.0.0
**Module ID:** APPROVAL_AUTOMATION_SESSION4
**Last Updated:** 2025-11-07
