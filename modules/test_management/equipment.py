"""
Equipment Integration and Monitoring System
"""

from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import uuid

from .models import Equipment, EquipmentStatus


class EquipmentManager:
    """Manages equipment, calibration, maintenance, and monitoring"""

    def __init__(self):
        self.equipment: Dict[str, Equipment] = {}
        self.usage_logs: Dict[str, List[Dict]] = {}  # equipment_id -> usage logs
        self.maintenance_history: Dict[str, List[Dict]] = {}  # equipment_id -> maintenance records
        self._initialize_standard_equipment()

    def _initialize_standard_equipment(self):
        """Initialize standard solar testing equipment"""

        # Solar Simulator
        self.add_equipment(Equipment(
            equipment_id="EQ_SOLAR_SIMULATOR_001",
            name="Class AAA Solar Simulator",
            model="SunSim 3000",
            manufacturer="PhotonTech",
            serial_number="SS3000-2023-001",
            equipment_type="Solar Simulator",
            status=EquipmentStatus.AVAILABLE,
            location="Test Lab 1",
            calibration_due_date=datetime.now() + timedelta(days=45),
            last_calibration_date=datetime.now() - timedelta(days=45),
            calibration_frequency_days=90,
            usage_hours=1250.5,
            performance_metrics={
                'spectral_match': 'Class A',
                'spatial_uniformity': 'Class A',
                'temporal_stability': 'Class A',
                'irradiance_range': '200-1200 W/m²'
            },
            metadata={'max_module_size': '2.0m x 1.2m'}
        ))

        # IV Tracer
        self.add_equipment(Equipment(
            equipment_id="EQ_IV_TRACER_001",
            name="High-Precision IV Tracer",
            model="IVMaster Pro",
            manufacturer="TestEquip Inc",
            serial_number="IVM-2023-042",
            equipment_type="IV Tracer",
            status=EquipmentStatus.AVAILABLE,
            location="Test Lab 1",
            calibration_due_date=datetime.now() + timedelta(days=60),
            last_calibration_date=datetime.now() - timedelta(days=30),
            calibration_frequency_days=90,
            usage_hours=850.3,
            performance_metrics={
                'voltage_accuracy': '±0.1%',
                'current_accuracy': '±0.1%',
                'max_voltage': '1500V',
                'max_current': '30A'
            }
        ))

        # EL Imaging System
        self.add_equipment(Equipment(
            equipment_id="EQ_EL_IMAGING_001",
            name="Electroluminescence Imaging System",
            model="EL-Vision 5000",
            manufacturer="ImageSolar",
            serial_number="ELV-2023-015",
            equipment_type="EL Imaging System",
            status=EquipmentStatus.AVAILABLE,
            location="Test Lab 2",
            calibration_due_date=datetime.now() + timedelta(days=75),
            last_calibration_date=datetime.now() - timedelta(days=15),
            calibration_frequency_days=90,
            usage_hours=420.0,
            performance_metrics={
                'camera_resolution': '16MP',
                'detection_sensitivity': 'High',
                'image_processing': 'AI-enhanced'
            }
        ))

        # Thermal Chamber
        self.add_equipment(Equipment(
            equipment_id="EQ_THERMAL_CHAMBER_001",
            name="Environmental Test Chamber",
            model="ThermoCycle 2000",
            manufacturer="ClimateTech",
            serial_number="TC2000-2022-008",
            equipment_type="Thermal Chamber",
            status=EquipmentStatus.AVAILABLE,
            location="Environmental Lab",
            calibration_due_date=datetime.now() + timedelta(days=30),
            last_calibration_date=datetime.now() - timedelta(days=60),
            calibration_frequency_days=90,
            usage_hours=2100.0,
            performance_metrics={
                'temp_range': '-40°C to +150°C',
                'humidity_range': '10% to 95% RH',
                'chamber_volume': '2000L',
                'uniformity': '±2°C'
            }
        ))

        # HiPot Tester
        self.add_equipment(Equipment(
            equipment_id="EQ_HIPOT_TESTER_001",
            name="High Potential Tester",
            model="SafeTest 5000",
            manufacturer="ElectroSafe",
            serial_number="ST5000-2023-003",
            equipment_type="HiPot Tester",
            status=EquipmentStatus.AVAILABLE,
            location="Safety Test Lab",
            calibration_due_date=datetime.now() + timedelta(days=20),
            last_calibration_date=datetime.now() - timedelta(days=70),
            calibration_frequency_days=90,
            usage_hours=315.5,
            performance_metrics={
                'max_ac_voltage': '5000V AC',
                'max_dc_voltage': '6000V DC',
                'leakage_current_range': '0.01μA to 50mA',
                'accuracy': '±1%'
            }
        ))

    def add_equipment(self, equipment: Equipment) -> str:
        """Add equipment to system"""
        self.equipment[equipment.equipment_id] = equipment
        self.usage_logs[equipment.equipment_id] = []
        self.maintenance_history[equipment.equipment_id] = []
        return equipment.equipment_id

    def get_equipment(self, equipment_id: str) -> Optional[Equipment]:
        """Get equipment by ID"""
        return self.equipment.get(equipment_id)

    def get_all_equipment(self) -> List[Equipment]:
        """Get all equipment"""
        return list(self.equipment.values())

    def get_equipment_by_status(self, status: EquipmentStatus) -> List[Equipment]:
        """Get equipment by status"""
        return [e for e in self.equipment.values() if e.status == status]

    def get_equipment_by_type(self, equipment_type: str) -> List[Equipment]:
        """Get equipment by type"""
        return [e for e in self.equipment.values() if e.equipment_type == equipment_type]

    def update_equipment_status(self, equipment_id: str, new_status: EquipmentStatus) -> bool:
        """Update equipment status"""
        if equipment_id not in self.equipment:
            return False

        self.equipment[equipment_id].status = new_status
        return True

    def log_equipment_usage(self,
                          equipment_id: str,
                          start_time: datetime,
                          end_time: datetime,
                          used_by: str,
                          purpose: str = "",
                          notes: str = "") -> bool:
        """
        Log equipment usage

        Args:
            equipment_id: Equipment identifier
            start_time: Usage start time
            end_time: Usage end time
            used_by: User/technician
            purpose: Purpose of usage
            notes: Additional notes

        Returns:
            Success status
        """
        if equipment_id not in self.equipment:
            return False

        duration_hours = (end_time - start_time).total_seconds() / 3600

        usage_log = {
            'log_id': f"USAGE_{uuid.uuid4().hex[:8].upper()}",
            'equipment_id': equipment_id,
            'start_time': start_time,
            'end_time': end_time,
            'duration_hours': duration_hours,
            'used_by': used_by,
            'purpose': purpose,
            'notes': notes
        }

        self.usage_logs[equipment_id].append(usage_log)

        # Update total usage hours
        self.equipment[equipment_id].usage_hours += duration_hours

        return True

    def schedule_maintenance(self,
                           equipment_id: str,
                           maintenance_type: str,
                           scheduled_date: datetime,
                           description: str = "",
                           estimated_duration_hours: float = 4.0) -> str:
        """
        Schedule maintenance for equipment

        Args:
            equipment_id: Equipment identifier
            maintenance_type: Type (Preventive, Corrective, Calibration)
            scheduled_date: Scheduled date
            description: Maintenance description
            estimated_duration_hours: Estimated duration

        Returns:
            Maintenance record ID
        """
        if equipment_id not in self.equipment:
            return None

        maintenance_id = f"MAINT_{uuid.uuid4().hex[:8].upper()}"

        maintenance_record = {
            'maintenance_id': maintenance_id,
            'equipment_id': equipment_id,
            'type': maintenance_type,
            'scheduled_date': scheduled_date,
            'description': description,
            'estimated_duration_hours': estimated_duration_hours,
            'status': 'Scheduled',
            'performed_by': None,
            'actual_start': None,
            'actual_end': None,
            'findings': '',
            'actions_taken': ''
        }

        self.maintenance_history[equipment_id].append(maintenance_record)

        return maintenance_id

    def complete_maintenance(self,
                           equipment_id: str,
                           maintenance_id: str,
                           performed_by: str,
                           findings: str = "",
                           actions_taken: str = "") -> bool:
        """
        Mark maintenance as completed

        Args:
            equipment_id: Equipment identifier
            maintenance_id: Maintenance record ID
            performed_by: Technician who performed maintenance
            findings: Maintenance findings
            actions_taken: Actions taken

        Returns:
            Success status
        """
        if equipment_id not in self.maintenance_history:
            return False

        for record in self.maintenance_history[equipment_id]:
            if record['maintenance_id'] == maintenance_id:
                record['status'] = 'Completed'
                record['performed_by'] = performed_by
                record['actual_end'] = datetime.now()
                record['findings'] = findings
                record['actions_taken'] = actions_taken

                # If it was a calibration, update calibration dates
                if record['type'] == 'Calibration':
                    equipment = self.equipment[equipment_id]
                    equipment.last_calibration_date = datetime.now()
                    equipment.calibration_due_date = datetime.now() + timedelta(
                        days=equipment.calibration_frequency_days
                    )

                return True

        return False

    def get_calibration_alerts(self, days_threshold: int = 30) -> List[Dict[str, Any]]:
        """
        Get equipment requiring calibration within threshold

        Args:
            days_threshold: Days before due date to alert

        Returns:
            List of calibration alerts
        """
        alerts = []
        threshold_date = datetime.now() + timedelta(days=days_threshold)

        for equipment in self.equipment.values():
            if equipment.calibration_due_date <= threshold_date:
                days_until_due = (equipment.calibration_due_date - datetime.now()).days

                alerts.append({
                    'equipment_id': equipment.equipment_id,
                    'equipment_name': equipment.name,
                    'calibration_due_date': equipment.calibration_due_date,
                    'days_until_due': days_until_due,
                    'status': 'OVERDUE' if days_until_due < 0 else 'DUE_SOON',
                    'last_calibration': equipment.last_calibration_date
                })

        return sorted(alerts, key=lambda x: x['days_until_due'])

    def get_equipment_performance(self, equipment_id: str) -> Dict[str, Any]:
        """
        Get equipment performance metrics

        Args:
            equipment_id: Equipment identifier

        Returns:
            Performance metrics dictionary
        """
        if equipment_id not in self.equipment:
            return {'error': 'Equipment not found'}

        equipment = self.equipment[equipment_id]
        usage_logs = self.usage_logs.get(equipment_id, [])
        maintenance_records = self.maintenance_history.get(equipment_id, [])

        # Calculate utilization
        total_usage_hours = equipment.usage_hours
        days_since_install = 365  # Assume 1 year for now
        available_hours = days_since_install * 10  # 10 hours/day working time
        utilization_rate = (total_usage_hours / available_hours * 100) if available_hours > 0 else 0

        # Count maintenance events
        preventive_maintenance_count = len([m for m in maintenance_records if m['type'] == 'Preventive'])
        corrective_maintenance_count = len([m for m in maintenance_records if m['type'] == 'Corrective'])

        return {
            'equipment_id': equipment_id,
            'name': equipment.name,
            'status': equipment.status.value if isinstance(equipment.status, EquipmentStatus) else equipment.status,
            'total_usage_hours': total_usage_hours,
            'utilization_rate_percent': utilization_rate,
            'total_usage_sessions': len(usage_logs),
            'calibration_status': 'Current' if equipment.calibration_due_date > datetime.now() else 'Overdue',
            'days_until_calibration': (equipment.calibration_due_date - datetime.now()).days,
            'preventive_maintenance_count': preventive_maintenance_count,
            'corrective_maintenance_count': corrective_maintenance_count,
            'performance_metrics': equipment.performance_metrics
        }

    def get_usage_statistics(self, equipment_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get usage statistics for specific period

        Args:
            equipment_id: Equipment identifier
            days: Number of days to analyze

        Returns:
            Usage statistics
        """
        if equipment_id not in self.usage_logs:
            return {'error': 'Equipment not found'}

        cutoff_date = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in self.usage_logs[equipment_id]
            if log['start_time'] >= cutoff_date
        ]

        total_usage_hours = sum(log['duration_hours'] for log in recent_logs)
        avg_session_duration = total_usage_hours / len(recent_logs) if recent_logs else 0

        return {
            'equipment_id': equipment_id,
            'period_days': days,
            'total_sessions': len(recent_logs),
            'total_usage_hours': total_usage_hours,
            'avg_session_duration_hours': avg_session_duration,
            'avg_daily_usage_hours': total_usage_hours / days
        }

    def get_availability_forecast(self,
                                 equipment_id: str,
                                 start_date: datetime,
                                 end_date: datetime) -> Dict[str, Any]:
        """
        Forecast equipment availability

        Args:
            equipment_id: Equipment identifier
            start_date: Forecast start date
            end_date: Forecast end date

        Returns:
            Availability forecast
        """
        if equipment_id not in self.equipment:
            return {'error': 'Equipment not found'}

        equipment = self.equipment[equipment_id]

        # Check if calibration due in period
        calibration_needed = False
        if start_date <= equipment.calibration_due_date <= end_date:
            calibration_needed = True

        # Check scheduled maintenance
        scheduled_maintenance = [
            m for m in self.maintenance_history.get(equipment_id, [])
            if m['status'] == 'Scheduled' and start_date <= m['scheduled_date'] <= end_date
        ]

        # Calculate availability percentage
        total_days = (end_date - start_date).days
        unavailable_days = 0

        if calibration_needed:
            unavailable_days += 1  # Assume 1 day for calibration

        for maint in scheduled_maintenance:
            unavailable_days += maint['estimated_duration_hours'] / 10  # Convert to days

        availability_percent = ((total_days - unavailable_days) / total_days * 100) if total_days > 0 else 0

        return {
            'equipment_id': equipment_id,
            'period': {
                'start': start_date,
                'end': end_date,
                'total_days': total_days
            },
            'availability_percent': availability_percent,
            'unavailable_days': unavailable_days,
            'calibration_needed': calibration_needed,
            'scheduled_maintenance_count': len(scheduled_maintenance),
            'current_status': equipment.status.value if isinstance(equipment.status, EquipmentStatus) else equipment.status
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get overall equipment statistics"""
        total = len(self.equipment)

        by_status = {}
        for status in EquipmentStatus:
            count = len(self.get_equipment_by_status(status))
            by_status[status.value] = count

        calibration_alerts = self.get_calibration_alerts(30)

        total_usage_hours = sum(eq.usage_hours for eq in self.equipment.values())

        return {
            'total_equipment': total,
            'by_status': by_status,
            'total_usage_hours': total_usage_hours,
            'calibration_alerts': len(calibration_alerts),
            'overdue_calibrations': len([a for a in calibration_alerts if a['status'] == 'OVERDUE'])
        }
