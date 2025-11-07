# Flowchart & Equipment Management Module

**Module ID:** `FLOWCHART_EQUIPMENT_SESSION2`
**Version:** 1.0
**File:** `flowchart_equipment.py`

## Overview

This module provides independent, modular functions for workflow visualization and equipment management in the Solar PV Project Management system. All functions are self-contained and use Streamlit session state for data storage.

## Features

### 1. Flowchart View Module

Interactive workflow visualization using Plotly with hierarchical layout:

- **Function:** `render_flowchart_view()`
- **Node Hierarchy:** Project → Phases → Tasks → Tests → Approvals → Reports
- **Status Colors:**
  - Pending: Gray (#808080)
  - In-Progress: Yellow (#FFD700)
  - Completed: Green (#00AA00)
  - Blocked: Red (#FF0000)
- **Interactive Features:**
  - Hover details for each node
  - Click handlers for drill-down
  - Status summary metrics
  - Filterable node tables by type

### 2. Equipment Dashboard

Comprehensive equipment management interface:

- **Function:** `render_equipment_dashboard()`
- **Equipment Data Model:**
  ```python
  {
    'equipment_id': str,
    'name': str,
    'type': str,
    'model': str,
    'serial': str,
    'calibration_date': str (YYYY-MM-DD),
    'last_service': str (YYYY-MM-DD),
    'status': str (available/in-use/maintenance),
    'location': str,
    'tests_completed': int,
    'avg_time': float,
    'success_rate': float,
    'downtime_hours': float
  }
  ```
- **Features:**
  - Overview metrics (total, available, in-use equipment)
  - Calibration alerts (critical overdue, warning < 30 days)
  - Equipment inventory table with filters
  - Status and type distribution charts
  - Performance metrics (success rate, downtime)
  - Test completion analytics

### 3. Equipment Availability Calendar

Gantt-style booking calendar:

- **Function:** `render_equipment_availability()`
- **Booking Data Model:**
  ```python
  {
    'booking_id': str,
    'equipment_id': str,
    'start_date': str (YYYY-MM-DD),
    'end_date': str (YYYY-MM-DD),
    'booked_by': str,
    'purpose': str,
    'status': str (confirmed/pending/completed)
  }
  ```
- **Features:**
  - Timeline visualization of bookings
  - Booking details table with filters
  - Current availability status
  - Utilization analytics
  - Booking conflict detection

### 4. Maintenance Logs

Complete maintenance tracking system:

- **Function:** `render_maintenance_logs()`
- **Log Data Model:**
  ```python
  {
    'log_id': str,
    'equipment_id': str,
    'date': str (YYYY-MM-DD HH:MM:SS),
    'type': str (Calibration/Repair/Inspection/Cleaning),
    'technician': str,
    'notes': str,
    'cost': float,
    'duration_hours': float
  }
  ```
- **Features:**
  - Maintenance history table with filters
  - Cost analysis by type and equipment
  - Timeline visualization
  - Type distribution charts
  - Technician tracking

## Installation & Usage

### Quick Start

```python
# In your Streamlit app (app.py)
import flowchart_equipment as fe

# Initialize data (call once at app startup)
fe.initialize_workflow_data()
fe.initialize_equipment_data()

# Create UI tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Flowchart View",
    "🔧 Equipment Dashboard",
    "📅 Equipment Availability",
    "🔨 Maintenance Logs"
])

with tab1:
    fe.render_flowchart_view()

with tab2:
    fe.render_equipment_dashboard()

with tab3:
    fe.render_equipment_availability()

with tab4:
    fe.render_maintenance_logs()
```

### Standalone Demo

```python
# Run complete demo with all features
import flowchart_equipment as fe

fe.demo_all_features()
```

## Data Storage

All data is stored in Streamlit session state:

- `st.session_state.workflow_data` - Workflow nodes and edges
- `st.session_state.equipment_registry` - Equipment inventory
- `st.session_state.equipment_bookings` - Equipment bookings
- `st.session_state.maintenance_logs` - Maintenance history

## Sample Data

The module includes comprehensive sample data for testing:

- **Workflow:** 14 nodes across 6 levels (1 project, 3 phases, 4 tasks, 3 tests, 2 approvals, 1 report)
- **Equipment:** 5 equipment items with realistic metrics
- **Bookings:** 15 sample bookings across different time periods
- **Maintenance:** 20 maintenance log entries

## Testing & Validation

### Validate Module Structure

```bash
python validate_module.py
```

This will check:
- Module loading
- Function signatures
- Docstrings
- Required imports
- File structure

### Test Functions

```bash
python test_flowchart_equipment.py
```

Note: Full testing requires Streamlit app context.

## Integration with Existing App

The module is designed to be **non-invasive**:

- ✅ No modifications to existing `app.py` required
- ✅ Uses session state (no database changes)
- ✅ Independent functions (no dependencies on existing code)
- ✅ Self-contained data initialization
- ✅ Can be imported and used anywhere in the app

### Adding to Existing Tabs

```python
# Option 1: Add as new tabs
import flowchart_equipment as fe

# In your main tab selection
selected_tab = st.sidebar.radio("Navigation", [
    "Dashboard",
    "Projects",
    "Tasks",
    "Flowchart View",  # NEW
    "Equipment Management"  # NEW
])

if selected_tab == "Flowchart View":
    fe.render_flowchart_view()
elif selected_tab == "Equipment Management":
    # Create sub-tabs for equipment features
    eq_tab = st.tabs(["Dashboard", "Availability", "Maintenance"])
    with eq_tab[0]:
        fe.render_equipment_dashboard()
    with eq_tab[1]:
        fe.render_equipment_availability()
    with eq_tab[2]:
        fe.render_maintenance_logs()
```

### Custom Data Integration

Replace sample data with your own:

```python
import flowchart_equipment as fe

# Custom workflow data
st.session_state.workflow_data = {
    'nodes': [
        {'id': 'node1', 'label': 'My Node', 'type': 'Task',
         'status': 'completed', 'level': 1}
        # ... more nodes
    ],
    'edges': [
        {'source': 'node1', 'target': 'node2'}
        # ... more edges
    ]
}

# Custom equipment data
st.session_state.equipment_registry = [
    {
        'equipment_id': 'EQ001',
        'name': 'My Equipment',
        # ... other fields
    }
    # ... more equipment
]

# Now call render functions
fe.render_flowchart_view()
fe.render_equipment_dashboard()
```

## API Reference

### Initialization Functions

#### `initialize_workflow_data()`
Initialize sample workflow data for testing.

**Parameters:** None
**Returns:** None (stores in `st.session_state.workflow_data`)

#### `initialize_equipment_data()`
Initialize sample equipment registry, bookings, and maintenance logs.

**Parameters:** None
**Returns:** None (stores in `st.session_state`)

### Render Functions

#### `render_flowchart_view()`
Render interactive workflow flowchart using Plotly.

**Parameters:** None
**Returns:** None (renders directly to Streamlit)

#### `render_equipment_dashboard()`
Render equipment dashboard with overview, table, charts, and metrics.

**Parameters:** None
**Returns:** None (renders directly to Streamlit)

#### `render_equipment_availability()`
Render equipment availability calendar view with bookings.

**Parameters:** None
**Returns:** None (renders directly to Streamlit)

#### `render_maintenance_logs()`
Render maintenance logs with timestamps and filtering.

**Parameters:** None
**Returns:** None (renders directly to Streamlit)

### Helper Functions

#### `get_status_color(status: str) -> str`
Get color code for status.

**Parameters:**
- `status` (str): Status string (pending/in-progress/completed/blocked)

**Returns:** str - Color hex code

#### `create_flowchart_layout(nodes: List[Dict], edges: List[Dict]) -> Tuple[Dict, Dict]`
Create hierarchical layout for flowchart nodes.

**Parameters:**
- `nodes` (List[Dict]): List of node dictionaries
- `edges` (List[Dict]): List of edge dictionaries

**Returns:** Tuple of (positions dict, node_map dict)

#### `check_calibration_alerts(equipment_df: pd.DataFrame) -> pd.DataFrame`
Check for equipment calibration alerts.

**Parameters:**
- `equipment_df` (pd.DataFrame): DataFrame with equipment data

**Returns:** pd.DataFrame - DataFrame with alert information

### Demo Function

#### `demo_all_features()`
Demonstration function showing all features of the module.

**Parameters:** None
**Returns:** None (renders complete demo app)

## Error Handling

All render functions include comprehensive error handling:

```python
try:
    # Function logic
except Exception as e:
    st.error(f"Error rendering [feature]: {str(e)}")
    import traceback
    st.error(traceback.format_exc())
```

## Dependencies

Required packages (from `requirements.txt`):
- `streamlit >= 1.28.0`
- `pandas >= 2.0.0`
- `plotly >= 5.17.0`
- `numpy >= 1.24.0`

## Performance Considerations

- **Lazy Loading:** Data is only initialized when functions are called
- **Caching:** Uses session state to avoid re-initialization
- **Efficient Rendering:** Plotly charts are optimized for interactivity
- **Filtering:** Client-side filtering for responsive UI

## Customization

### Modify Status Colors

```python
# In flowchart_equipment.py, update get_status_color()
color_map = {
    'pending': '#YOUR_COLOR',
    'in-progress': '#YOUR_COLOR',
    'completed': '#YOUR_COLOR',
    'blocked': '#YOUR_COLOR'
}
```

### Add New Node Types

```python
# Add to workflow_nodes in initialize_workflow_data()
{'id': 'new_1', 'label': 'New Type', 'type': 'NewType',
 'status': 'pending', 'level': 6}
```

### Customize Calibration Warning Period

```python
# In check_calibration_alerts(), change:
warning_days = 30  # Change to your preferred value
```

## Troubleshooting

### Issue: Functions not rendering

**Solution:** Ensure data is initialized before calling render functions:
```python
fe.initialize_workflow_data()
fe.initialize_equipment_data()
fe.render_flowchart_view()
```

### Issue: No data showing

**Solution:** Check session state:
```python
import streamlit as st
st.write(st.session_state.workflow_data)
st.write(st.session_state.equipment_registry)
```

### Issue: Import errors

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

## License

Part of the Solar PV Project Management System.

## Support

For issues or questions, refer to:
- Module validation: `python validate_module.py`
- Test script: `python test_flowchart_equipment.py`
- Source code: `flowchart_equipment.py`

## Version History

### Version 1.0 (SESSION2)
- Initial release
- Flowchart view with hierarchical layout
- Equipment dashboard with metrics
- Availability calendar with Gantt view
- Maintenance logs with analytics
- Complete sample data
- Full error handling
- Comprehensive documentation
