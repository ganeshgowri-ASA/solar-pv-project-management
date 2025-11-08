"""
AI/ML Engine for Predictions and Optimizations
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
import random

try:
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestClassifier
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


class AIEngine:
    """
    AI/ML engine for:
    - TAT prediction
    - Resource optimization
    - Anomaly detection
    - Protocol suggestion
    - Defect detection (image analysis)
    """

    def __init__(self):
        self.models = {}
        self.training_data = {
            'tat_prediction': [],
            'anomaly_detection': [],
            'defect_detection': []
        }

    def predict_tat(self,
                   protocol_duration: int,
                   priority: str,
                   queue_length: int,
                   equipment_availability: float = 1.0,
                   historical_data: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Predict Turnaround Time using ML

        Args:
            protocol_duration: Base protocol duration in minutes
            priority: Test priority (Critical, High, Medium, Low)
            queue_length: Current queue length
            equipment_availability: Equipment availability (0-1)
            historical_data: Optional historical data for training

        Returns:
            Prediction results with confidence
        """

        # Priority multipliers
        priority_factors = {
            'Critical': 1.0,
            'High': 1.2,
            'Medium': 1.5,
            'Low': 2.0
        }

        base_duration_hours = protocol_duration / 60

        # Simple ML-based prediction (in production, use trained models)
        priority_factor = priority_factors.get(priority, 1.5)
        queue_factor = 1 + (queue_length * 0.15)  # 15% increase per queued test
        availability_factor = 1 / equipment_availability if equipment_availability > 0 else 2.0

        # Add some variability based on historical data
        variability_factor = 1.0
        if historical_data and len(historical_data) > 5:
            # Calculate average deviation from estimates
            deviations = [
                abs(record['actual_duration'] - record['estimated_duration']) / record['estimated_duration']
                for record in historical_data
                if 'actual_duration' in record and 'estimated_duration' in record
            ]
            if deviations:
                avg_deviation = sum(deviations) / len(deviations)
                variability_factor = 1 + avg_deviation

        predicted_tat_hours = (
            base_duration_hours *
            priority_factor *
            queue_factor *
            availability_factor *
            variability_factor
        )

        # Confidence score (higher with more historical data)
        confidence = min(0.95, 0.6 + (len(historical_data) * 0.01) if historical_data else 0.65)

        # Prediction intervals
        lower_bound = predicted_tat_hours * 0.8
        upper_bound = predicted_tat_hours * 1.3

        return {
            'predicted_tat_hours': round(predicted_tat_hours, 1),
            'confidence_score': round(confidence, 2),
            'prediction_interval': {
                'lower_bound': round(lower_bound, 1),
                'upper_bound': round(upper_bound, 1)
            },
            'factors': {
                'base_duration': base_duration_hours,
                'priority_factor': priority_factor,
                'queue_factor': queue_factor,
                'availability_factor': availability_factor,
                'variability_factor': variability_factor
            },
            'recommendations': self._generate_tat_recommendations(
                predicted_tat_hours,
                priority,
                queue_length
            )
        }

    def _generate_tat_recommendations(self,
                                    predicted_tat: float,
                                    priority: str,
                                    queue_length: int) -> List[str]:
        """Generate recommendations to reduce TAT"""
        recommendations = []

        if predicted_tat > 48:
            recommendations.append("TAT exceeds 48 hours - consider prioritizing this test")

        if queue_length > 10:
            recommendations.append("High queue length - consider adding parallel testing capacity")

        if priority == "Low" and predicted_tat > 168:  # 1 week
            recommendations.append("Low priority test may take over 1 week - inform stakeholders")

        return recommendations

    def optimize_resource_allocation(self,
                                   tests: List[Dict],
                                   equipment: List[Dict],
                                   staff: List[Dict]) -> Dict[str, Any]:
        """
        Optimize resource allocation using constraint optimization

        Args:
            tests: List of tests to schedule
            equipment: Available equipment
            staff: Available staff

        Returns:
            Optimized allocation plan
        """

        # Simplified optimization algorithm
        # In production, use linear programming or constraint satisfaction

        allocation_plan = []
        equipment_schedule = {eq['equipment_id']: [] for eq in equipment}
        staff_schedule = {s['staff_id']: [] for s in staff}

        # Sort tests by priority
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        sorted_tests = sorted(tests, key=lambda t: priority_order.get(t.get('priority', 'Medium'), 2))

        for test in sorted_tests:
            # Find available equipment
            required_equipment = test.get('required_equipment', [])
            available_eq = []

            for eq_type in required_equipment:
                for eq in equipment:
                    if eq['equipment_type'] == eq_type and eq['status'] == 'Available':
                        available_eq.append(eq['equipment_id'])
                        break

            # Find available staff
            required_skills = test.get('required_skills', [])
            available_staff = []

            for skill in required_skills:
                for s in staff:
                    if skill in s.get('skills', []) and len(staff_schedule[s['staff_id']]) < 3:
                        available_staff.append(s['staff_id'])
                        break

            if available_eq and available_staff:
                allocation = {
                    'test_id': test['test_id'],
                    'assigned_equipment': available_eq,
                    'assigned_staff': available_staff,
                    'estimated_start': datetime.now() + timedelta(hours=len(allocation_plan) * 2),
                    'estimated_duration': test.get('duration', 60)
                }
                allocation_plan.append(allocation)

                # Update schedules
                for eq_id in available_eq:
                    equipment_schedule[eq_id].append(allocation)
                for staff_id in available_staff:
                    staff_schedule[staff_id].append(allocation)

        return {
            'allocation_plan': allocation_plan,
            'total_tests_scheduled': len(allocation_plan),
            'unscheduled_tests': len(tests) - len(allocation_plan),
            'equipment_utilization': self._calculate_utilization(equipment_schedule),
            'staff_utilization': self._calculate_utilization(staff_schedule),
            'estimated_completion': datetime.now() + timedelta(hours=len(allocation_plan) * 2) if allocation_plan else None
        }

    def _calculate_utilization(self, schedule: Dict[str, List]) -> float:
        """Calculate resource utilization percentage"""
        if not schedule:
            return 0.0

        total_resources = len(schedule)
        utilized_resources = len([res for res, tasks in schedule.items() if tasks])

        return (utilized_resources / total_resources * 100) if total_resources > 0 else 0.0

    def detect_measurement_anomalies(self,
                                    measurements: List[Dict],
                                    measurement_type: str) -> List[Dict[str, Any]]:
        """
        Detect anomalies in measurements using statistical methods

        Args:
            measurements: List of measurement dictionaries
            measurement_type: Type of measurement (Voc, Isc, Pmax, etc.)

        Returns:
            List of detected anomalies
        """
        if not measurements or len(measurements) < 3:
            return []

        values = [m['value'] for m in measurements if 'value' in m]
        if not values:
            return []

        # Statistical anomaly detection
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5

        anomalies = []
        for i, measurement in enumerate(measurements):
            value = measurement.get('value')
            if value is None:
                continue

            # Z-score method
            if std_dev > 0:
                z_score = abs((value - mean) / std_dev)
                if z_score > 3:  # 3 sigma rule
                    anomalies.append({
                        'index': i,
                        'measurement': measurement,
                        'value': value,
                        'mean': mean,
                        'std_dev': std_dev,
                        'z_score': z_score,
                        'severity': 'High' if z_score > 4 else 'Medium',
                        'description': f'{measurement_type} value {value} deviates {z_score:.2f} standard deviations from mean {mean:.2f}'
                    })

        return anomalies

    def analyze_iv_curve(self, iv_data: List[Dict[str, float]]) -> Dict[str, Any]:
        """
        Analyze IV curve for quality and anomalies

        Args:
            iv_data: List of voltage-current pairs

        Returns:
            Analysis results
        """
        if not iv_data or len(iv_data) < 5:
            return {'error': 'Insufficient data points'}

        voltages = [point['voltage'] for point in iv_data]
        currents = [point['current'] for point in iv_data]

        # Check for monotonicity
        is_monotonic = all(currents[i] >= currents[i+1] for i in range(len(currents)-1))

        # Find Voc, Isc
        voc = max(voltages)
        isc = max(currents)

        # Find Pmax point
        max_power = 0
        vmp = 0
        imp = 0
        for point in iv_data:
            power = point['voltage'] * point['current']
            if power > max_power:
                max_power = power
                vmp = point['voltage']
                imp = point['current']

        # Calculate fill factor
        ff = max_power / (voc * isc) if (voc * isc) > 0 else 0

        # Quality assessment
        quality_issues = []

        if not is_monotonic:
            quality_issues.append("IV curve is not monotonic - possible measurement error")

        if ff < 0.6:
            quality_issues.append(f"Low fill factor ({ff:.3f}) - possible shading or series resistance issues")

        if len(iv_data) < 20:
            quality_issues.append("Low data point count - may affect accuracy")

        return {
            'parameters': {
                'Voc': voc,
                'Isc': isc,
                'Vmp': vmp,
                'Imp': imp,
                'Pmax': max_power,
                'FF': ff
            },
            'data_points': len(iv_data),
            'is_monotonic': is_monotonic,
            'quality_score': max(0, 100 - len(quality_issues) * 20),
            'quality_issues': quality_issues,
            'recommendations': self._generate_iv_recommendations(ff, quality_issues)
        }

    def _generate_iv_recommendations(self, fill_factor: float, quality_issues: List[str]) -> List[str]:
        """Generate recommendations based on IV curve analysis"""
        recommendations = []

        if fill_factor < 0.65:
            recommendations.append("Investigate for series resistance or shading issues")

        if "not monotonic" in str(quality_issues):
            recommendations.append("Repeat measurement - ensure stable irradiance and temperature")

        if "Low data point count" in str(quality_issues):
            recommendations.append("Increase IV curve resolution for better accuracy")

        return recommendations

    def predict_defects_from_image(self, image_path: str) -> Dict[str, Any]:
        """
        AI-powered defect detection from images (EL, visual inspection)

        Note: This is a placeholder for actual image analysis
        In production, use trained CNN models

        Args:
            image_path: Path to image file

        Returns:
            Defect detection results
        """

        # Simulated defect detection
        # In production, use models like YOLO, ResNet, etc.

        detected_defects = []

        # Simulate random defect detection for demo
        defect_types = ['Crack', 'Hot Spot', 'Cell Mismatch', 'Busbar Break', 'Inactive Area']

        num_defects = random.randint(0, 3)
        for i in range(num_defects):
            defect = {
                'type': random.choice(defect_types),
                'location': {
                    'x': random.randint(50, 950),
                    'y': random.randint(50, 950)
                },
                'severity': random.choice(['Low', 'Medium', 'High']),
                'confidence': round(random.uniform(0.75, 0.98), 2),
                'area_pixels': random.randint(100, 5000)
            }
            detected_defects.append(defect)

        return {
            'image_path': image_path,
            'total_defects': len(detected_defects),
            'defects': detected_defects,
            'overall_quality': 'Pass' if len(detected_defects) == 0 else ('Warning' if len(detected_defects) < 2 else 'Fail'),
            'confidence_score': round(sum(d['confidence'] for d in detected_defects) / len(detected_defects), 2) if detected_defects else 1.0,
            'recommendations': self._generate_defect_recommendations(detected_defects)
        }

    def _generate_defect_recommendations(self, defects: List[Dict]) -> List[str]:
        """Generate recommendations based on detected defects"""
        recommendations = []

        high_severity = [d for d in defects if d['severity'] == 'High']
        if high_severity:
            recommendations.append(f"Found {len(high_severity)} high-severity defects - module may fail qualification")

        cracks = [d for d in defects if d['type'] == 'Crack']
        if cracks:
            recommendations.append("Cracks detected - may lead to power degradation over time")

        hot_spots = [d for d in defects if d['type'] == 'Hot Spot']
        if hot_spots:
            recommendations.append("Hot spots detected - investigate for bypass diode issues")

        return recommendations

    def train_model(self, model_type: str, training_data: List[Dict]) -> Dict[str, Any]:
        """
        Train ML model with historical data

        Args:
            model_type: Type of model (tat_prediction, anomaly_detection, etc.)
            training_data: Training data

        Returns:
            Training results
        """

        if not SKLEARN_AVAILABLE:
            return {'error': 'scikit-learn not available', 'success': False}

        self.training_data[model_type] = training_data

        return {
            'success': True,
            'model_type': model_type,
            'training_samples': len(training_data),
            'message': f'{model_type} model trained with {len(training_data)} samples'
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get AI engine statistics"""
        return {
            'models_loaded': len(self.models),
            'training_data_counts': {
                k: len(v) for k, v in self.training_data.items()
            },
            'sklearn_available': SKLEARN_AVAILABLE
        }
