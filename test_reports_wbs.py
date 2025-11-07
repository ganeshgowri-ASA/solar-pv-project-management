"""
Test script for reports_wbs_session5 module
"""

import sys
sys.path.append('/home/user/solar-pv-project-management')

import reports_wbs_session5 as rwbs
from datetime import datetime

def test_module_id():
    """Test module ID is correct"""
    assert rwbs.MODULE_ID == 'REPORTS_WBS_SESSION5', "Module ID mismatch"
    print("✓ Module ID: REPORTS_WBS_SESSION5")

def test_wbs_creation():
    """Test WBS structure creation"""
    wbs = rwbs.create_sample_wbs()
    assert len(wbs) > 0, "WBS structure is empty"
    assert any(node['wbs_id'] == 'WBS-1.0' for node in wbs), "Root node not found"

    # Count phases and tasks
    phases = [n for n in wbs if n['type'] == 'phase']
    tasks = [n for n in wbs if n['type'] == 'task']

    assert len(phases) == 3, f"Expected 3 phases, got {len(phases)}"
    assert len(tasks) == 12, f"Expected 12 tasks, got {len(tasks)}"

    print(f"✓ WBS Structure: 1 project, {len(phases)} phases, {len(tasks)} tasks")

def test_baselines():
    """Test baseline creation"""
    baselines = rwbs.create_sample_baselines()
    assert len(baselines) == 2, f"Expected 2 baselines, got {len(baselines)}"
    assert baselines[0]['baseline_id'] == 'BL001', "First baseline ID incorrect"
    assert baselines[1]['baseline_id'] == 'BL002', "Second baseline ID incorrect"
    print(f"✓ Baselines: {len(baselines)} baselines created")

def test_wbs_utility_functions():
    """Test WBS utility functions"""
    # Create a mock session state
    class MockSessionState:
        def __init__(self):
            self.wbs_structure = rwbs.create_sample_wbs()

    import streamlit as st
    st.session_state = MockSessionState()

    # Test get_wbs_node
    node = rwbs.get_wbs_node('WBS-1.0')
    assert node is not None, "Root node not found"
    assert node['name'] == 'Solar PV Module Testing & Certification Project'
    print("✓ get_wbs_node() works")

    # Test get_children
    children = rwbs.get_children('WBS-1.0')
    assert len(children) == 3, f"Expected 3 children for root, got {len(children)}"
    print("✓ get_children() works")

    # Test rollup calculations
    progress = rwbs.calculate_rollup_progress('WBS-1.1')
    assert 0 <= progress <= 100, "Progress out of range"
    print(f"✓ calculate_rollup_progress() = {progress:.1f}%")

    # Test critical path
    critical_tasks = rwbs.find_critical_path()
    assert len(critical_tasks) > 0, "No critical tasks found"
    print(f"✓ find_critical_path() found {len(critical_tasks)} critical tasks")

def test_report_functions():
    """Test report generation functions exist"""
    functions = [
        'render_test_report',
        'render_equipment_performance_report',
        'render_manpower_utilization_report',
        'render_project_status_report',
        'render_compliance_report',
        'render_report_builder_ui'
    ]

    for func_name in functions:
        assert hasattr(rwbs, func_name), f"Function {func_name} not found"

    print(f"✓ All {len(functions)} report functions exist")

def test_visualization_functions():
    """Test visualization functions exist"""
    functions = [
        'render_wbs_tree',
        'render_wbs_gantt',
        'render_wbs_performance_analytics',
        'render_baseline_comparison'
    ]

    for func_name in functions:
        assert hasattr(rwbs, func_name), f"Function {func_name} not found"

    print(f"✓ All {len(functions)} visualization functions exist")

def test_export_functions():
    """Test export functions exist"""
    functions = [
        'generate_test_report_pdf',
        'generate_test_report_excel',
        'generate_equipment_report_excel',
        'generate_manpower_report_excel',
        'generate_project_status_pdf',
        'generate_compliance_report_pdf'
    ]

    for func_name in functions:
        assert hasattr(rwbs, func_name), f"Function {func_name} not found"

    print(f"✓ All {len(functions)} export functions exist")

def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("Testing reports_wbs_session5 module")
    print("=" * 60)

    try:
        test_module_id()
        test_wbs_creation()
        test_baselines()
        test_wbs_utility_functions()
        test_report_functions()
        test_visualization_functions()
        test_export_functions()

        print("=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
