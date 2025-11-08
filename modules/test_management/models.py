"""
Data models for Test Management AI System
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from enum import Enum
import hashlib
import json


class TestStandard(str, Enum):
    """Standard test protocols"""
    IEC_61215 = "IEC 61215"
    IEC_61730 = "IEC 61730"
    IEC_61853 = "IEC 61853"
    UL_1703 = "UL 1703"
    UL_61730 = "UL 61730"
    IEEE_1547 = "IEEE 1547"
    ASTM_E1036 = "ASTM E1036"
    ASTM_E2481 = "ASTM E2481"


class SampleStatus(str, Enum):
    """Sample status in workflow"""
    REGISTERED = "Registered"
    IN_QUEUE = "In Queue"
    IN_TESTING = "In Testing"
    ON_HOLD = "On Hold"
    COMPLETED = "Completed"
    FAILED = "Failed"
    ARCHIVED = "Archived"


class TestStatus(str, Enum):
    """Test execution status"""
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    PAUSED = "Paused"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"


class EquipmentStatus(str, Enum):
    """Equipment availability status"""
    AVAILABLE = "Available"
    IN_USE = "In Use"
    MAINTENANCE = "Maintenance"
    CALIBRATION_DUE = "Calibration Due"
    OUT_OF_SERVICE = "Out of Service"


class Priority(str, Enum):
    """Test priority levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


@dataclass
class TestProtocol:
    """Test protocol definition"""
    protocol_id: str
    name: str
    standard: TestStandard
    version: str
    description: str
    steps: List[Dict[str, Any]]
    parameters: Dict[str, Any]
    acceptance_criteria: Dict[str, Any]
    estimated_duration: int  # in minutes
    required_equipment: List[str]
    required_staff_skills: List[str]
    tags: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'protocol_id': self.protocol_id,
            'name': self.name,
            'standard': self.standard.value if isinstance(self.standard, Enum) else self.standard,
            'version': self.version,
            'description': self.description,
            'steps': self.steps,
            'parameters': self.parameters,
            'acceptance_criteria': self.acceptance_criteria,
            'estimated_duration': self.estimated_duration,
            'required_equipment': self.required_equipment,
            'required_staff_skills': self.required_staff_skills,
            'tags': self.tags,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime) else self.created_date,
            'updated_date': self.updated_date.isoformat() if isinstance(self.updated_date, datetime) else self.updated_date,
            'is_active': self.is_active
        }


@dataclass
class Sample:
    """Test sample"""
    sample_id: str
    sample_name: str
    sample_type: str  # Module, Cell, String, etc.
    manufacturer: str
    model: str
    batch_number: str
    serial_number: str
    quantity: int
    status: SampleStatus
    qr_code: Optional[str] = None
    barcode: Optional[str] = None
    registered_date: datetime = field(default_factory=datetime.now)
    registered_by: str = "system"
    current_location: str = "Receiving"
    customer: str = ""
    project_id: str = ""
    expiry_date: Optional[datetime] = None
    storage_conditions: Dict[str, Any] = field(default_factory=dict)
    photos: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'sample_id': self.sample_id,
            'sample_name': self.sample_name,
            'sample_type': self.sample_type,
            'manufacturer': self.manufacturer,
            'model': self.model,
            'batch_number': self.batch_number,
            'serial_number': self.serial_number,
            'quantity': self.quantity,
            'status': self.status.value if isinstance(self.status, Enum) else self.status,
            'qr_code': self.qr_code,
            'barcode': self.barcode,
            'registered_date': self.registered_date.isoformat() if isinstance(self.registered_date, datetime) else self.registered_date,
            'registered_by': self.registered_by,
            'current_location': self.current_location,
            'customer': self.customer,
            'project_id': self.project_id,
            'expiry_date': self.expiry_date.isoformat() if isinstance(self.expiry_date, datetime) else None,
            'storage_conditions': self.storage_conditions,
            'photos': self.photos,
            'metadata': self.metadata
        }


@dataclass
class ChainOfCustody:
    """Blockchain-style chain of custody record"""
    record_id: str
    sample_id: str
    timestamp: datetime
    event_type: str  # Received, Moved, Tested, Released
    from_location: str
    to_location: str
    handled_by: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    photos: List[str] = field(default_factory=list)
    notes: str = ""
    previous_hash: Optional[str] = None
    current_hash: Optional[str] = None

    def __post_init__(self):
        """Generate hash after initialization"""
        if self.current_hash is None:
            self.current_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of record"""
        record_data = {
            'record_id': self.record_id,
            'sample_id': self.sample_id,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            'event_type': self.event_type,
            'from_location': self.from_location,
            'to_location': self.to_location,
            'handled_by': self.handled_by,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'notes': self.notes,
            'previous_hash': self.previous_hash
        }
        record_string = json.dumps(record_data, sort_keys=True)
        return hashlib.sha256(record_string.encode()).hexdigest()

    def verify_hash(self) -> bool:
        """Verify integrity of record"""
        return self.current_hash == self.calculate_hash()

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'record_id': self.record_id,
            'sample_id': self.sample_id,
            'timestamp': self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
            'event_type': self.event_type,
            'from_location': self.from_location,
            'to_location': self.to_location,
            'handled_by': self.handled_by,
            'temperature': self.temperature,
            'humidity': self.humidity,
            'photos': self.photos,
            'notes': self.notes,
            'previous_hash': self.previous_hash,
            'current_hash': self.current_hash
        }


@dataclass
class TestSchedule:
    """Test schedule entry"""
    schedule_id: str
    sample_id: str
    protocol_id: str
    scheduled_start: datetime
    scheduled_end: datetime
    assigned_equipment: List[str]
    assigned_staff: List[str]
    priority: Priority
    status: TestStatus
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    estimated_tat: int = 0  # in hours
    predicted_tat: Optional[int] = None  # ML prediction
    dependencies: List[str] = field(default_factory=list)
    created_date: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    notes: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'schedule_id': self.schedule_id,
            'sample_id': self.sample_id,
            'protocol_id': self.protocol_id,
            'scheduled_start': self.scheduled_start.isoformat() if isinstance(self.scheduled_start, datetime) else self.scheduled_start,
            'scheduled_end': self.scheduled_end.isoformat() if isinstance(self.scheduled_end, datetime) else self.scheduled_end,
            'assigned_equipment': self.assigned_equipment,
            'assigned_staff': self.assigned_staff,
            'priority': self.priority.value if isinstance(self.priority, Enum) else self.priority,
            'status': self.status.value if isinstance(self.status, Enum) else self.status,
            'actual_start': self.actual_start.isoformat() if isinstance(self.actual_start, datetime) else None,
            'actual_end': self.actual_end.isoformat() if isinstance(self.actual_end, datetime) else None,
            'estimated_tat': self.estimated_tat,
            'predicted_tat': self.predicted_tat,
            'dependencies': self.dependencies,
            'created_date': self.created_date.isoformat() if isinstance(self.created_date, datetime) else self.created_date,
            'created_by': self.created_by,
            'notes': self.notes
        }


@dataclass
class TestResult:
    """Test execution result"""
    result_id: str
    schedule_id: str
    sample_id: str
    protocol_id: str
    test_data: Dict[str, Any]
    measurements: List[Dict[str, Any]]
    images: List[str] = field(default_factory=list)
    videos: List[str] = field(default_factory=list)
    pass_fail: Optional[str] = None
    anomalies_detected: List[str] = field(default_factory=list)
    validation_errors: List[str] = field(default_factory=list)
    performed_by: str = "system"
    performed_date: datetime = field(default_factory=datetime.now)
    reviewed_by: Optional[str] = None
    reviewed_date: Optional[datetime] = None
    notes: str = ""

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'result_id': self.result_id,
            'schedule_id': self.schedule_id,
            'sample_id': self.sample_id,
            'protocol_id': self.protocol_id,
            'test_data': self.test_data,
            'measurements': self.measurements,
            'images': self.images,
            'videos': self.videos,
            'pass_fail': self.pass_fail,
            'anomalies_detected': self.anomalies_detected,
            'validation_errors': self.validation_errors,
            'performed_by': self.performed_by,
            'performed_date': self.performed_date.isoformat() if isinstance(self.performed_date, datetime) else self.performed_date,
            'reviewed_by': self.reviewed_by,
            'reviewed_date': self.reviewed_date.isoformat() if isinstance(self.reviewed_date, datetime) else None,
            'notes': self.notes
        }


@dataclass
class Equipment:
    """Equipment/Instrument"""
    equipment_id: str
    name: str
    model: str
    manufacturer: str
    serial_number: str
    equipment_type: str  # Solar Simulator, EL Tester, IV Tracer, etc.
    status: EquipmentStatus
    location: str
    calibration_due_date: datetime
    last_calibration_date: datetime
    calibration_frequency_days: int = 90
    usage_hours: float = 0.0
    maintenance_schedule: List[Dict[str, Any]] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'equipment_id': self.equipment_id,
            'name': self.name,
            'model': self.model,
            'manufacturer': self.manufacturer,
            'serial_number': self.serial_number,
            'equipment_type': self.equipment_type,
            'status': self.status.value if isinstance(self.status, Enum) else self.status,
            'location': self.location,
            'calibration_due_date': self.calibration_due_date.isoformat() if isinstance(self.calibration_due_date, datetime) else self.calibration_due_date,
            'last_calibration_date': self.last_calibration_date.isoformat() if isinstance(self.last_calibration_date, datetime) else self.last_calibration_date,
            'calibration_frequency_days': self.calibration_frequency_days,
            'usage_hours': self.usage_hours,
            'maintenance_schedule': self.maintenance_schedule,
            'performance_metrics': self.performance_metrics,
            'metadata': self.metadata
        }


@dataclass
class Staff:
    """Staff member"""
    staff_id: str
    name: str
    role: str
    skills: List[str]
    certifications: List[Dict[str, Any]]
    availability: Dict[str, Any]  # Calendar availability
    current_assignments: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'staff_id': self.staff_id,
            'name': self.name,
            'role': self.role,
            'skills': self.skills,
            'certifications': self.certifications,
            'availability': self.availability,
            'current_assignments': self.current_assignments
        }
