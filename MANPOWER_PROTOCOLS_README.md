# Manpower & Test Protocols Module

**MODULE_ID:** `MANPOWER_PROTOCOLS_SESSION3`
**Version:** 1.0.0
**Status:** Production Ready

## Overview

This module provides comprehensive manpower management and test methods/protocol system functionality for solar PV project management. It includes advanced features for staff tracking, workload analysis, test protocol management, and automated compliance checking.

## Features

### 👥 Manpower Management

1. **Staff Registry**
   - Comprehensive staff profiles with ID, name, role, and contact info
   - Expertise areas and skill tracking
   - Certification management with expiration alerts
   - Availability status tracking

2. **Performance Metrics**
   - Tasks completed counter
   - Quality score (0-100)
   - Speed score (0-100)
   - Reliability percentage

3. **Workload Analysis**
   - Current load vs. capacity tracking
   - Utilization percentage calculation
   - Real-time capacity monitoring
   - Visual workload distribution charts

4. **Availability Calendar**
   - Timeline view of all staff activities
   - Monthly grid calendar
   - Individual staff schedules
   - Holiday, assignment, and training tracking

5. **Skill-Based Task Assignment**
   - Automated staff matching based on expertise
   - Availability and capacity checking
   - Performance-weighted assignment scoring
   - Manual override options

6. **Certification Tracking**
   - Expiration date monitoring
   - Automatic alerts (60-day, 30-day, critical)
   - Compliance status reporting

### 🔬 Test Methods & Protocols

1. **Test Standards Database**
   - IEC 61215 (Thermal Cycling, Humidity Freeze, etc.)
   - IEC 61730 (Safety Testing)
   - ISO standards support
   - Detailed test specifications

2. **Protocol Templates**
   - Step-by-step test procedures
   - Expected results and pass criteria
   - Operator instructions and safety notes
   - Equipment requirements

3. **Test Selection Interface**
   - Search and filter capabilities
   - Category-based browsing
   - Protocol association tracking

4. **Protocol Entry Sheet**
   - Guided data entry forms
   - Step completion tracking
   - Real-time validation
   - File attachment support

5. **Auto-Validation**
   - Automatic compliance checking
   - Pass/fail determination
   - Detailed criterion evaluation
   - Multi-parameter validation

6. **Result Tracking**
   - Version control
   - Audit trail with timestamps
   - Operator attribution
   - Environmental condition logging

7. **Compliance Reporting**
   - Comprehensive results table
   - Status filtering and searching
   - Export to CSV/JSON
   - Detailed result inspection

## Installation & Integration

### Quick Start

1. **Ensure the module file is in your project directory:**
   ```
   manpower_protocols_session3.py
   ```

2. **Import in your app.py:**
   ```python
   from manpower_protocols_session3 import (
       initialize_manpower_protocols_data,
       render_manpower_dashboard,
       render_availability_calendar,
       render_test_selection,
       render_protocol_entry_sheet,
       render_test_results_table,
       assign_task_to_staff
   )
   ```

3. **Initialize data (call once at startup):**
   ```python
   initialize_manpower_protocols_data()
   ```

4. **Use the rendering functions in your UI:**
   ```python
   # In your Streamlit app
   tab1, tab2, tab3 = st.tabs(["Manpower", "Protocols", "Results"])

   with tab1:
       render_manpower_dashboard()
       render_availability_calendar()

   with tab2:
       render_test_selection()
       render_protocol_entry_sheet()

   with tab3:
       render_test_results_table()
   ```

### Run Demo Application

Test the module independently:

```bash
streamlit run demo_manpower_protocols.py
```

## Sample Data

The module includes sample data for immediate testing:

### Staff Members (5)

| ID | Name | Role | Expertise |
|---|---|---|---|
| STF-001 | Dr. Sarah Chen | Senior Test Engineer | IEC 61215, Thermal Cycling, Mechanical Load |
| STF-002 | James Rodriguez | Test Technician | UV Testing, Humidity Freeze, Visual Inspection |
| STF-003 | Maria Santos | Laboratory Manager | Quality Control, All IEC Standards, ISO Compliance |
| STF-004 | Michael Zhang | Junior Test Engineer | Data Analysis, Report Generation, Sample Preparation |
| STF-005 | Emily Johnson | QA Specialist | Data Validation, Protocol Compliance, Audit Support |

### Test Standards (3)

1. **IEC 61215-001**: Thermal Cycling Test
2. **IEC 61215-002**: Humidity Freeze Test
3. **IEC 61730-001**: Module Safety Test - Electrical

### Protocol Templates (2)

1. **PROT-TC-001**: Thermal Cycling Protocol - Standard Modules
2. **PROT-HF-001**: Humidity Freeze Protocol - Standard Modules

## API Reference

### Initialization

```python
initialize_manpower_protocols_data()
```
Initializes all session state variables and loads sample data if not already present.

### Rendering Functions

#### Manpower Dashboard
```python
render_manpower_dashboard()
```
Displays comprehensive manpower overview with metrics, workload analysis, performance charts, and certification alerts.

#### Availability Calendar
```python
render_availability_calendar()
```
Shows staff availability with multiple view modes (Timeline, Monthly Grid, Staff Schedule) and event management.

#### Test Selection
```python
render_test_selection()
```
Provides searchable interface for browsing and selecting test methods from the standards database.

#### Protocol Entry Sheet
```python
render_protocol_entry_sheet(protocol_id=None)
```
Renders comprehensive data entry form for recording test results with validation and compliance checking.

**Parameters:**
- `protocol_id` (optional): Specific protocol to display. If None, shows protocol selection.

#### Test Results Table
```python
render_test_results_table()
```
Displays all test results with filtering, compliance status, and export options.

### Utility Functions

#### Task Assignment
```python
assign_task_to_staff(task_name, required_skills=None, preferred_staff_id=None)
```
Automatically assigns tasks to staff based on skills, availability, and performance.

**Parameters:**
- `task_name` (str): Name/description of the task
- `required_skills` (list, optional): Required expertise areas
- `preferred_staff_id` (str, optional): Specific staff member to assign to

**Returns:**
- `dict`: Assignment result with success status, staff_id, and message

#### Get Staff by ID
```python
get_staff_by_id(staff_id)
```
Retrieves staff member details by ID.

#### Get Protocol by ID
```python
get_protocol_by_id(protocol_id)
```
Retrieves protocol details by ID.

#### Get Test Standard by ID
```python
get_test_standard_by_id(test_id)
```
Retrieves test standard details by ID.

#### Check Certification Expiry
```python
check_certification_expiry(staff_id, days_ahead=60)
```
Checks for expiring certifications for a staff member.

**Parameters:**
- `staff_id` (str): Staff member ID
- `days_ahead` (int): Number of days to look ahead (default: 60)

**Returns:**
- `list`: List of expiring certifications with details

### Validation Function

```python
validate_test_results(results, pass_criteria)
```
Validates test results against pass criteria and returns compliance status.

**Parameters:**
- `results` (dict): Test results data
- `pass_criteria` (dict): Pass/fail criteria

**Returns:**
- `dict`: Validation result with status ('PASS'/'FAIL') and detailed compliance information

## Session State Variables

The module uses the following session state variables:

- `staff_registry`: List of staff member dictionaries
- `test_standards`: List of test standard dictionaries
- `test_protocols`: List of protocol template dictionaries
- `test_results`: List of test result dictionaries
- `staff_assignments`: List of task assignments
- `staff_calendar_events`: List of calendar events (holidays, shifts, assignments)

## Data Structures

### Staff Member
```python
{
    'staff_id': 'STF-001',
    'name': 'Dr. Sarah Chen',
    'role': 'Senior Test Engineer',
    'expertise_areas': ['IEC 61215 Testing', 'Thermal Cycling'],
    'certifications': [
        {'cert_name': 'IEC 61215 Certification', 'expiry_date': '2025-12-31'}
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
}
```

### Test Standard
```python
{
    'test_id': 'IEC-61215-001',
    'standard_name': 'IEC 61215',
    'version': '2021',
    'method_number': '10.8',
    'test_name': 'Thermal Cycling Test',
    'description': 'Test to determine ability to withstand thermal cycling...',
    'category': 'Environmental',
    'duration_hours': 200,
    'equipment_required': ['Thermal Chamber', 'Temperature Logger']
}
```

### Protocol Template
```python
{
    'protocol_id': 'PROT-TC-001',
    'test_id': 'IEC-61215-001',
    'protocol_name': 'Thermal Cycling Protocol - Standard Modules',
    'version': '1.2',
    'steps': [
        {'step': 1, 'instruction': 'Visual inspection...', 'duration_min': 15}
    ],
    'expected_results': {
        'max_power_degradation': 5,
        'visual_defects': 'None'
    },
    'pass_criteria': {
        'power_degradation_limit': 5.0,
        'no_visual_defects': True
    },
    'operator_instructions': 'Ensure chamber is calibrated...',
    'safety_notes': 'High temperature hazard...',
    'created_date': '2024-01-15',
    'approved_by': 'Maria Santos'
}
```

### Test Result
```python
{
    'result_id': 'RESULT-abc123',
    'protocol_id': 'PROT-TC-001',
    'sample_id': 'SAMPLE-001',
    'operator_name': 'James Rodriguez',
    'test_date': '2025-11-07',
    'equipment_id': 'CHAMBER-01',
    'results': {
        'power_degradation': 2.5,
        'initial_power': 300.0,
        'final_power': 292.5,
        'visual_defects': 'No'
    },
    'compliance_status': 'PASS',
    'compliance_details': [...],
    'timestamp': '2025-11-07 10:30:45'
}
```

## Error Handling

All functions include comprehensive error handling:

- Form validation with clear error messages
- Missing data checks
- Date range validation
- Capacity overflow prevention
- Graceful handling of empty datasets

## Best Practices

1. **Initialize Early**: Call `initialize_manpower_protocols_data()` at app startup
2. **Check Availability**: Always verify staff availability before manual assignments
3. **Monitor Capacity**: Watch utilization percentages to prevent overload
4. **Track Certifications**: Set up regular checks for expiring certifications
5. **Validate Data**: Use the auto-validation features for test results
6. **Export Regularly**: Use export functions for backup and reporting

## Troubleshooting

### No Data Appears
- Ensure `initialize_manpower_protocols_data()` has been called
- Check that session_state variables are accessible

### Assignment Fails
- Verify staff members are marked as available
- Check that staff have available capacity
- Ensure required skills match staff expertise

### Validation Issues
- Confirm pass_criteria structure matches expected format
- Verify all required measurements are provided
- Check data types (numeric fields must be numbers)

## Future Enhancements

Potential areas for expansion:
- Email notifications for certification expiry
- Advanced analytics and trend analysis
- Integration with equipment scheduling
- Multi-project resource allocation
- Automated report generation
- Mobile-responsive calendar views

## Support

For issues or questions:
1. Check this documentation
2. Review the demo application code
3. Inspect session_state variables
4. Check Streamlit console for error messages

## License

This module is part of the Solar PV Project Management System.

---

**Module ID:** MANPOWER_PROTOCOLS_SESSION3
**Last Updated:** 2025-11-07
**Status:** ✅ Production Ready
