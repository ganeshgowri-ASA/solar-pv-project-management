"""
FastAPI Backend for Intelligent Test Management AI System

This module provides RESTful API endpoints for:
- Protocol management
- Sample tracking
- Test scheduling
- Test execution
- Data ingestion
- Equipment management
- AI/ML services

API Documentation available at: /docs (Swagger UI)
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from modules.test_management.protocols import ProtocolLibrary
from modules.test_management.sample_tracking import SampleTracker
from modules.test_management.scheduling import AIScheduler
from modules.test_management.test_execution import TestExecutor
from modules.test_management.data_ingestion import DataIngestor
from modules.test_management.equipment import EquipmentManager
from modules.test_management.ai_engine import AIEngine
from modules.test_management.models import (
    TestStandard, SampleStatus, TestStatus, EquipmentStatus, Priority
)

# Initialize FastAPI app
app = FastAPI(
    title="Solar PV Test Management API",
    description="Intelligent Test Management System for Solar PV Testing Labs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for GenSpark/Snowflake integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize system components
protocol_library = ProtocolLibrary()
sample_tracker = SampleTracker()
ai_scheduler = AIScheduler()
test_executor = TestExecutor()
data_ingestor = DataIngestor()
equipment_manager = EquipmentManager()
ai_engine = AIEngine()


# ===================== Pydantic Models for API =====================

class SampleCreate(BaseModel):
    sample_name: str
    sample_type: str
    manufacturer: str
    model: str
    batch_number: str
    serial_number: str
    quantity: int = 1
    customer: str = ""
    project_id: str = ""
    registered_by: str = "api_user"
    storage_conditions: Optional[Dict] = None
    metadata: Optional[Dict] = None


class SampleMove(BaseModel):
    to_location: str
    handled_by: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    notes: str = ""


class ScheduleCreate(BaseModel):
    sample_id: str
    protocol_id: str
    priority: str = "Medium"
    requested_date: Optional[str] = None
    created_by: str = "api_user"


class MeasurementRecord(BaseModel):
    measurement_name: str
    value: Any
    unit: str = ""
    notes: str = ""


class TestReview(BaseModel):
    reviewed_by: str
    approval_status: str
    comments: str = ""


# ===================== Root & Health Check =====================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Solar PV Test Management API",
        "version": "1.0.0",
        "documentation": "/docs",
        "module_id": "TEST_MANAGEMENT_AI_SESSION2"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "protocol_library": len(protocol_library.protocols),
            "samples": len(sample_tracker.samples),
            "schedules": len(ai_scheduler.schedules),
            "equipment": len(equipment_manager.equipment)
        }
    }


# ===================== Protocol Management =====================

@app.get("/api/protocols")
async def get_all_protocols():
    """Get all test protocols"""
    protocols = protocol_library.get_all_protocols()
    return {
        "total": len(protocols),
        "protocols": [p.to_dict() for p in protocols]
    }


@app.get("/api/protocols/{protocol_id}")
async def get_protocol(protocol_id: str):
    """Get specific protocol by ID"""
    protocol = protocol_library.get_protocol(protocol_id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")
    return protocol.to_dict()


@app.get("/api/protocols/standard/{standard}")
async def get_protocols_by_standard(standard: str):
    """Get protocols by standard"""
    try:
        test_standard = TestStandard(standard)
        protocols = protocol_library.get_protocols_by_standard(test_standard)
        return {
            "standard": standard,
            "total": len(protocols),
            "protocols": [p.to_dict() for p in protocols]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid standard: {standard}")


@app.get("/api/protocols/search/{query}")
async def search_protocols(query: str):
    """Search protocols by name or description"""
    protocols = protocol_library.search_protocols(query)
    return {
        "query": query,
        "results": len(protocols),
        "protocols": [p.to_dict() for p in protocols]
    }


@app.post("/api/protocols/suggest")
async def suggest_protocols(sample_type: str, customer_requirements: Optional[Dict] = None):
    """AI-powered protocol suggestion"""
    suggestions = protocol_library.suggest_protocols(sample_type, customer_requirements)
    return {
        "sample_type": sample_type,
        "suggestions": [
            {
                "protocol": s['protocol'].to_dict(),
                "confidence": s['confidence'],
                "reason": s['reason']
            } for s in suggestions
        ]
    }


@app.get("/api/protocols/statistics")
async def get_protocol_statistics():
    """Get protocol library statistics"""
    return protocol_library.get_protocol_statistics()


# ===================== Sample Tracking =====================

@app.post("/api/samples")
async def register_sample(sample: SampleCreate):
    """Register new sample"""
    new_sample = sample_tracker.register_sample(
        sample_name=sample.sample_name,
        sample_type=sample.sample_type,
        manufacturer=sample.manufacturer,
        model=sample.model,
        batch_number=sample.batch_number,
        serial_number=sample.serial_number,
        quantity=sample.quantity,
        customer=sample.customer,
        project_id=sample.project_id,
        registered_by=sample.registered_by,
        storage_conditions=sample.storage_conditions,
        metadata=sample.metadata
    )
    return new_sample.to_dict()


@app.get("/api/samples")
async def get_all_samples():
    """Get all samples"""
    samples = sample_tracker.get_all_samples()
    return {
        "total": len(samples),
        "samples": [s.to_dict() for s in samples]
    }


@app.get("/api/samples/{sample_id}")
async def get_sample(sample_id: str):
    """Get specific sample by ID"""
    sample = sample_tracker.get_sample(sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")
    return sample.to_dict()


@app.get("/api/samples/status/{status}")
async def get_samples_by_status(status: str):
    """Get samples by status"""
    try:
        sample_status = SampleStatus(status)
        samples = sample_tracker.get_samples_by_status(sample_status)
        return {
            "status": status,
            "total": len(samples),
            "samples": [s.to_dict() for s in samples]
        }
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid status: {status}")


@app.post("/api/samples/{sample_id}/move")
async def move_sample(sample_id: str, move: SampleMove):
    """Move sample to new location"""
    success = sample_tracker.move_sample(
        sample_id=sample_id,
        to_location=move.to_location,
        handled_by=move.handled_by,
        temperature=move.temperature,
        humidity=move.humidity,
        notes=move.notes
    )
    if not success:
        raise HTTPException(status_code=404, detail="Sample not found")
    return {"success": True, "message": f"Sample moved to {move.to_location}"}


@app.get("/api/samples/{sample_id}/chain-of-custody")
async def get_chain_of_custody(sample_id: str):
    """Get chain of custody for sample"""
    chain = sample_tracker.get_chain_of_custody(sample_id)
    integrity = sample_tracker.verify_chain_integrity(sample_id)

    return {
        "sample_id": sample_id,
        "total_records": len(chain),
        "chain": [c.to_dict() for c in chain],
        "integrity_check": integrity
    }


@app.get("/api/samples/{sample_id}/history")
async def get_sample_history(sample_id: str):
    """Get complete sample history"""
    history = sample_tracker.get_sample_history(sample_id)
    if 'error' in history:
        raise HTTPException(status_code=404, detail=history['error'])
    return history


@app.get("/api/samples/search/{query}")
async def search_samples(query: str):
    """Search samples"""
    results = sample_tracker.search_samples(query)
    return {
        "query": query,
        "results": len(results),
        "samples": [s.to_dict() for s in results]
    }


@app.get("/api/samples/statistics")
async def get_sample_statistics():
    """Get sample tracking statistics"""
    return sample_tracker.get_statistics()


# ===================== Test Scheduling =====================

@app.post("/api/schedule")
async def schedule_test(schedule_data: ScheduleCreate):
    """Schedule a new test"""
    # Get sample and protocol
    sample = sample_tracker.get_sample(schedule_data.sample_id)
    if not sample:
        raise HTTPException(status_code=404, detail="Sample not found")

    protocol = protocol_library.get_protocol(schedule_data.protocol_id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")

    # Parse requested date if provided
    requested_date = None
    if schedule_data.requested_date:
        try:
            requested_date = datetime.fromisoformat(schedule_data.requested_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format")

    # Parse priority
    try:
        priority = Priority(schedule_data.priority)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid priority: {schedule_data.priority}")

    # Schedule test
    schedule, conflicts = ai_scheduler.schedule_test(
        sample=sample,
        protocol=protocol,
        priority=priority,
        requested_date=requested_date,
        created_by=schedule_data.created_by
    )

    return {
        "schedule": schedule.to_dict(),
        "conflicts": [
            {
                "type": c.conflict_type,
                "resource_id": c.resource_id,
                "severity": c.severity
            } for c in conflicts
        ]
    }


@app.get("/api/schedule")
async def get_all_schedules():
    """Get all schedules"""
    schedules = ai_scheduler.get_all_schedules()
    return {
        "total": len(schedules),
        "schedules": [s.to_dict() for s in schedules]
    }


@app.get("/api/schedule/{schedule_id}")
async def get_schedule(schedule_id: str):
    """Get specific schedule"""
    schedule = ai_scheduler.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule.to_dict()


@app.get("/api/schedule/queue/status")
async def get_queue_status():
    """Get current queue status"""
    return ai_scheduler.get_queue_status()


@app.post("/api/schedule/{schedule_id}/start")
async def start_test(schedule_id: str):
    """Start scheduled test"""
    success = ai_scheduler.start_test(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"success": True, "message": "Test started"}


@app.post("/api/schedule/{schedule_id}/complete")
async def complete_test(schedule_id: str):
    """Mark test as completed"""
    success = ai_scheduler.complete_test(schedule_id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"success": True, "message": "Test completed"}


@app.get("/api/schedule/statistics")
async def get_schedule_statistics():
    """Get scheduling statistics"""
    return ai_scheduler.get_statistics()


# ===================== Test Execution =====================

@app.post("/api/execution/start/{schedule_id}")
async def start_test_execution(schedule_id: str, performed_by: str):
    """Start test execution"""
    schedule = ai_scheduler.get_schedule(schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    protocol = protocol_library.get_protocol(schedule.protocol_id)
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")

    result_id = test_executor.start_test_execution(schedule, protocol, performed_by)
    return {"result_id": result_id, "message": "Test execution started"}


@app.post("/api/execution/{result_id}/measurement")
async def record_measurement(result_id: str, measurement: MeasurementRecord):
    """Record measurement during test"""
    success = test_executor.record_measurement(
        result_id=result_id,
        measurement_name=measurement.measurement_name,
        value=measurement.value,
        unit=measurement.unit,
        notes=measurement.notes
    )
    if not success:
        raise HTTPException(status_code=404, detail="Test result not found")
    return {"success": True, "message": "Measurement recorded"}


@app.post("/api/execution/{result_id}/complete")
async def complete_test_execution(result_id: str, notes: str = ""):
    """Complete test execution"""
    active_test = test_executor.get_active_test(result_id)
    if not active_test:
        raise HTTPException(status_code=404, detail="Active test not found")

    protocol = protocol_library.get_protocol(active_test['protocol_id'])
    if not protocol:
        raise HTTPException(status_code=404, detail="Protocol not found")

    try:
        result = test_executor.complete_test_execution(result_id, protocol, notes)
        return result.to_dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/execution/{result_id}")
async def get_test_result(result_id: str):
    """Get test result"""
    result = test_executor.get_test_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Test result not found")
    return result.to_dict()


@app.get("/api/execution/statistics")
async def get_execution_statistics():
    """Get test execution statistics"""
    return test_executor.get_statistics()


# ===================== Data Ingestion =====================

@app.post("/api/data/validate")
async def validate_data(data: Dict[str, Any]):
    """Validate measurement data"""
    validation_result = data_ingestor.validate_dataset(data)
    return validation_result


@app.post("/api/data/import/ivc")
async def import_ivc_file(file: UploadFile = File(...)):
    """Import IV curve data from .ivc file"""
    content = await file.read()
    content_str = content.decode('utf-8')

    data, errors = data_ingestor.import_ivc_file(content_str)

    if errors:
        return {"success": False, "errors": errors, "data": data}
    return {"success": True, "data": data}


@app.post("/api/data/import/json")
async def import_json_file(file: UploadFile = File(...)):
    """Import data from JSON file"""
    content = await file.read()
    content_str = content.decode('utf-8')

    data, errors = data_ingestor.import_json_file(content_str)

    if errors:
        return {"success": False, "errors": errors, "data": data}
    return {"success": True, "data": data}


# ===================== Equipment Management =====================

@app.get("/api/equipment")
async def get_all_equipment():
    """Get all equipment"""
    equipment = equipment_manager.get_all_equipment()
    return {
        "total": len(equipment),
        "equipment": [e.to_dict() for e in equipment]
    }


@app.get("/api/equipment/{equipment_id}")
async def get_equipment(equipment_id: str):
    """Get specific equipment"""
    equipment = equipment_manager.get_equipment(equipment_id)
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment.to_dict()


@app.get("/api/equipment/{equipment_id}/performance")
async def get_equipment_performance(equipment_id: str):
    """Get equipment performance metrics"""
    performance = equipment_manager.get_equipment_performance(equipment_id)
    if 'error' in performance:
        raise HTTPException(status_code=404, detail=performance['error'])
    return performance


@app.get("/api/equipment/calibration/alerts")
async def get_calibration_alerts(days: int = 30):
    """Get calibration alerts"""
    alerts = equipment_manager.get_calibration_alerts(days)
    return {
        "threshold_days": days,
        "total_alerts": len(alerts),
        "alerts": alerts
    }


@app.get("/api/equipment/statistics")
async def get_equipment_statistics():
    """Get equipment statistics"""
    return equipment_manager.get_statistics()


# ===================== AI/ML Services =====================

@app.post("/api/ai/predict-tat")
async def predict_tat(
    protocol_duration: int,
    priority: str,
    queue_length: int,
    equipment_availability: float = 1.0
):
    """Predict turnaround time"""
    prediction = ai_engine.predict_tat(
        protocol_duration=protocol_duration,
        priority=priority,
        queue_length=queue_length,
        equipment_availability=equipment_availability
    )
    return prediction


@app.post("/api/ai/detect-anomalies")
async def detect_anomalies(measurements: List[Dict], measurement_type: str):
    """Detect measurement anomalies"""
    anomalies = ai_engine.detect_measurement_anomalies(measurements, measurement_type)
    return {
        "measurement_type": measurement_type,
        "total_measurements": len(measurements),
        "anomalies_detected": len(anomalies),
        "anomalies": anomalies
    }


@app.post("/api/ai/analyze-iv-curve")
async def analyze_iv_curve(iv_data: List[Dict[str, float]]):
    """Analyze IV curve"""
    analysis = ai_engine.analyze_iv_curve(iv_data)
    return analysis


@app.get("/api/ai/statistics")
async def get_ai_statistics():
    """Get AI engine statistics"""
    return ai_engine.get_statistics()


# ===================== System Statistics =====================

@app.get("/api/statistics/overview")
async def get_system_overview():
    """Get complete system overview"""
    return {
        "timestamp": datetime.now().isoformat(),
        "protocols": protocol_library.get_protocol_statistics(),
        "samples": sample_tracker.get_statistics(),
        "schedules": ai_scheduler.get_statistics(),
        "test_execution": test_executor.get_statistics(),
        "equipment": equipment_manager.get_statistics(),
        "ai_engine": ai_engine.get_statistics()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
