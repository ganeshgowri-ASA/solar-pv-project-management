# Solar PV Test Project Management System - User Guide

## Welcome

Welcome to the Solar PV Test Project Management System - a comprehensive, modular application designed specifically for managing solar photovoltaic testing projects. This guide will help you navigate and use all features effectively.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Features](#core-features)
3. [Advanced Modules](#advanced-modules)
4. [Common Workflows](#common-workflows)
5. [Tips and Best Practices](#tips-and-best-practices)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### Launching the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### User Interface Overview

- **Sidebar (Left)**: Navigation menu and user information
- **Main Area**: Content and interactive features
- **Module Status**: Shows which advanced modules are loaded

### Navigation

Use the sidebar radio buttons to switch between different sections:
- Core features (Dashboard, Projects, etc.)
- Advanced modules (if available)

---

## Core Features

### 1. Dashboard

**Purpose:** Get a quick overview of all project activities

**Features:**
- Real-time project metrics and KPIs
- Task completion statistics
- Equipment utilization charts
- Upcoming deadlines
- Recent notifications

**How to Use:**
1. Select "📊 Dashboard" from navigation
2. View key metrics at the top
3. Scroll to see detailed charts
4. Click on metrics for drill-down views

### 2. Project Management

**Purpose:** Manage project lifecycle from initiation to completion

**Features:**
- Create and edit projects
- Set budgets and timelines
- Assign project managers
- Track project status
- Monitor budget vs. actual spending

**How to Use:**
1. Select "📋 Project Management"
2. Click "Add New Project" to create
3. Fill in project details
4. Click "Save" to confirm
5. Edit existing projects by selecting from the list

**Key Fields:**
- Project ID (auto-generated)
- Project Name
- Client
- Start/End Dates
- Budget
- Priority Level
- Status

### 3. Views

**Purpose:** Visualize project data in different formats

**Available Views:**
- **Gantt Chart**: Timeline visualization with dependencies
- **Calendar View**: Monthly calendar with events and milestones
- **WBS Tree**: Hierarchical work breakdown structure
- **Kanban Board**: Task flow visualization
- **Network Diagram**: Project dependencies

**How to Use:**
1. Select "👁️ Views"
2. Choose your desired view from tabs
3. Use filters to customize display
4. Export visualizations as needed

### 4. Solar Testing

**Purpose:** Manage test samples and testing processes

**Features:**
- Sample registration and tracking
- Chain of custody management
- Barcode/QR code generation
- Test status monitoring
- Sample location tracking

**How to Use:**
1. Select "☀️ Solar Testing"
2. Add new samples with "Register Sample"
3. Track sample movement with chain of custody
4. Update test status as work progresses
5. Generate barcode labels

**Sample Workflow:**
1. Receive sample → Register in system
2. Assign barcode → Print label
3. Move to storage → Log custody change
4. Begin testing → Update status
5. Complete tests → Record results

### 5. Workflows

**Purpose:** Manage approval and review processes

**Features:**
- Sample workflow tracking
- Approval routing
- Digital signatures
- Workflow status visualization
- Automated notifications

**How to Use:**
1. Select "📝 Workflows"
2. View current workflows
3. Submit items for approval
4. Track approval status
5. Receive notifications on decisions

### 6. Resources

**Purpose:** Manage equipment and team members

**Features:**
- Equipment registry
- Equipment booking
- Calibration tracking
- Team member profiles
- Skills and certifications
- Resource availability

**How to Use:**
1. Select "👥 Resources"
2. Choose "Equipment" or "Manpower" tab
3. Add/edit resources
4. Book equipment for projects
5. Track calibration schedules

### 7. Risks & Issues

**Purpose:** Identify and manage project risks and issues

**Features:**
- Risk assessment and tracking
- Issue logging and resolution
- Priority levels
- Impact analysis
- Mitigation strategies

**How to Use:**
1. Select "⚠️ Risks & Issues"
2. Log new risks or issues
3. Assess impact and probability
4. Assign resolution owners
5. Track to closure

### 8. Reports

**Purpose:** Generate project reports and analytics

**Features:**
- Project status reports
- Test result summaries
- Resource utilization reports
- Custom report builder
- PDF export

**How to Use:**
1. Select "📄 Reports"
2. Choose report type
3. Set parameters and filters
4. Generate report
5. Download PDF if needed

### 9. Notifications

**Purpose:** Stay informed of important events

**Features:**
- Real-time notifications
- Priority levels
- Read/unread tracking
- Notification history

**How to Use:**
1. Select "🔔 Notifications"
2. View unread notifications first
3. Click "Mark as Read" when reviewed
4. Expand "Read" section for history

---

## Advanced Modules

### Module 1: 🔬 Flowcharts & Equipment

**Purpose:** Advanced workflow visualization and equipment management

#### Features:

**A. Workflow Flowcharts**
- Visual workflow design
- Node-based workflow builder
- Process flow visualization
- Real-time status updates

**How to Use:**
1. Navigate to "🔬 Flowcharts & Equipment"
2. Select "Workflow Flowcharts" tab
3. View existing workflows
4. Click nodes to see details
5. Track workflow progress

**B. Equipment Dashboard**
- Performance metrics
- Utilization statistics
- Calibration alerts
- Maintenance schedules

**How to Use:**
1. Select "Equipment Dashboard" tab
2. View equipment performance metrics
3. Check calibration status
4. Review upcoming maintenance

**C. Equipment Availability**
- Real-time availability calendar
- Equipment booking system
- Conflict detection
- Resource optimization

**How to Use:**
1. Select "Equipment Availability" tab
2. Choose date range
3. View availability
4. Book equipment as needed

**D. Maintenance Logs**
- Detailed maintenance history
- Service records
- Part replacements
- Performance trends

**How to Use:**
1. Select "Maintenance Logs" tab
2. Choose equipment
3. View maintenance history
4. Add new maintenance records

### Module 2: 👥 Manpower & Protocols

**Purpose:** Advanced staff management and test protocol system

#### Features:

**A. Manpower Dashboard**
- Staff registry with certifications
- Skills matrix
- Performance metrics
- Workload analysis
- Certification expiry alerts

**How to Use:**
1. Navigate to "👥 Manpower & Protocols"
2. Select "Manpower Dashboard" tab
3. View staff profiles
4. Track certifications
5. Monitor workload

**B. Availability Calendar**
- Staff scheduling
- Leave management
- Project assignments
- Capacity planning

**How to Use:**
1. Select "Availability Calendar" tab
2. View staff availability
3. Schedule assignments
4. Plan project resources

**C. Test Selection & Protocols**
- Comprehensive protocol library
- Standards: IEC, UL, IEEE, ASTM
- Protocol search and filtering
- Requirements documentation

**How to Use:**
1. Select "Test Selection & Protocols" tab
2. Search for test standards
3. View protocol requirements
4. Select applicable tests

**D. Protocol Entry Sheet**
- Step-by-step test execution
- Data entry forms
- Real-time validation
- Pass/fail criteria checking
- Compliance verification

**How to Use:**
1. Select "Protocol Entry Sheet" tab
2. Choose protocol
3. Fill in test data
4. System validates against criteria
5. Save results

**E. Test Results Table**
- Comprehensive results view
- Pass/fail status
- Compliance details
- Step completion tracking
- Results export

**How to Use:**
1. Select "Test Results" tab
2. View all test results
3. Filter by status/protocol
4. Export data as needed

### Module 3: ✅ Approval Automation

**Purpose:** Automated approval workflows with digital signatures

#### Features:

**A. Approval Dashboard**
- Pending approvals queue
- Approval history
- Status tracking
- Priority indicators

**How to Use:**
1. Navigate to "✅ Approval Automation"
2. Select "Approval Dashboard"
3. View pending items
4. Click to review details

**B. Approval Processing**
- Digital signature generation
- Multi-level approvals
- Comments and feedback
- Rejection with reasons

**How to Use:**
1. Select item to review
2. Review test results/documents
3. Click "Approve" or "Reject"
4. Add comments if needed
5. System generates digital signature

**C. Automation Rules**
- Rule-based routing
- Automatic approval for compliant results
- Escalation workflows
- Custom conditions

**How to Use:**
1. Select "Automation Rules"
2. View active rules
3. Configure conditions
4. Set actions
5. Enable/disable rules

**D. Notifications**
- Approval requests
- Status updates
- Escalation alerts
- Email integration

**How to Use:**
1. Select "Notifications"
2. View approval notifications
3. Click to take action
4. Mark as read when done

**E. Audit Trail**
- Complete action history
- User tracking
- Timestamp logging
- Signature verification

**How to Use:**
1. Select "Test Functions" or view from dashboard
2. Search audit log
3. Filter by user/date/action
4. Export for compliance

### Module 4: 📊 Advanced Reports & WBS

**Purpose:** Comprehensive reporting and work breakdown structure analysis

#### Features:

**A. Reports**
- Test Result Reports
- Equipment Performance Reports
- Manpower Utilization Reports
- Project Status Reports
- Compliance Reports

**How to Use:**
1. Navigate to "📊 Advanced Reports & WBS"
2. Select "Reports" tab
3. Choose report type
4. Set parameters
5. Generate and download PDF

**B. WBS Structure**
- Hierarchical work breakdown
- Task organization
- Cost and time rollups
- Progress tracking
- Interactive tree view

**How to Use:**
1. Select "WBS Structure" tab
2. View hierarchical structure
3. Expand/collapse nodes
4. See rollup calculations
5. Track progress

**C. Performance Analytics**
- Earned Value Management (EVM)
- Schedule Performance Index (SPI)
- Cost Performance Index (CPI)
- Variance analysis
- Forecasting

**How to Use:**
1. Select "Performance Analytics" tab
2. View EVM metrics
3. Analyze variances
4. Review forecasts
5. Identify trends

**D. Baseline Comparison**
- Original vs. current plan
- Schedule variance
- Cost variance
- Scope changes
- Trend analysis

**How to Use:**
1. Select baseline to compare
2. View variance charts
3. Analyze deviations
4. Generate variance reports

---

## Common Workflows

### Workflow 1: Creating and Managing a New Project

1. **Create Project**
   - Go to "📋 Project Management"
   - Click "Add New Project"
   - Fill in details
   - Save

2. **Set Up WBS** (if using Advanced Reports module)
   - Go to "📊 Advanced Reports & WBS"
   - Select "WBS Structure"
   - Build task hierarchy
   - Set dependencies

3. **Assign Resources**
   - Go to "👥 Resources" or "👥 Manpower & Protocols"
   - Assign team members
   - Book equipment

4. **Track Progress**
   - Update task status regularly
   - Log issues and risks
   - Monitor dashboard

### Workflow 2: Processing Test Samples

1. **Register Sample**
   - Go to "☀️ Solar Testing"
   - Register new sample
   - Generate barcode

2. **Select Test Protocol** (if using Manpower & Protocols module)
   - Go to "👥 Manpower & Protocols"
   - Select "Test Selection & Protocols"
   - Choose applicable standards

3. **Execute Test**
   - Use "Protocol Entry Sheet"
   - Follow step-by-step procedure
   - Enter measurements

4. **Submit for Approval** (if using Approval Automation module)
   - Results auto-routed
   - Digital signature applied
   - Notifications sent

5. **Generate Report** (if using Advanced Reports module)
   - Go to "📊 Advanced Reports & WBS"
   - Select "Test Result Report"
   - Generate PDF

### Workflow 3: Equipment Calibration and Maintenance

1. **Check Due Calibrations** (if using Flowcharts & Equipment module)
   - Go to "🔬 Flowcharts & Equipment"
   - Select "Equipment Dashboard"
   - View calibration alerts

2. **Schedule Calibration**
   - Check "Equipment Availability"
   - Book time slot
   - Assign technician

3. **Perform Calibration**
   - Execute calibration procedure
   - Record results

4. **Update Records**
   - Go to "Maintenance Logs"
   - Add calibration record
   - Update next due date

### Workflow 4: Staff Assignment and Tracking

1. **Check Staff Availability** (if using Manpower & Protocols module)
   - Go to "👥 Manpower & Protocols"
   - Select "Availability Calendar"
   - View staff schedules

2. **Verify Qualifications**
   - Check "Manpower Dashboard"
   - Review certifications
   - Ensure skills match requirements

3. **Assign to Task**
   - Use task assignment function
   - System checks availability and skills
   - Confirmation sent

4. **Track Utilization**
   - Monitor workload
   - Review performance metrics
   - Plan future assignments

---

## Tips and Best Practices

### General Tips

1. **Regular Updates**
   - Update task status daily
   - Log issues immediately
   - Keep sample tracking current

2. **Use Filters**
   - Most views support filtering
   - Narrow down to relevant data
   - Save time finding information

3. **Export Data**
   - Export reports regularly
   - Keep offline backups
   - Share with stakeholders

4. **Notifications**
   - Review notifications daily
   - Act on high-priority items first
   - Clear old notifications

### Module-Specific Tips

**Flowcharts & Equipment:**
- Set up calibration reminders early
- Book equipment in advance
- Log all maintenance activities
- Review utilization monthly

**Manpower & Protocols:**
- Keep certifications up to date
- Use protocol templates
- Validate data as you enter
- Track certification expiry proactively

**Approval Automation:**
- Configure automation rules carefully
- Review audit trail regularly
- Use comments for clarity
- Set appropriate escalation times

**Advanced Reports & WBS:**
- Update baselines for major changes
- Review variances weekly
- Use EVM for project health
- Generate status reports regularly

### Performance Tips

1. **Page Load**
   - Application loads all data on start
   - Be patient on first load
   - Subsequent navigation is fast

2. **Data Entry**
   - Fill all required fields
   - Use consistent formatting
   - Validate before saving

3. **Large Datasets**
   - Use date range filters
   - Limit displayed records
   - Export for detailed analysis

---

## Troubleshooting

### Common Issues

**Issue: Module not appearing in menu**
- **Cause**: Module file missing or import error
- **Solution**: Check that module .py file is in same directory as app.py
- **Status**: Check sidebar for module status message

**Issue: Data not saving**
- **Cause**: Session state issue or validation error
- **Solution**: Check for error messages, ensure all required fields filled

**Issue: Charts not displaying**
- **Cause**: No data available or date range too narrow
- **Solution**: Expand date range, check that data exists

**Issue: Calibration alerts not showing**
- **Cause**: Equipment module not loaded or no equipment data
- **Solution**: Ensure flowchart_equipment.py is available

**Issue: Approval workflow not triggering**
- **Cause**: Automation rules not configured or module not loaded
- **Solution**: Check automation rules in Approval Automation module

### Getting Help

1. **Check Documentation**
   - Read this guide
   - Review `CONSOLIDATED_APP_ARCHITECTURE.md`
   - Check `README.md`

2. **Module Status**
   - Look at sidebar module status
   - Check console for error messages

3. **Data Validation**
   - Review error messages
   - Check required fields
   - Verify data formats

### Known Limitations

1. **Session State**
   - Data persists only during session
   - Browser refresh clears data
   - Use export for permanent storage

2. **Concurrent Users**
   - Each user has separate session
   - No real-time collaboration yet
   - Future: database backend planned

3. **Large Files**
   - PDF generation may be slow for large reports
   - Complex charts may take time to render

4. **Browser Compatibility**
   - Best in Chrome/Firefox
   - Some features may not work in older browsers

---

## Keyboard Shortcuts

Streamlit provides some built-in shortcuts:
- `R` - Rerun the application
- `C` - Clear cache
- `?` - Show keyboard shortcuts

---

## Best Practices Summary

### Daily Activities
- [ ] Review Dashboard for overview
- [ ] Check and respond to notifications
- [ ] Update task status
- [ ] Log any issues or risks

### Weekly Activities
- [ ] Review project progress
- [ ] Check equipment calibration schedules
- [ ] Review staff workload and availability
- [ ] Generate status reports
- [ ] Review pending approvals

### Monthly Activities
- [ ] Generate comprehensive reports
- [ ] Review WBS and update baselines if needed
- [ ] Analyze performance metrics
- [ ] Review and update automation rules
- [ ] Audit trail review
- [ ] Certification expiry check

---

## Quick Reference

### Module IDs
- Core Application: Session 1
- Flowcharts & Equipment: `FLOWCHART_EQUIPMENT`
- Manpower & Protocols: `MANPOWER_PROTOCOLS_SESSION3`
- Approval Automation: `APPROVAL_AUTOMATION_SESSION4`
- Advanced Reports & WBS: `REPORTS_WBS_SESSION5`

### Feature Availability

| Feature | Core | Module |
|---------|------|--------|
| Dashboard | ✓ | - |
| Project Management | ✓ | - |
| Basic Views | ✓ | - |
| Sample Testing | ✓ | - |
| Basic Workflows | ✓ | - |
| Basic Resources | ✓ | - |
| Risks & Issues | ✓ | - |
| Basic Reports | ✓ | - |
| Notifications | ✓ | - |
| Advanced Flowcharts | - | Session 2 |
| Equipment Analytics | - | Session 2 |
| Test Protocols | - | Session 3 |
| Staff Management | - | Session 3 |
| Approval Automation | - | Session 4 |
| Digital Signatures | - | Session 4 |
| Advanced WBS | - | Session 5 |
| EVM Analytics | - | Session 5 |

---

## Conclusion

This Solar PV Test Project Management System provides comprehensive tools for managing all aspects of solar panel testing projects. The modular architecture allows you to use core features immediately while adding advanced capabilities as needed.

For technical details, see `CONSOLIDATED_APP_ARCHITECTURE.md`.

**Version:** 2.0
**Last Updated:** 2024-11-08
**Status:** Production Ready

---

## Feedback and Support

If you encounter issues or have suggestions:
1. Check this guide and architecture documentation
2. Review error messages and module status
3. Document the issue with screenshots if possible
4. Contact your system administrator

Enjoy using the Solar PV Test Project Management System!
