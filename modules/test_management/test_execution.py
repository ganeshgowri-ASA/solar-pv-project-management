"""
Test Execution Management with Digital Test Sheets and Real-time Validation
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid
import json

from .models import TestResult, TestSchedule, TestProtocol, TestStatus


class TestExecutor:
    """Manages test execution with digital test sheets and validation"""

    def __init__(self):
        self.test_results: Dict[str, TestResult] = {}
        self.active_tests: Dict[str, Dict[str, Any]] = {}  # Tests in progress with partial data

    def start_test_execution(self,
                           schedule: TestSchedule,
                           protocol: TestProtocol,
                           performed_by: str) -> str:
        """
        Start test execution

        Args:
            schedule: Test schedule
            protocol: Test protocol
            performed_by: Technician performing test

        Returns:
            Result ID for the test execution
        """
        result_id = f"RESULT_{uuid.uuid4().hex[:8].upper()}"

        # Initialize test result
        self.active_tests[result_id] = {
            'result_id': result_id,
            'schedule_id': schedule.schedule_id,
            'sample_id': schedule.sample_id,
            'protocol_id': protocol.protocol_id,
            'performed_by': performed_by,
            'started_at': datetime.now(),
            'current_step': 0,
            'total_steps': len(protocol.steps),
            'measurements': [],
            'images': [],
            'videos': [],
            'notes': '',
            'partial_data': {}
        }

        return result_id

    def record_measurement(self,
                         result_id: str,
                         measurement_name: str,
                         value: Any,
                         unit: str = "",
                         timestamp: Optional[datetime] = None,
                         notes: str = "") -> bool:
        """
        Record a measurement during test execution

        Args:
            result_id: Test result ID
            measurement_name: Name of measurement (e.g., "Voc", "Isc", "Temperature")
            value: Measured value
            unit: Unit of measurement
            timestamp: Measurement timestamp (defaults to now)
            notes: Additional notes

        Returns:
            Success status
        """
        if result_id not in self.active_tests:
            return False

        measurement = {
            'name': measurement_name,
            'value': value,
            'unit': unit,
            'timestamp': timestamp or datetime.now(),
            'notes': notes
        }

        self.active_tests[result_id]['measurements'].append(measurement)
        return True

    def add_image(self, result_id: str, image_path: str, description: str = "") -> bool:
        """Add image to test results"""
        if result_id not in self.active_tests:
            return False

        self.active_tests[result_id]['images'].append({
            'path': image_path,
            'description': description,
            'timestamp': datetime.now()
        })
        return True

    def add_video(self, result_id: str, video_path: str, description: str = "") -> bool:
        """Add video to test results"""
        if result_id not in self.active_tests:
            return False

        self.active_tests[result_id]['videos'].append({
            'path': video_path,
            'description': description,
            'timestamp': datetime.now()
        })
        return True

    def update_step(self, result_id: str, step_number: int) -> bool:
        """Update current step in test execution"""
        if result_id not in self.active_tests:
            return False

        self.active_tests[result_id]['current_step'] = step_number
        return True

    def save_partial_data(self, result_id: str, data: Dict[str, Any]) -> bool:
        """
        Save partial test data (for resume capability)

        Args:
            result_id: Test result ID
            data: Partial data to save

        Returns:
            Success status
        """
        if result_id not in self.active_tests:
            return False

        self.active_tests[result_id]['partial_data'].update(data)
        return True

    def validate_measurement(self,
                           measurement_name: str,
                           value: Any,
                           protocol: TestProtocol) -> Dict[str, Any]:
        """
        Validate measurement against protocol acceptance criteria

        Args:
            measurement_name: Name of measurement
            value: Measured value
            protocol: Test protocol with acceptance criteria

        Returns:
            Validation result with status and messages
        """
        validation_result = {
            'valid': True,
            'warnings': [],
            'errors': [],
            'within_spec': True
        }

        # Get acceptance criteria for this measurement
        criteria = protocol.acceptance_criteria.get(measurement_name)

        if not criteria:
            # No specific criteria, just validate data type
            validation_result['warnings'].append(f"No acceptance criteria defined for {measurement_name}")
            return validation_result

        # Validate based on criteria type
        if isinstance(criteria, dict):
            # Range validation
            if 'min' in criteria and value < criteria['min']:
                validation_result['valid'] = False
                validation_result['within_spec'] = False
                validation_result['errors'].append(
                    f"{measurement_name} = {value} is below minimum {criteria['min']}"
                )

            if 'max' in criteria and value > criteria['max']:
                validation_result['valid'] = False
                validation_result['within_spec'] = False
                validation_result['errors'].append(
                    f"{measurement_name} = {value} exceeds maximum {criteria['max']}"
                )

            # Tolerance validation
            if 'nominal' in criteria and 'tolerance' in criteria:
                nominal = criteria['nominal']
                tolerance = criteria['tolerance']
                deviation = abs(value - nominal) / nominal * 100

                if deviation > tolerance:
                    validation_result['warnings'].append(
                        f"{measurement_name} deviates {deviation:.1f}% from nominal (tolerance: {tolerance}%)"
                    )

        elif isinstance(criteria, (int, float)):
            # Simple threshold
            if value < criteria:
                validation_result['valid'] = False
                validation_result['within_spec'] = False
                validation_result['errors'].append(
                    f"{measurement_name} = {value} is below threshold {criteria}"
                )

        return validation_result

    def detect_anomalies(self,
                        measurements: List[Dict[str, Any]],
                        protocol: TestProtocol) -> List[str]:
        """
        AI-powered anomaly detection in test results

        This is a simplified version. In production, this would use
        trained ML models for anomaly detection.

        Args:
            measurements: List of measurements
            protocol: Test protocol

        Returns:
            List of detected anomalies
        """
        anomalies = []

        # Group measurements by name
        measurement_groups = {}
        for m in measurements:
            name = m['name']
            if name not in measurement_groups:
                measurement_groups[name] = []
            measurement_groups[name].append(m['value'])

        # Check for anomalies
        for name, values in measurement_groups.items():
            if len(values) < 2:
                continue

            # Statistical anomaly detection (simplified)
            avg = sum(values) / len(values)
            std_dev = (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5

            for i, value in enumerate(values):
                # Check if value is more than 3 standard deviations from mean
                if abs(value - avg) > 3 * std_dev:
                    anomalies.append(
                        f"Anomaly detected in {name} measurement #{i+1}: "
                        f"value {value} deviates significantly from average {avg:.2f}"
                    )

        return anomalies

    def complete_test_execution(self,
                               result_id: str,
                               protocol: TestProtocol,
                               notes: str = "") -> TestResult:
        """
        Complete test execution and create final result

        Args:
            result_id: Test result ID
            protocol: Test protocol
            notes: Final notes

        Returns:
            TestResult object
        """
        if result_id not in self.active_tests:
            raise ValueError(f"Test result {result_id} not found in active tests")

        active_test = self.active_tests[result_id]

        # Validate all measurements
        validation_errors = []
        for measurement in active_test['measurements']:
            validation = self.validate_measurement(
                measurement['name'],
                measurement['value'],
                protocol
            )
            if not validation['valid']:
                validation_errors.extend(validation['errors'])

        # Detect anomalies
        anomalies = self.detect_anomalies(active_test['measurements'], protocol)

        # Determine pass/fail
        if validation_errors:
            pass_fail = "FAIL"
        elif anomalies:
            pass_fail = "PASS_WITH_ANOMALIES"
        else:
            pass_fail = "PASS"

        # Create test result
        test_result = TestResult(
            result_id=result_id,
            schedule_id=active_test['schedule_id'],
            sample_id=active_test['sample_id'],
            protocol_id=active_test['protocol_id'],
            test_data=active_test.get('partial_data', {}),
            measurements=[{
                'name': m['name'],
                'value': m['value'],
                'unit': m.get('unit', ''),
                'timestamp': m['timestamp'].isoformat() if isinstance(m['timestamp'], datetime) else m['timestamp'],
                'notes': m.get('notes', '')
            } for m in active_test['measurements']],
            images=[img['path'] for img in active_test.get('images', [])],
            videos=[vid['path'] for vid in active_test.get('videos', [])],
            pass_fail=pass_fail,
            anomalies_detected=anomalies,
            validation_errors=validation_errors,
            performed_by=active_test['performed_by'],
            performed_date=active_test['started_at'],
            notes=notes
        )

        # Store result
        self.test_results[result_id] = test_result

        # Remove from active tests
        del self.active_tests[result_id]

        return test_result

    def get_active_test(self, result_id: str) -> Optional[Dict[str, Any]]:
        """Get active test details"""
        return self.active_tests.get(result_id)

    def get_test_result(self, result_id: str) -> Optional[TestResult]:
        """Get completed test result"""
        return self.test_results.get(result_id)

    def get_all_results(self) -> List[TestResult]:
        """Get all test results"""
        return list(self.test_results.values())

    def get_results_by_sample(self, sample_id: str) -> List[TestResult]:
        """Get all test results for a sample"""
        return [r for r in self.test_results.values() if r.sample_id == sample_id]

    def get_results_by_protocol(self, protocol_id: str) -> List[TestResult]:
        """Get all test results for a protocol"""
        return [r for r in self.test_results.values() if r.protocol_id == protocol_id]

    def get_pass_fail_statistics(self) -> Dict[str, Any]:
        """Get pass/fail statistics"""
        total = len(self.test_results)
        if total == 0:
            return {
                'total': 0,
                'passed': 0,
                'failed': 0,
                'pass_with_anomalies': 0,
                'pass_rate': 0.0
            }

        passed = len([r for r in self.test_results.values() if r.pass_fail == "PASS"])
        failed = len([r for r in self.test_results.values() if r.pass_fail == "FAIL"])
        pass_with_anomalies = len([r for r in self.test_results.values() if r.pass_fail == "PASS_WITH_ANOMALIES"])

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'pass_with_anomalies': pass_with_anomalies,
            'pass_rate': (passed + pass_with_anomalies) / total * 100
        }

    def export_test_report(self, result_id: str) -> Dict[str, Any]:
        """Export comprehensive test report"""
        if result_id not in self.test_results:
            return {'error': 'Test result not found'}

        result = self.test_results[result_id]

        return {
            'result_id': result.result_id,
            'schedule_id': result.schedule_id,
            'sample_id': result.sample_id,
            'protocol_id': result.protocol_id,
            'performed_by': result.performed_by,
            'performed_date': result.performed_date.isoformat() if isinstance(result.performed_date, datetime) else result.performed_date,
            'pass_fail': result.pass_fail,
            'measurements': result.measurements,
            'test_data': result.test_data,
            'images': result.images,
            'videos': result.videos,
            'anomalies': result.anomalies_detected,
            'validation_errors': result.validation_errors,
            'notes': result.notes,
            'reviewed_by': result.reviewed_by,
            'reviewed_date': result.reviewed_date.isoformat() if isinstance(result.reviewed_date, datetime) else None,
            'export_timestamp': datetime.now().isoformat()
        }

    def review_result(self, result_id: str, reviewed_by: str, approval_status: str, comments: str = "") -> bool:
        """
        Review and approve/reject test result

        Args:
            result_id: Test result ID
            reviewed_by: Reviewer name
            approval_status: "Approved" or "Rejected"
            comments: Review comments

        Returns:
            Success status
        """
        if result_id not in self.test_results:
            return False

        result = self.test_results[result_id]
        result.reviewed_by = reviewed_by
        result.reviewed_date = datetime.now()
        result.notes += f"\n\nReview by {reviewed_by} ({approval_status}): {comments}"

        return True

    def get_statistics(self) -> Dict[str, Any]:
        """Get test execution statistics"""
        total_results = len(self.test_results)
        active_tests = len(self.active_tests)

        pass_fail_stats = self.get_pass_fail_statistics()

        total_measurements = sum(len(r.measurements) for r in self.test_results.values())
        total_anomalies = sum(len(r.anomalies_detected) for r in self.test_results.values())

        return {
            'total_completed_tests': total_results,
            'active_tests': active_tests,
            'pass_fail_statistics': pass_fail_stats,
            'total_measurements': total_measurements,
            'total_anomalies_detected': total_anomalies,
            'avg_measurements_per_test': total_measurements / total_results if total_results > 0 else 0
        }
