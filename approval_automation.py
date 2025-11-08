"""
APPROVAL AUTOMATION & NOTIFICATION SYSTEM
Module ID: APPROVAL_AUTOMATION_SESSION4

This module provides a comprehensive multi-level approval workflow system
with automation rules engine and notification management for solar PV test
project management.

Features:
- Multi-level approval workflow (Technician -> QA Manager -> Project Manager -> Director)
- Workflow routing engine
- Digital signatures with hash-based compliance
- Automation rules and trigger engine
- Notification system (in-app + email)
- Escalation logic
- Audit trail and logging
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import uuid
import json
import logging
from typing import Dict, List, Optional, Any
import plotly.express as px
import plotly.graph_objects as go

# Module Constants
MODULE_ID = 'APPROVAL_AUTOMATION_SESSION4'

# Approval Levels Configuration
APPROVAL_LEVELS = [
    {'level': 1, 'role': 'Technician', 'name': 'Field Technician'},
    {'level': 2, 'role': 'QA Manager', 'name': 'Quality Assurance Manager'},
    {'level': 3, 'role': 'Project Manager', 'name': 'Project Manager'},
    {'level': 4, 'role': 'Director', 'name': 'Engineering Director'}
]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(MODULE_ID)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def initialize_approval_automation_state():
    """Initialize session state variables for approval automation system"""
    defaults = {
        'approval_workflows': [],
        'automation_rules': [],
        'notifications': [],
        'approval_audit_trail': [],
        'notification_preferences': {
            'in_app': True,
            'email': True,
            'email_list': ['manager@solarpv.com', 'qa@solarpv.com']
        },
        'approval_config': {
            'auto_escalation_days': 3,
            'reminder_days': 2,
            'require_digital_signature': True
        }
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # Initialize sample data if needed
    if not st.session_state.get('approval_automation_initialized', False):
        _initialize_sample_data()
        st.session_state.approval_automation_initialized = True


def _initialize_sample_data():
    """Initialize sample automation rules and test data"""

    # Sample Automation Rules
    sample_rules = [
        {
            'id': str(uuid.uuid4()),
            'trigger_name': 'Test Overdue Alert',
            'condition': 'test_overdue > 2 days',
            'action': 'alert_manager',
            'status': 'Active',
            'created_date': datetime.now() - timedelta(days=30),
            'last_triggered': datetime.now() - timedelta(hours=5),
            'trigger_count': 12
        },
        {
            'id': str(uuid.uuid4()),
            'trigger_name': 'Approval Pending Escalation',
            'condition': 'approval_pending > 3 days',
            'action': 'escalate_to_next_level',
            'status': 'Active',
            'created_date': datetime.now() - timedelta(days=25),
            'last_triggered': datetime.now() - timedelta(hours=8),
            'trigger_count': 8
        },
        {
            'id': str(uuid.uuid4()),
            'trigger_name': 'Critical Test Failure',
            'condition': 'test_result = Failed AND priority = Critical',
            'action': 'immediate_notification',
            'status': 'Active',
            'created_date': datetime.now() - timedelta(days=20),
            'last_triggered': datetime.now() - timedelta(days=2),
            'trigger_count': 3
        },
        {
            'id': str(uuid.uuid4()),
            'trigger_name': 'Weekly Summary Report',
            'condition': 'schedule = weekly',
            'action': 'send_summary_report',
            'status': 'Active',
            'created_date': datetime.now() - timedelta(days=15),
            'last_triggered': datetime.now() - timedelta(days=7),
            'trigger_count': 2
        }
    ]

    if not st.session_state.automation_rules:
        st.session_state.automation_rules = sample_rules

    # Sample notifications
    sample_notifications = [
        {
            'id': str(uuid.uuid4()),
            'type': 'Approval Required',
            'title': 'Test Result Approval Needed',
            'message': 'Solar panel efficiency test requires your approval',
            'priority': 'High',
            'timestamp': datetime.now() - timedelta(hours=2),
            'read': False,
            'action_required': True,
            'related_id': 'TEST-001'
        },
        {
            'id': str(uuid.uuid4()),
            'type': 'Alert',
            'title': 'Test Overdue',
            'message': 'Module thermal testing is 3 days overdue',
            'priority': 'Critical',
            'timestamp': datetime.now() - timedelta(hours=5),
            'read': False,
            'action_required': True,
            'related_id': 'TEST-002'
        }
    ]

    if not st.session_state.notifications:
        st.session_state.notifications = sample_notifications

    logger.info(f"{MODULE_ID}: Sample data initialized successfully")


# ============================================================================
# DIGITAL SIGNATURE SYSTEM
# ============================================================================

def generate_digital_signature(data: Dict[str, Any], reviewer_name: str, timestamp: datetime) -> str:
    """
    Generate a hash-based digital signature for compliance

    Args:
        data: The approval data to sign
        reviewer_name: Name of the reviewer
        timestamp: Timestamp of the signature

    Returns:
        SHA-256 hash signature
    """
    try:
        # Create signature payload
        signature_data = {
            'reviewer': reviewer_name,
            'timestamp': timestamp.isoformat(),
            'data': json.dumps(data, sort_keys=True, default=str)
        }

        # Generate hash
        signature_string = json.dumps(signature_data, sort_keys=True)
        signature_hash = hashlib.sha256(signature_string.encode()).hexdigest()

        logger.info(f"Digital signature generated for {reviewer_name}")
        return signature_hash

    except Exception as e:
        logger.error(f"Error generating digital signature: {str(e)}")
        raise


def verify_signature(approval_data: Dict[str, Any]) -> bool:
    """
    Verify the integrity of a digital signature

    Args:
        approval_data: Approval data containing signature

    Returns:
        True if signature is valid, False otherwise
    """
    try:
        if 'signature_hash' not in approval_data:
            return False

        # Reconstruct signature
        data_copy = approval_data.copy()
        original_hash = data_copy.pop('signature_hash')

        signature_data = {
            'reviewer': approval_data.get('reviewer_name'),
            'timestamp': approval_data.get('timestamp').isoformat() if isinstance(approval_data.get('timestamp'), datetime) else approval_data.get('timestamp'),
            'data': json.dumps({k: v for k, v in data_copy.items() if k != 'signature_hash'}, sort_keys=True, default=str)
        }

        signature_string = json.dumps(signature_data, sort_keys=True)
        computed_hash = hashlib.sha256(signature_string.encode()).hexdigest()

        return original_hash == computed_hash

    except Exception as e:
        logger.error(f"Error verifying signature: {str(e)}")
        return False


# ============================================================================
# APPROVAL WORKFLOW ENGINE
# ============================================================================

def route_for_approval(test_result: Dict[str, Any], approval_config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Route a test result through the multi-level approval workflow

    Args:
        test_result: Test result data to be approved
        approval_config: Optional configuration for approval routing

    Returns:
        Created approval workflow record
    """
    try:
        if approval_config is None:
            approval_config = st.session_state.get('approval_config', {})

        # Generate unique approval ID
        approval_id = f"APR-{len(st.session_state.approval_workflows) + 1:04d}"

        # Create approval workflow
        approval_workflow = {
            'approval_id': approval_id,
            'test_result_id': test_result.get('id', test_result.get('test_id', 'Unknown')),
            'test_type': test_result.get('test_type', 'General Test'),
            'current_level': 1,
            'total_levels': len(APPROVAL_LEVELS),
            'status': 'pending',
            'created_date': datetime.now(),
            'created_by': st.session_state.get('current_user', 'System'),
            'approval_chain': [],
            'test_data': test_result,
            'escalation_date': datetime.now() + timedelta(days=approval_config.get('auto_escalation_days', 3)),
            'module_id': MODULE_ID
        }

        # Add to session state
        st.session_state.approval_workflows.append(approval_workflow)

        # Log to audit trail
        _log_audit_event(
            approval_id=approval_id,
            action='CREATED',
            user=st.session_state.get('current_user', 'System'),
            details=f"Approval workflow created for test {test_result.get('id', 'Unknown')}"
        )

        # Create notification for first approver
        first_approver = APPROVAL_LEVELS[0]
        _create_notification(
            notification_type='Approval Required',
            title=f'New Approval: {test_result.get("test_type", "Test")}',
            message=f'Test result requires {first_approver["role"]} approval',
            priority='Medium',
            related_id=approval_id,
            action_required=True
        )

        logger.info(f"Approval workflow {approval_id} created for test {test_result.get('id')}")
        return approval_workflow

    except Exception as e:
        logger.error(f"Error routing approval: {str(e)}")
        raise


def process_approval_action(approval_id: str, action: str, reviewer_name: str,
                           comments: str = "", level: int = 1) -> bool:
    """
    Process an approval action (approve/reject/request_info)

    Args:
        approval_id: ID of the approval workflow
        action: Action to take ('approved', 'rejected', 'request_info')
        reviewer_name: Name of the reviewer
        comments: Optional comments
        level: Current approval level

    Returns:
        True if action processed successfully
    """
    try:
        # Find the approval workflow
        workflow = None
        workflow_index = None
        for idx, wf in enumerate(st.session_state.approval_workflows):
            if wf['approval_id'] == approval_id:
                workflow = wf
                workflow_index = idx
                break

        if not workflow:
            logger.error(f"Approval workflow {approval_id} not found")
            return False

        timestamp = datetime.now()

        # Create approval record
        approval_record = {
            'approval_id': approval_id,
            'test_result_id': workflow['test_result_id'],
            'reviewer_name': reviewer_name,
            'level': level,
            'role': APPROVAL_LEVELS[level - 1]['role'] if level <= len(APPROVAL_LEVELS) else 'Unknown',
            'status': action,
            'comments': comments,
            'timestamp': timestamp,
            'signature_hash': None
        }

        # Generate digital signature if required
        if st.session_state.approval_config.get('require_digital_signature', True):
            approval_record['signature_hash'] = generate_digital_signature(
                approval_record,
                reviewer_name,
                timestamp
            )

        # Add to approval chain
        workflow['approval_chain'].append(approval_record)

        # Process based on action
        if action == 'approved':
            if level < workflow['total_levels']:
                # Move to next level
                workflow['current_level'] = level + 1
                workflow['status'] = 'pending'

                # Notify next approver
                next_approver = APPROVAL_LEVELS[level]
                _create_notification(
                    notification_type='Approval Required',
                    title=f'Approval Escalated: {workflow["test_type"]}',
                    message=f'Test result requires {next_approver["role"]} approval',
                    priority='Medium',
                    related_id=approval_id,
                    action_required=True
                )

                _log_audit_event(
                    approval_id=approval_id,
                    action='APPROVED',
                    user=reviewer_name,
                    details=f"Level {level} approved, escalated to level {level + 1}"
                )
            else:
                # Final approval
                workflow['status'] = 'approved'
                workflow['completed_date'] = timestamp

                _create_notification(
                    notification_type='Approval Complete',
                    title=f'Fully Approved: {workflow["test_type"]}',
                    message=f'Test result has completed all approval levels',
                    priority='Low',
                    related_id=approval_id,
                    action_required=False
                )

                _log_audit_event(
                    approval_id=approval_id,
                    action='COMPLETED',
                    user=reviewer_name,
                    details=f"All levels approved - workflow complete"
                )

        elif action == 'rejected':
            workflow['status'] = 'rejected'
            workflow['completed_date'] = timestamp
            workflow['rejection_level'] = level

            # Notify submitter about rejection
            _create_notification(
                notification_type='Approval Rejected',
                title=f'Rejected: {workflow["test_type"]}',
                message=f'Test result rejected at {APPROVAL_LEVELS[level-1]["role"]} level. Comments: {comments}',
                priority='High',
                related_id=approval_id,
                action_required=True
            )

            _log_audit_event(
                approval_id=approval_id,
                action='REJECTED',
                user=reviewer_name,
                details=f"Rejected at level {level}. Reason: {comments}"
            )

        elif action == 'request_info':
            workflow['status'] = 'info_requested'

            _create_notification(
                notification_type='Information Requested',
                title=f'Info Required: {workflow["test_type"]}',
                message=f'Additional information requested: {comments}',
                priority='Medium',
                related_id=approval_id,
                action_required=True
            )

            _log_audit_event(
                approval_id=approval_id,
                action='INFO_REQUESTED',
                user=reviewer_name,
                details=f"Information requested at level {level}: {comments}"
            )

        # Update workflow in session state
        st.session_state.approval_workflows[workflow_index] = workflow

        logger.info(f"Approval action '{action}' processed for {approval_id} by {reviewer_name}")
        return True

    except Exception as e:
        logger.error(f"Error processing approval action: {str(e)}")
        return False


def resubmit_for_approval(approval_id: str, updated_test_result: Dict[str, Any],
                          submitter_comments: str = "") -> bool:
    """
    Resubmit a rejected test result for approval

    Args:
        approval_id: Original approval ID
        updated_test_result: Updated test result data
        submitter_comments: Comments from submitter about changes

    Returns:
        True if resubmitted successfully
    """
    try:
        # Find original workflow
        original_workflow = None
        for wf in st.session_state.approval_workflows:
            if wf['approval_id'] == approval_id:
                original_workflow = wf
                break

        if not original_workflow or original_workflow['status'] != 'rejected':
            logger.error(f"Cannot resubmit approval {approval_id}")
            return False

        # Create new approval workflow
        new_workflow = route_for_approval(updated_test_result)
        new_workflow['resubmission'] = True
        new_workflow['original_approval_id'] = approval_id
        new_workflow['resubmission_comments'] = submitter_comments

        # Log resubmission
        _log_audit_event(
            approval_id=new_workflow['approval_id'],
            action='RESUBMITTED',
            user=st.session_state.get('current_user', 'System'),
            details=f"Resubmitted after rejection (original: {approval_id}). Changes: {submitter_comments}"
        )

        logger.info(f"Test result resubmitted as {new_workflow['approval_id']}")
        return True

    except Exception as e:
        logger.error(f"Error resubmitting approval: {str(e)}")
        return False


# ============================================================================
# AUTOMATION RULES ENGINE
# ============================================================================

def evaluate_automation_rules():
    """
    Evaluate all active automation rules and trigger actions
    """
    try:
        active_rules = [r for r in st.session_state.automation_rules if r['status'] == 'Active']

        for rule in active_rules:
            condition = rule['condition']

            # Evaluate condition
            if _evaluate_condition(condition):
                # Execute action
                _execute_automation_action(rule)

                # Update rule statistics
                rule['last_triggered'] = datetime.now()
                rule['trigger_count'] = rule.get('trigger_count', 0) + 1

                logger.info(f"Automation rule '{rule['trigger_name']}' triggered")

    except Exception as e:
        logger.error(f"Error evaluating automation rules: {str(e)}")


def _evaluate_condition(condition: str) -> bool:
    """
    Evaluate a condition string

    Args:
        condition: Condition string (e.g., "test_overdue > 2 days")

    Returns:
        True if condition is met
    """
    try:
        # Parse condition
        if "test_overdue >" in condition:
            days = int(condition.split('>')[1].strip().split()[0])
            # Check for overdue tests
            test_results = st.session_state.get('test_results', [])
            for test in test_results:
                if test.get('status') == 'In Progress':
                    start_date = test.get('start_date', datetime.now())
                    if isinstance(start_date, str):
                        start_date = datetime.fromisoformat(start_date)
                    days_elapsed = (datetime.now() - start_date).days
                    if days_elapsed > days:
                        return True

        elif "approval_pending >" in condition:
            days = int(condition.split('>')[1].strip().split()[0])
            # Check for pending approvals
            for workflow in st.session_state.approval_workflows:
                if workflow['status'] == 'pending':
                    created_date = workflow.get('created_date', datetime.now())
                    days_pending = (datetime.now() - created_date).days
                    if days_pending > days:
                        return True

        elif "test_result = Failed" in condition:
            # Check for failed tests
            test_results = st.session_state.get('test_results', [])
            for test in test_results:
                if test.get('result') == 'Failed':
                    if "priority = Critical" in condition:
                        if test.get('priority') == 'Critical':
                            return True
                    else:
                        return True

        elif "schedule = weekly" in condition:
            # Check if it's time for weekly report
            # Simple check: trigger on Mondays
            if datetime.now().weekday() == 0:
                return True

        return False

    except Exception as e:
        logger.error(f"Error evaluating condition '{condition}': {str(e)}")
        return False


def _execute_automation_action(rule: Dict[str, Any]):
    """
    Execute an automation action

    Args:
        rule: Automation rule containing action to execute
    """
    try:
        action = rule['action']

        if action == 'alert_manager':
            _create_notification(
                notification_type='Alert',
                title='Automated Alert: Test Overdue',
                message=f"Rule '{rule['trigger_name']}' triggered - tests are overdue",
                priority='High',
                related_id=rule['id'],
                action_required=True
            )

        elif action == 'escalate_to_next_level':
            # Escalate pending approvals
            for workflow in st.session_state.approval_workflows:
                if workflow['status'] == 'pending':
                    created_date = workflow.get('created_date', datetime.now())
                    days_pending = (datetime.now() - created_date).days
                    if days_pending > 3:
                        _escalate_approval(workflow['approval_id'])

        elif action == 'immediate_notification':
            _create_notification(
                notification_type='Critical Alert',
                title='Critical Test Failure Detected',
                message=f"Rule '{rule['trigger_name']}' triggered - immediate attention required",
                priority='Critical',
                related_id=rule['id'],
                action_required=True
            )

            # Send email notification if configured
            if st.session_state.notification_preferences.get('email', False):
                _send_email_notification(
                    subject='Critical Test Failure',
                    body=f"Critical test failure detected. Rule: {rule['trigger_name']}",
                    recipients=st.session_state.notification_preferences.get('email_list', [])
                )

        elif action == 'send_summary_report':
            _generate_summary_report()

        logger.info(f"Automation action '{action}' executed for rule '{rule['trigger_name']}'")

    except Exception as e:
        logger.error(f"Error executing automation action: {str(e)}")


def _escalate_approval(approval_id: str):
    """
    Escalate an approval to the next level or notify management

    Args:
        approval_id: ID of approval to escalate
    """
    try:
        workflow = None
        for wf in st.session_state.approval_workflows:
            if wf['approval_id'] == approval_id:
                workflow = wf
                break

        if not workflow:
            return

        # Notify current approver and manager
        current_level = workflow.get('current_level', 1)
        if current_level <= len(APPROVAL_LEVELS):
            approver = APPROVAL_LEVELS[current_level - 1]

            _create_notification(
                notification_type='Escalation',
                title=f'Approval Escalated: {workflow["test_type"]}',
                message=f'Approval pending for {(datetime.now() - workflow["created_date"]).days} days - requires immediate attention',
                priority='High',
                related_id=approval_id,
                action_required=True
            )

            _log_audit_event(
                approval_id=approval_id,
                action='ESCALATED',
                user='System',
                details=f"Auto-escalated due to pending time exceeding threshold"
            )

    except Exception as e:
        logger.error(f"Error escalating approval: {str(e)}")


# ============================================================================
# NOTIFICATION SYSTEM
# ============================================================================

def _create_notification(notification_type: str, title: str, message: str,
                        priority: str = 'Medium', related_id: str = None,
                        action_required: bool = False):
    """
    Create a new notification

    Args:
        notification_type: Type of notification
        title: Notification title
        message: Notification message
        priority: Priority level (Low/Medium/High/Critical)
        related_id: ID of related entity
        action_required: Whether action is required
    """
    try:
        notification = {
            'id': str(uuid.uuid4()),
            'type': notification_type,
            'title': title,
            'message': message,
            'priority': priority,
            'timestamp': datetime.now(),
            'read': False,
            'action_required': action_required,
            'related_id': related_id
        }

        # Add to session state
        st.session_state.notifications.append(notification)

        # Send email if configured
        if st.session_state.notification_preferences.get('email', False):
            if priority in ['High', 'Critical']:
                _send_email_notification(
                    subject=f"{priority} Priority: {title}",
                    body=message,
                    recipients=st.session_state.notification_preferences.get('email_list', [])
                )

        logger.info(f"Notification created: {title}")

    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}")


def _send_email_notification(subject: str, body: str, recipients: List[str]):
    """
    Send email notification (simulated)

    Args:
        subject: Email subject
        body: Email body
        recipients: List of recipient email addresses
    """
    try:
        # In production, integrate with actual email service (SMTP, SendGrid, etc.)
        logger.info(f"Email notification sent to {', '.join(recipients)}: {subject}")

        # Log to audit trail
        _log_audit_event(
            approval_id=None,
            action='EMAIL_SENT',
            user='System',
            details=f"Email sent to {len(recipients)} recipients: {subject}"
        )

    except Exception as e:
        logger.error(f"Error sending email notification: {str(e)}")


def mark_notification_read(notification_id: str) -> bool:
    """
    Mark a notification as read

    Args:
        notification_id: ID of notification to mark as read

    Returns:
        True if successful
    """
    try:
        for notification in st.session_state.notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                logger.info(f"Notification {notification_id} marked as read")
                return True
        return False

    except Exception as e:
        logger.error(f"Error marking notification as read: {str(e)}")
        return False


def get_unread_notification_count() -> int:
    """
    Get count of unread notifications

    Returns:
        Count of unread notifications
    """
    return len([n for n in st.session_state.notifications if not n.get('read', False)])


# ============================================================================
# AUDIT TRAIL & LOGGING
# ============================================================================

def _log_audit_event(approval_id: Optional[str], action: str, user: str, details: str):
    """
    Log an audit event

    Args:
        approval_id: Related approval ID (optional)
        action: Action performed
        user: User who performed action
        details: Event details
    """
    try:
        audit_event = {
            'id': str(uuid.uuid4()),
            'approval_id': approval_id,
            'action': action,
            'user': user,
            'timestamp': datetime.now(),
            'details': details,
            'module_id': MODULE_ID
        }

        st.session_state.approval_audit_trail.append(audit_event)
        logger.info(f"Audit event logged: {action} by {user}")

    except Exception as e:
        logger.error(f"Error logging audit event: {str(e)}")


def get_audit_trail(approval_id: Optional[str] = None,
                   start_date: Optional[datetime] = None,
                   end_date: Optional[datetime] = None) -> List[Dict[str, Any]]:
    """
    Retrieve audit trail with optional filtering

    Args:
        approval_id: Filter by approval ID
        start_date: Filter by start date
        end_date: Filter by end date

    Returns:
        List of audit events
    """
    try:
        events = st.session_state.approval_audit_trail.copy()

        if approval_id:
            events = [e for e in events if e.get('approval_id') == approval_id]

        if start_date:
            events = [e for e in events if e['timestamp'] >= start_date]

        if end_date:
            events = [e for e in events if e['timestamp'] <= end_date]

        # Sort by timestamp descending
        events.sort(key=lambda x: x['timestamp'], reverse=True)

        return events

    except Exception as e:
        logger.error(f"Error retrieving audit trail: {str(e)}")
        return []


# ============================================================================
# SUMMARY REPORTS
# ============================================================================

def _generate_summary_report():
    """Generate and send summary report"""
    try:
        # Collect statistics
        total_workflows = len(st.session_state.approval_workflows)
        pending = len([w for w in st.session_state.approval_workflows if w['status'] == 'pending'])
        approved = len([w for w in st.session_state.approval_workflows if w['status'] == 'approved'])
        rejected = len([w for w in st.session_state.approval_workflows if w['status'] == 'rejected'])

        total_notifications = len(st.session_state.notifications)
        unread = get_unread_notification_count()

        # Create report
        report = f"""
        SOLAR PV PROJECT MANAGEMENT - WEEKLY SUMMARY REPORT
        Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

        APPROVAL WORKFLOWS:
        - Total Workflows: {total_workflows}
        - Pending: {pending}
        - Approved: {approved}
        - Rejected: {rejected}

        NOTIFICATIONS:
        - Total Notifications: {total_notifications}
        - Unread: {unread}

        AUTOMATION RULES:
        - Active Rules: {len([r for r in st.session_state.automation_rules if r['status'] == 'Active'])}
        - Total Triggers (7 days): {sum([r.get('trigger_count', 0) for r in st.session_state.automation_rules])}
        """

        # Create notification for report
        _create_notification(
            notification_type='Report',
            title='Weekly Summary Report Available',
            message='Weekly project summary report has been generated',
            priority='Low',
            related_id=None,
            action_required=False
        )

        # Send email if configured
        if st.session_state.notification_preferences.get('email', False):
            _send_email_notification(
                subject='Weekly Summary Report - Solar PV Project Management',
                body=report,
                recipients=st.session_state.notification_preferences.get('email_list', [])
            )

        logger.info("Summary report generated and sent")

    except Exception as e:
        logger.error(f"Error generating summary report: {str(e)}")


# ============================================================================
# UI RENDERING FUNCTIONS
# ============================================================================

def render_approval_dashboard():
    """Render the approval dashboard showing pending approvals and history"""
    try:
        st.subheader("📋 Approval Dashboard")

        # Initialize state if needed
        initialize_approval_automation_state()

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        total_workflows = len(st.session_state.approval_workflows)
        pending = len([w for w in st.session_state.approval_workflows if w['status'] == 'pending'])
        approved = len([w for w in st.session_state.approval_workflows if w['status'] == 'approved'])
        rejected = len([w for w in st.session_state.approval_workflows if w['status'] == 'rejected'])

        col1.metric("Total Workflows", total_workflows)
        col2.metric("Pending", pending, delta=None if pending == 0 else f"{pending} waiting")
        col3.metric("Approved", approved)
        col4.metric("Rejected", rejected)

        st.markdown("---")

        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["Pending Approvals", "Approval History", "My Actions"])

        with tab1:
            _render_pending_approvals()

        with tab2:
            _render_approval_history()

        with tab3:
            _render_my_actions()

    except Exception as e:
        logger.error(f"Error rendering approval dashboard: {str(e)}")
        st.error(f"Error loading approval dashboard: {str(e)}")


def _render_pending_approvals():
    """Render pending approvals section"""
    try:
        pending_workflows = [w for w in st.session_state.approval_workflows if w['status'] == 'pending']

        if not pending_workflows:
            st.info("No pending approvals at this time.")
            return

        st.markdown("### ⏳ Pending Approvals")

        for workflow in pending_workflows:
            current_level = workflow.get('current_level', 1)
            if current_level <= len(APPROVAL_LEVELS):
                approver_info = APPROVAL_LEVELS[current_level - 1]
            else:
                approver_info = {'role': 'Unknown', 'name': 'Unknown'}

            # Calculate days pending
            created_date = workflow.get('created_date', datetime.now())
            days_pending = (datetime.now() - created_date).days

            # Status color
            status_color = "🟡" if days_pending < 2 else "🟠" if days_pending < 3 else "🔴"

            with st.expander(f"{status_color} {workflow['approval_id']} - {workflow.get('test_type', 'Test')} (Level {current_level}/{workflow['total_levels']})"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**Test ID:** {workflow['test_result_id']}")
                    st.write(f"**Test Type:** {workflow.get('test_type', 'N/A')}")
                    st.write(f"**Current Approver:** {approver_info['role']}")
                    st.write(f"**Created:** {created_date.strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Days Pending:** {days_pending}")

                    # Show test data
                    if workflow.get('test_data'):
                        st.write("**Test Data:**")
                        test_data = workflow['test_data']
                        st.json({k: str(v) if isinstance(v, datetime) else v for k, v in test_data.items()})

                with col2:
                    # Approval chain progress
                    st.write("**Approval Progress:**")
                    for i, level in enumerate(APPROVAL_LEVELS, 1):
                        if i < current_level:
                            st.write(f"✅ {level['role']}")
                        elif i == current_level:
                            st.write(f"⏳ {level['role']} (Current)")
                        else:
                            st.write(f"⬜ {level['role']}")

                # Show previous approvals
                if workflow.get('approval_chain'):
                    st.write("**Previous Approvals:**")
                    for approval in workflow['approval_chain']:
                        st.write(f"- {approval['role']}: {approval['status']} by {approval['reviewer_name']} ({approval['timestamp'].strftime('%Y-%m-%d %H:%M')})")
                        if approval.get('comments'):
                            st.write(f"  Comments: {approval['comments']}")

    except Exception as e:
        logger.error(f"Error rendering pending approvals: {str(e)}")
        st.error(f"Error: {str(e)}")


def _render_approval_history():
    """Render approval history section"""
    try:
        st.markdown("### 📜 Approval History")

        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox("Filter by Status", ["All", "Approved", "Rejected", "Pending"])
        with col2:
            days_filter = st.selectbox("Time Period", ["Last 7 Days", "Last 30 Days", "All Time"])
        with col3:
            sort_by = st.selectbox("Sort By", ["Newest First", "Oldest First"])

        # Apply filters
        workflows = st.session_state.approval_workflows.copy()

        if status_filter != "All":
            workflows = [w for w in workflows if w['status'] == status_filter.lower()]

        if days_filter == "Last 7 Days":
            cutoff = datetime.now() - timedelta(days=7)
            workflows = [w for w in workflows if w.get('created_date', datetime.now()) >= cutoff]
        elif days_filter == "Last 30 Days":
            cutoff = datetime.now() - timedelta(days=30)
            workflows = [w for w in workflows if w.get('created_date', datetime.now()) >= cutoff]

        # Sort
        workflows.sort(key=lambda x: x.get('created_date', datetime.now()),
                      reverse=(sort_by == "Newest First"))

        if not workflows:
            st.info("No approval workflows found matching the filters.")
            return

        # Create DataFrame for display
        df_data = []
        for wf in workflows:
            df_data.append({
                'Approval ID': wf['approval_id'],
                'Test ID': wf['test_result_id'],
                'Test Type': wf.get('test_type', 'N/A'),
                'Status': wf['status'].title(),
                'Current Level': f"{wf.get('current_level', 1)}/{wf['total_levels']}",
                'Created Date': wf.get('created_date', datetime.now()).strftime('%Y-%m-%d %H:%M'),
                'Created By': wf.get('created_by', 'N/A')
            })

        df = pd.DataFrame(df_data)

        # Display table
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Approval timeline chart
        if len(workflows) > 0:
            st.markdown("### Approval Timeline")

            fig = go.Figure()

            status_colors = {
                'pending': '#FFA500',
                'approved': '#28a745',
                'rejected': '#dc3545',
                'info_requested': '#17a2b8'
            }

            for wf in workflows:
                color = status_colors.get(wf['status'], '#6c757d')
                fig.add_trace(go.Scatter(
                    x=[wf.get('created_date', datetime.now())],
                    y=[wf['approval_id']],
                    mode='markers',
                    marker=dict(size=12, color=color),
                    name=wf['status'].title(),
                    text=[f"{wf['test_type']}<br>Level: {wf.get('current_level', 1)}/{wf['total_levels']}"],
                    hovertemplate='<b>%{text}</b><br>%{y}<br>%{x}<extra></extra>'
                ))

            fig.update_layout(
                title="Approval Workflow Timeline",
                xaxis_title="Date",
                yaxis_title="Approval ID",
                showlegend=True,
                height=400
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        logger.error(f"Error rendering approval history: {str(e)}")
        st.error(f"Error: {str(e)}")


def _render_my_actions():
    """Render user's action items"""
    try:
        st.markdown("### 👤 My Action Items")

        current_user = st.session_state.get('current_user', 'Admin User')

        # Find workflows requiring action from current user
        action_items = []
        for workflow in st.session_state.approval_workflows:
            if workflow['status'] == 'pending':
                current_level = workflow.get('current_level', 1)
                if current_level <= len(APPROVAL_LEVELS):
                    # In a real system, match user to role
                    # For demo, show all pending items
                    action_items.append(workflow)

        if not action_items:
            st.success("You have no pending action items!")
            return

        st.info(f"You have {len(action_items)} approval(s) requiring your attention.")

        for workflow in action_items:
            st.markdown(f"**{workflow['approval_id']} - {workflow.get('test_type', 'Test')}**")
            st.write(f"Test ID: {workflow['test_result_id']}")
            st.write(f"Created: {workflow.get('created_date', datetime.now()).strftime('%Y-%m-%d %H:%M')}")

            # Quick action button
            if st.button(f"Review {workflow['approval_id']}", key=f"review_{workflow['approval_id']}"):
                st.session_state.selected_approval_for_review = workflow['approval_id']
                st.info(f"Please use the Approval Form below to review {workflow['approval_id']}")

            st.markdown("---")

    except Exception as e:
        logger.error(f"Error rendering my actions: {str(e)}")
        st.error(f"Error: {str(e)}")


def render_approval_form():
    """Render approval form for reviewers to approve/reject with comments"""
    try:
        st.subheader("✍️ Approval Form")

        # Initialize state if needed
        initialize_approval_automation_state()

        # Get pending approvals
        pending_workflows = [w for w in st.session_state.approval_workflows
                           if w['status'] == 'pending']

        if not pending_workflows:
            st.info("No pending approvals available for review.")
            return

        # Select approval to review
        approval_options = {f"{w['approval_id']} - {w.get('test_type', 'Test')} (Level {w.get('current_level', 1)})": w['approval_id']
                          for w in pending_workflows}

        selected_option = st.selectbox("Select Approval to Review", list(approval_options.keys()))
        selected_approval_id = approval_options[selected_option]

        # Find workflow
        workflow = None
        for w in st.session_state.approval_workflows:
            if w['approval_id'] == selected_approval_id:
                workflow = w
                break

        if not workflow:
            st.error("Workflow not found")
            return

        # Display workflow details
        st.markdown("---")
        st.markdown("### Approval Details")

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Approval ID:** {workflow['approval_id']}")
            st.write(f"**Test ID:** {workflow['test_result_id']}")
            st.write(f"**Test Type:** {workflow.get('test_type', 'N/A')}")
            st.write(f"**Created By:** {workflow.get('created_by', 'N/A')}")
            st.write(f"**Created Date:** {workflow.get('created_date', datetime.now()).strftime('%Y-%m-%d %H:%M')}")

        with col2:
            current_level = workflow.get('current_level', 1)
            if current_level <= len(APPROVAL_LEVELS):
                approver_info = APPROVAL_LEVELS[current_level - 1]
                st.write(f"**Current Level:** {current_level} of {workflow['total_levels']}")
                st.write(f"**Current Approver Role:** {approver_info['role']}")
                st.write(f"**Approver Name:** {approver_info['name']}")

            days_pending = (datetime.now() - workflow.get('created_date', datetime.now())).days
            st.write(f"**Days Pending:** {days_pending}")

        # Test data
        if workflow.get('test_data'):
            with st.expander("View Test Data"):
                test_data = workflow['test_data']
                st.json({k: str(v) if isinstance(v, datetime) else v for k, v in test_data.items()})

        # Previous approvals
        if workflow.get('approval_chain'):
            with st.expander("View Previous Approvals"):
                for approval in workflow['approval_chain']:
                    st.write(f"**Level {approval['level']} - {approval['role']}:**")
                    st.write(f"Reviewer: {approval['reviewer_name']}")
                    st.write(f"Status: {approval['status'].title()}")
                    st.write(f"Timestamp: {approval['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                    if approval.get('comments'):
                        st.write(f"Comments: {approval['comments']}")
                    if approval.get('signature_hash'):
                        st.write(f"Signature: {approval['signature_hash'][:16]}...")
                    st.markdown("---")

        # Approval form
        st.markdown("---")
        st.markdown("### Review Action")

        with st.form("approval_form"):
            reviewer_name = st.text_input("Your Name", value=st.session_state.get('current_user', 'Reviewer'))
            comments = st.text_area("Comments", placeholder="Enter your review comments here...")

            col1, col2, col3 = st.columns(3)

            approve_btn = col1.form_submit_button("✅ Approve", use_container_width=True)
            reject_btn = col2.form_submit_button("❌ Reject", use_container_width=True)
            info_btn = col3.form_submit_button("ℹ️ Request Info", use_container_width=True)

            if approve_btn:
                if process_approval_action(
                    approval_id=selected_approval_id,
                    action='approved',
                    reviewer_name=reviewer_name,
                    comments=comments,
                    level=current_level
                ):
                    st.success(f"✅ Approval {selected_approval_id} has been approved!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("Failed to process approval")

            elif reject_btn:
                if not comments:
                    st.error("Please provide comments for rejection")
                else:
                    if process_approval_action(
                        approval_id=selected_approval_id,
                        action='rejected',
                        reviewer_name=reviewer_name,
                        comments=comments,
                        level=current_level
                    ):
                        st.error(f"❌ Approval {selected_approval_id} has been rejected")
                        st.rerun()
                    else:
                        st.error("Failed to process rejection")

            elif info_btn:
                if not comments:
                    st.error("Please specify what information is needed")
                else:
                    if process_approval_action(
                        approval_id=selected_approval_id,
                        action='request_info',
                        reviewer_name=reviewer_name,
                        comments=comments,
                        level=current_level
                    ):
                        st.info(f"ℹ️ Information requested for {selected_approval_id}")
                        st.rerun()
                    else:
                        st.error("Failed to request information")

    except Exception as e:
        logger.error(f"Error rendering approval form: {str(e)}")
        st.error(f"Error: {str(e)}")


def render_automation_rules_panel():
    """Render automation rules management panel"""
    try:
        st.subheader("⚙️ Automation Rules")

        # Initialize state if needed
        initialize_approval_automation_state()

        # Summary metrics
        col1, col2, col3 = st.columns(3)

        total_rules = len(st.session_state.automation_rules)
        active_rules = len([r for r in st.session_state.automation_rules if r['status'] == 'Active'])
        total_triggers = sum([r.get('trigger_count', 0) for r in st.session_state.automation_rules])

        col1.metric("Total Rules", total_rules)
        col2.metric("Active Rules", active_rules)
        col3.metric("Total Triggers", total_triggers)

        st.markdown("---")

        # Tabs
        tab1, tab2 = st.tabs(["Manage Rules", "Create New Rule"])

        with tab1:
            _render_existing_rules()

        with tab2:
            _render_create_rule_form()

        # Run automation check
        st.markdown("---")
        if st.button("🔄 Run Automation Check Now"):
            with st.spinner("Evaluating automation rules..."):
                evaluate_automation_rules()
                st.success("Automation rules evaluated successfully!")
                st.rerun()

    except Exception as e:
        logger.error(f"Error rendering automation rules panel: {str(e)}")
        st.error(f"Error: {str(e)}")


def _render_existing_rules():
    """Render existing automation rules"""
    try:
        st.markdown("### 📋 Existing Rules")

        if not st.session_state.automation_rules:
            st.info("No automation rules configured.")
            return

        for rule in st.session_state.automation_rules:
            status_icon = "✅" if rule['status'] == 'Active' else "⏸️"

            with st.expander(f"{status_icon} {rule['trigger_name']}"):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**Condition:** {rule['condition']}")
                    st.write(f"**Action:** {rule['action']}")
                    st.write(f"**Status:** {rule['status']}")
                    st.write(f"**Created:** {rule['created_date'].strftime('%Y-%m-%d')}")

                    if rule.get('last_triggered'):
                        st.write(f"**Last Triggered:** {rule['last_triggered'].strftime('%Y-%m-%d %H:%M')}")
                    st.write(f"**Trigger Count:** {rule.get('trigger_count', 0)}")

                with col2:
                    # Toggle status
                    new_status = "Inactive" if rule['status'] == 'Active' else "Active"
                    if st.button(f"Set {new_status}", key=f"toggle_{rule['id']}"):
                        rule['status'] = new_status
                        st.success(f"Rule status changed to {new_status}")
                        st.rerun()

                    # Delete rule
                    if st.button("🗑️ Delete", key=f"delete_{rule['id']}"):
                        st.session_state.automation_rules.remove(rule)
                        st.success("Rule deleted")
                        st.rerun()

    except Exception as e:
        logger.error(f"Error rendering existing rules: {str(e)}")
        st.error(f"Error: {str(e)}")


def _render_create_rule_form():
    """Render form to create new automation rule"""
    try:
        st.markdown("### ➕ Create New Automation Rule")

        with st.form("new_automation_rule"):
            trigger_name = st.text_input("Rule Name", placeholder="e.g., Test Overdue Alert")

            condition_type = st.selectbox("Condition Type", [
                "Test Overdue",
                "Approval Pending",
                "Test Failed",
                "Scheduled Report"
            ])

            # Dynamic condition builder
            if condition_type == "Test Overdue":
                days = st.number_input("Days Overdue", min_value=1, max_value=30, value=2)
                condition = f"test_overdue > {days} days"
            elif condition_type == "Approval Pending":
                days = st.number_input("Days Pending", min_value=1, max_value=30, value=3)
                condition = f"approval_pending > {days} days"
            elif condition_type == "Test Failed":
                priority = st.selectbox("Priority", ["Any", "Critical", "High"])
                if priority == "Any":
                    condition = "test_result = Failed"
                else:
                    condition = f"test_result = Failed AND priority = {priority}"
            else:  # Scheduled Report
                frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
                condition = f"schedule = {frequency.lower()}"

            action_type = st.selectbox("Action", [
                "alert_manager",
                "escalate_to_next_level",
                "immediate_notification",
                "send_summary_report"
            ])

            submit = st.form_submit_button("Create Rule")

            if submit:
                if not trigger_name:
                    st.error("Please provide a rule name")
                else:
                    new_rule = {
                        'id': str(uuid.uuid4()),
                        'trigger_name': trigger_name,
                        'condition': condition,
                        'action': action_type,
                        'status': 'Active',
                        'created_date': datetime.now(),
                        'last_triggered': None,
                        'trigger_count': 0
                    }

                    st.session_state.automation_rules.append(new_rule)
                    st.success(f"Automation rule '{trigger_name}' created successfully!")
                    logger.info(f"New automation rule created: {trigger_name}")
                    st.rerun()

    except Exception as e:
        logger.error(f"Error rendering create rule form: {str(e)}")
        st.error(f"Error: {str(e)}")


def render_notifications_panel():
    """Render notifications panel with read/unread tracking"""
    try:
        st.subheader("🔔 Notifications")

        # Initialize state if needed
        initialize_approval_automation_state()

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)

        total_notifications = len(st.session_state.notifications)
        unread = get_unread_notification_count()
        high_priority = len([n for n in st.session_state.notifications
                           if n.get('priority') in ['High', 'Critical'] and not n.get('read', False)])
        action_required = len([n for n in st.session_state.notifications
                             if n.get('action_required', False) and not n.get('read', False)])

        col1.metric("Total", total_notifications)
        col2.metric("Unread", unread, delta=f"{unread} new" if unread > 0 else None)
        col3.metric("High Priority", high_priority)
        col4.metric("Action Required", action_required)

        st.markdown("---")

        # Filter and sort options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_read = st.selectbox("Filter", ["All", "Unread Only", "Read Only"])
        with col2:
            filter_priority = st.selectbox("Priority", ["All", "Critical", "High", "Medium", "Low"])
        with col3:
            sort_order = st.selectbox("Sort", ["Newest First", "Oldest First"])

        # Mark all as read button
        if st.button("✅ Mark All as Read"):
            for notification in st.session_state.notifications:
                notification['read'] = True
            st.success("All notifications marked as read")
            st.rerun()

        st.markdown("---")

        # Apply filters
        notifications = st.session_state.notifications.copy()

        if filter_read == "Unread Only":
            notifications = [n for n in notifications if not n.get('read', False)]
        elif filter_read == "Read Only":
            notifications = [n for n in notifications if n.get('read', False)]

        if filter_priority != "All":
            notifications = [n for n in notifications if n.get('priority') == filter_priority]

        # Sort
        notifications.sort(key=lambda x: x.get('timestamp', datetime.now()),
                          reverse=(sort_order == "Newest First"))

        if not notifications:
            st.info("No notifications found matching the filters.")
            return

        # Display notifications
        for notification in notifications:
            _render_notification_card(notification)

    except Exception as e:
        logger.error(f"Error rendering notifications panel: {str(e)}")
        st.error(f"Error: {str(e)}")


def _render_notification_card(notification: Dict[str, Any]):
    """Render a single notification card"""
    try:
        # Priority colors
        priority_colors = {
            'Critical': '🔴',
            'High': '🟠',
            'Medium': '🟡',
            'Low': '🟢'
        }

        priority_icon = priority_colors.get(notification.get('priority', 'Medium'), '🔵')
        read_icon = "📭" if notification.get('read', False) else "📬"
        action_icon = "⚡" if notification.get('action_required', False) else ""

        # Card container
        card_class = "" if notification.get('read', False) else "background-color: #f0f8ff;"

        with st.container():
            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {priority_icon} {read_icon} {action_icon} {notification['title']}")
                st.write(f"**Type:** {notification['type']}")
                st.write(f"**Message:** {notification['message']}")
                st.write(f"**Time:** {notification.get('timestamp', datetime.now()).strftime('%Y-%m-%d %H:%M')}")

                if notification.get('related_id'):
                    st.write(f"**Related ID:** {notification['related_id']}")

            with col2:
                if not notification.get('read', False):
                    if st.button("Mark Read", key=f"read_{notification['id']}"):
                        mark_notification_read(notification['id'])
                        st.rerun()

                if notification.get('action_required', False):
                    st.warning("Action Required")

            st.markdown("---")

    except Exception as e:
        logger.error(f"Error rendering notification card: {str(e)}")


# ============================================================================
# UTILITY FUNCTIONS FOR TESTING
# ============================================================================

def create_test_approval_workflow(test_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Utility function to create a test approval workflow

    Args:
        test_result: Optional test result data

    Returns:
        Created approval workflow
    """
    if test_result is None:
        test_result = {
            'id': f'TEST-{len(st.session_state.get("test_results", [])) + 1:03d}',
            'test_type': 'Solar Panel Efficiency Test',
            'test_date': datetime.now(),
            'result': 'Pass',
            'technician': 'John Doe',
            'status': 'Completed'
        }

    return route_for_approval(test_result)


# ============================================================================
# MAIN INTERFACE (for standalone testing)
# ============================================================================

def main():
    """Main function for standalone testing of the module"""
    st.title("☀️ Solar PV Approval Automation System")
    st.markdown(f"**Module ID:** {MODULE_ID}")

    # Initialize
    initialize_approval_automation_state()

    # Sidebar
    with st.sidebar:
        st.header("Module Navigation")
        page = st.radio("Select View", [
            "Approval Dashboard",
            "Approval Form",
            "Automation Rules",
            "Notifications",
            "Test Functions"
        ])

    # Main content
    if page == "Approval Dashboard":
        render_approval_dashboard()
    elif page == "Approval Form":
        render_approval_form()
    elif page == "Automation Rules":
        render_automation_rules_panel()
    elif page == "Notifications":
        render_notifications_panel()
    elif page == "Test Functions":
        st.header("Test Functions")

        if st.button("Create Test Approval Workflow"):
            workflow = create_test_approval_workflow()
            st.success(f"Created test workflow: {workflow['approval_id']}")
            st.json({k: str(v) if isinstance(v, datetime) else v for k, v in workflow.items()})

        if st.button("Trigger Automation Rules"):
            evaluate_automation_rules()
            st.success("Automation rules evaluated")

        if st.button("Create Test Notification"):
            _create_notification(
                notification_type='Test',
                title='Test Notification',
                message='This is a test notification',
                priority='Medium',
                action_required=False
            )
            st.success("Test notification created")


if __name__ == "__main__":
    main()
