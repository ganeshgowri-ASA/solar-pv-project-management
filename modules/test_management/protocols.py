"""
Test Protocol Library with AI-Powered Protocol Suggestions
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid
from .models import TestProtocol, TestStandard


class ProtocolLibrary:
    """Manages test protocol library with AI suggestions"""

    def __init__(self):
        self.protocols: Dict[str, TestProtocol] = {}
        self._initialize_standard_protocols()

    def _initialize_standard_protocols(self):
        """Initialize standard test protocols"""

        # IEC 61215 - Module Design Qualification
        self.add_protocol(TestProtocol(
            protocol_id="PROTO_IEC61215_001",
            name="Visual Inspection",
            standard=TestStandard.IEC_61215,
            version="4.0",
            description="Visual inspection of PV modules for defects, damage, and workmanship",
            steps=[
                {"step": 1, "description": "Inspect module surface for cracks, chips, or scratches", "duration": 5},
                {"step": 2, "description": "Check frame integrity and junction box", "duration": 3},
                {"step": 3, "description": "Verify labels and markings", "duration": 2},
                {"step": 4, "description": "Document findings with photos", "duration": 5}
            ],
            parameters={
                "lighting": "1000 lux minimum",
                "distance": "30-50 cm",
                "viewing_angle": "Multiple angles required"
            },
            acceptance_criteria={
                "max_defects": 0,
                "frame_damage": "None",
                "label_legibility": "100%"
            },
            estimated_duration=15,
            required_equipment=["Inspection Table", "LED Light"],
            required_staff_skills=["Visual Inspection", "IEC 61215"]
        ))

        self.add_protocol(TestProtocol(
            protocol_id="PROTO_IEC61215_002",
            name="Performance at STC",
            standard=TestStandard.IEC_61215,
            version="4.0",
            description="Electrical performance measurement at Standard Test Conditions",
            steps=[
                {"step": 1, "description": "Set up module in solar simulator", "duration": 10},
                {"step": 2, "description": "Allow temperature stabilization to 25±2°C", "duration": 15},
                {"step": 3, "description": "Perform IV curve measurement at 1000 W/m²", "duration": 5},
                {"step": 4, "description": "Record Voc, Isc, Vmp, Imp, Pmax, FF", "duration": 5},
                {"step": 5, "description": "Verify against nameplate ±3%", "duration": 5}
            ],
            parameters={
                "irradiance": "1000 W/m²",
                "temperature": "25°C",
                "spectrum": "AM 1.5G",
                "measurements": ["Voc", "Isc", "Vmp", "Imp", "Pmax", "FF"]
            },
            acceptance_criteria={
                "power_tolerance": "±3%",
                "min_fill_factor": 0.70,
                "iv_curve_quality": "Class A"
            },
            estimated_duration=40,
            required_equipment=["Solar Simulator", "IV Tracer", "Temperature Monitor"],
            required_staff_skills=["STC Testing", "IV Measurement", "IEC 61215"]
        ))

        self.add_protocol(TestProtocol(
            protocol_id="PROTO_IEC61215_003",
            name="Thermal Cycling Test",
            standard=TestStandard.IEC_61215,
            version="4.0",
            description="200 thermal cycles from -40°C to +85°C",
            steps=[
                {"step": 1, "description": "Baseline IV measurement at STC", "duration": 30},
                {"step": 2, "description": "Place module in thermal chamber", "duration": 10},
                {"step": 3, "description": "Execute 200 thermal cycles", "duration": 28800},
                {"step": 4, "description": "Final IV measurement at STC", "duration": 30},
                {"step": 5, "description": "Visual inspection", "duration": 15},
                {"step": 6, "description": "Calculate power degradation", "duration": 10}
            ],
            parameters={
                "min_temp": "-40°C",
                "max_temp": "+85°C",
                "cycles": 200,
                "ramp_rate": "100°C/hour max",
                "dwell_time": "10 minutes at each extreme"
            },
            acceptance_criteria={
                "max_power_loss": "5%",
                "no_visual_defects": True,
                "insulation_resistance": ">40 MΩ"
            },
            estimated_duration=29000,
            required_equipment=["Thermal Chamber", "Solar Simulator", "IV Tracer"],
            required_staff_skills=["Thermal Testing", "IEC 61215", "IV Measurement"]
        ))

        # IEC 61730 - Safety Qualification
        self.add_protocol(TestProtocol(
            protocol_id="PROTO_IEC61730_001",
            name="Wet Leakage Current Test",
            standard=TestStandard.IEC_61730,
            version="2.0",
            description="Measure leakage current in wet conditions",
            steps=[
                {"step": 1, "description": "Spray module with saline solution", "duration": 5},
                {"step": 2, "description": "Apply test voltage", "duration": 2},
                {"step": 3, "description": "Measure leakage current", "duration": 5},
                {"step": 4, "description": "Record and verify limits", "duration": 3}
            ],
            parameters={
                "test_voltage": "1000V + 2 × Voc",
                "solution": "1% NaCl",
                "duration": "60 seconds"
            },
            acceptance_criteria={
                "max_leakage_current": "1 mA per module"
            },
            estimated_duration=15,
            required_equipment=["HiPot Tester", "Spray System"],
            required_staff_skills=["Safety Testing", "IEC 61730", "High Voltage"]
        ))

        # IEC 61853 - PV Module Performance Testing
        self.add_protocol(TestProtocol(
            protocol_id="PROTO_IEC61853_001",
            name="IV Curve at Multiple Irradiances",
            standard=TestStandard.IEC_61853,
            version="3.0",
            description="Measure IV curves at multiple irradiance levels",
            steps=[
                {"step": 1, "description": "Set irradiance to 1100 W/m²", "duration": 5},
                {"step": 2, "description": "Measure IV curve", "duration": 5},
                {"step": 3, "description": "Set irradiance to 1000 W/m²", "duration": 5},
                {"step": 4, "description": "Measure IV curve", "duration": 5},
                {"step": 5, "description": "Set irradiance to 800 W/m²", "duration": 5},
                {"step": 6, "description": "Measure IV curve", "duration": 5},
                {"step": 7, "description": "Set irradiance to 600 W/m²", "duration": 5},
                {"step": 8, "description": "Measure IV curve", "duration": 5},
                {"step": 9, "description": "Set irradiance to 400 W/m²", "duration": 5},
                {"step": 10, "description": "Measure IV curve", "duration": 5},
                {"step": 11, "description": "Set irradiance to 200 W/m²", "duration": 5},
                {"step": 12, "description": "Measure IV curve", "duration": 5}
            ],
            parameters={
                "irradiances": [1100, 1000, 800, 600, 400, 200],
                "temperature": "25°C ± 2°C",
                "spectrum": "AM 1.5G"
            },
            acceptance_criteria={
                "linearity": "R² > 0.99",
                "repeatability": "±2%"
            },
            estimated_duration=60,
            required_equipment=["Solar Simulator", "IV Tracer", "Spectroradiometer"],
            required_staff_skills=["IEC 61853", "IV Measurement", "Solar Simulation"]
        ))

        # UL 1703 - Flat-Plate PV Modules
        self.add_protocol(TestProtocol(
            protocol_id="PROTO_UL1703_001",
            name="Impact Test",
            standard=TestStandard.UL_1703,
            version="2013",
            description="Ice ball impact test for hail resistance",
            steps=[
                {"step": 1, "description": "Prepare ice balls of specified diameter", "duration": 10},
                {"step": 2, "description": "Mount module at test angle", "duration": 5},
                {"step": 3, "description": "Drop ice balls from specified height", "duration": 15},
                {"step": 4, "description": "Visual inspection for damage", "duration": 10},
                {"step": 5, "description": "Electrical performance check", "duration": 20}
            ],
            parameters={
                "ice_ball_diameter": "25-76 mm",
                "drop_height": "1.3-2.5 m",
                "impact_points": 11,
                "test_angle": "45 degrees"
            },
            acceptance_criteria={
                "no_cracks": True,
                "no_electrical_failure": True,
                "max_power_loss": "5%"
            },
            estimated_duration=60,
            required_equipment=["Impact Tester", "Ice Ball Former", "Solar Simulator"],
            required_staff_skills=["UL 1703", "Impact Testing", "IV Measurement"]
        ))

        # IEEE 1547 - Interconnection Testing
        self.add_protocol(TestProtocol(
            protocol_id="PROTO_IEEE1547_001",
            name="Anti-Islanding Test",
            standard=TestStandard.IEEE_1547,
            version="2018",
            description="Verify inverter anti-islanding protection",
            steps=[
                {"step": 1, "description": "Connect inverter to grid simulator", "duration": 10},
                {"step": 2, "description": "Set resonant RLC load", "duration": 10},
                {"step": 3, "description": "Establish steady-state operation", "duration": 5},
                {"step": 4, "description": "Open utility disconnect", "duration": 1},
                {"step": 5, "description": "Measure time to cease energizing", "duration": 5},
                {"step": 6, "description": "Verify trip time < 2 seconds", "duration": 2}
            ],
            parameters={
                "quality_factor": "1.0 ± 0.05",
                "power_output": "Rated power",
                "trip_time_limit": "2.0 seconds"
            },
            acceptance_criteria={
                "max_trip_time": 2.0,
                "no_false_trips": True
            },
            estimated_duration=35,
            required_equipment=["Grid Simulator", "RLC Load Bank", "Power Analyzer"],
            required_staff_skills=["IEEE 1547", "Grid Testing", "Inverter Testing"]
        ))

        # ASTM Standards
        self.add_protocol(TestProtocol(
            protocol_id="PROTO_ASTM_E1036_001",
            name="Short-Circuit Current Temperature Coefficient",
            standard=TestStandard.ASTM_E1036,
            version="2019",
            description="Measure temperature coefficient of Isc",
            steps=[
                {"step": 1, "description": "Measure Isc at 25°C reference", "duration": 10},
                {"step": 2, "description": "Heat module to 50°C", "duration": 20},
                {"step": 3, "description": "Measure Isc at 50°C", "duration": 10},
                {"step": 4, "description": "Cool module to 15°C", "duration": 20},
                {"step": 5, "description": "Measure Isc at 15°C", "duration": 10},
                {"step": 6, "description": "Calculate temperature coefficient", "duration": 5}
            ],
            parameters={
                "temperatures": [15, 25, 50],
                "irradiance": "1000 W/m²",
                "stabilization_time": "10 minutes"
            },
            acceptance_criteria={
                "typical_range": "0.04% to 0.06% per °C",
                "linearity": "R² > 0.98"
            },
            estimated_duration=75,
            required_equipment=["Solar Simulator", "Temperature Chamber", "IV Tracer"],
            required_staff_skills=["ASTM Testing", "Temperature Coefficient", "IV Measurement"]
        ))

        self.add_protocol(TestProtocol(
            protocol_id="PROTO_ASTM_E2481_001",
            name="Electroluminescence Imaging",
            standard=TestStandard.ASTM_E2481,
            version="2021",
            description="EL imaging for defect detection in PV modules",
            steps=[
                {"step": 1, "description": "Mount module in dark room", "duration": 5},
                {"step": 2, "description": "Apply forward bias current", "duration": 2},
                {"step": 3, "description": "Capture EL images with camera", "duration": 10},
                {"step": 4, "description": "Analyze images for defects", "duration": 15},
                {"step": 5, "description": "Classify defect types and severity", "duration": 10}
            ],
            parameters={
                "forward_current": "Approximately Isc",
                "exposure_time": "1-10 seconds",
                "camera": "Si-CCD or InGaAs",
                "image_resolution": "Minimum 1 megapixel"
            },
            acceptance_criteria={
                "no_cracks": True,
                "inactive_area": "< 2%",
                "no_hot_spots": True
            },
            estimated_duration=42,
            required_equipment=["EL Imaging System", "DC Power Supply", "Analysis Software"],
            required_staff_skills=["EL Imaging", "Defect Analysis", "ASTM E2481"],
            tags=["imaging", "defect detection", "quality control"]
        ))

    def add_protocol(self, protocol: TestProtocol) -> str:
        """Add protocol to library"""
        self.protocols[protocol.protocol_id] = protocol
        return protocol.protocol_id

    def get_protocol(self, protocol_id: str) -> Optional[TestProtocol]:
        """Get protocol by ID"""
        return self.protocols.get(protocol_id)

    def get_all_protocols(self) -> List[TestProtocol]:
        """Get all protocols"""
        return list(self.protocols.values())

    def get_protocols_by_standard(self, standard: TestStandard) -> List[TestProtocol]:
        """Get protocols by standard"""
        return [p for p in self.protocols.values()
                if p.standard == standard and p.is_active]

    def search_protocols(self, query: str) -> List[TestProtocol]:
        """Search protocols by name or description"""
        query = query.lower()
        results = []
        for protocol in self.protocols.values():
            if (query in protocol.name.lower() or
                query in protocol.description.lower() or
                any(query in tag.lower() for tag in protocol.tags)):
                results.append(protocol)
        return results

    def suggest_protocols(self, sample_type: str, customer_requirements: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        AI-powered protocol suggestion based on sample type and requirements

        Args:
            sample_type: Type of sample (Module, Cell, String, etc.)
            customer_requirements: Optional customer-specific requirements

        Returns:
            List of suggested protocols with confidence scores
        """
        suggestions = []

        # Rule-based AI suggestions
        if sample_type.lower() in ['module', 'pv module', 'solar module']:
            # Standard module qualification tests
            suggested_ids = [
                "PROTO_IEC61215_001",  # Visual Inspection
                "PROTO_IEC61215_002",  # Performance at STC
                "PROTO_IEC61730_001",  # Wet Leakage Current
                "PROTO_ASTM_E2481_001" # EL Imaging
            ]
            confidence = 0.95

            # Add thermal cycling if reliability is required
            if customer_requirements and customer_requirements.get('reliability_test'):
                suggested_ids.append("PROTO_IEC61215_003")

            # Add impact test for outdoor applications
            if customer_requirements and customer_requirements.get('outdoor_use'):
                suggested_ids.append("PROTO_UL1703_001")

        elif sample_type.lower() in ['inverter', 'grid-tie inverter']:
            suggested_ids = ["PROTO_IEEE1547_001"]
            confidence = 0.90

        elif sample_type.lower() in ['cell', 'solar cell']:
            suggested_ids = [
                "PROTO_IEC61215_001",  # Visual Inspection
                "PROTO_IEC61853_001",  # IV at multiple irradiances
                "PROTO_ASTM_E1036_001" # Temperature coefficient
            ]
            confidence = 0.85
        else:
            # Default to basic tests
            suggested_ids = [
                "PROTO_IEC61215_001",
                "PROTO_IEC61215_002"
            ]
            confidence = 0.70

        # Build suggestion list
        for protocol_id in suggested_ids:
            protocol = self.get_protocol(protocol_id)
            if protocol:
                suggestions.append({
                    'protocol': protocol,
                    'confidence': confidence,
                    'reason': f"Recommended for {sample_type}"
                })

        return suggestions

    def create_custom_protocol(self,
                              name: str,
                              standard: TestStandard,
                              description: str,
                              steps: List[Dict],
                              parameters: Dict,
                              acceptance_criteria: Dict,
                              estimated_duration: int,
                              required_equipment: List[str],
                              required_staff_skills: List[str]) -> str:
        """Create custom test protocol"""
        protocol_id = f"PROTO_CUSTOM_{uuid.uuid4().hex[:8].upper()}"

        protocol = TestProtocol(
            protocol_id=protocol_id,
            name=name,
            standard=standard,
            version="1.0",
            description=description,
            steps=steps,
            parameters=parameters,
            acceptance_criteria=acceptance_criteria,
            estimated_duration=estimated_duration,
            required_equipment=required_equipment,
            required_staff_skills=required_staff_skills,
            tags=["custom"]
        )

        return self.add_protocol(protocol)

    def update_protocol(self, protocol_id: str, updates: Dict[str, Any]) -> bool:
        """Update protocol fields"""
        if protocol_id not in self.protocols:
            return False

        protocol = self.protocols[protocol_id]
        for key, value in updates.items():
            if hasattr(protocol, key):
                setattr(protocol, key, value)

        protocol.updated_date = datetime.now()
        return True

    def deactivate_protocol(self, protocol_id: str) -> bool:
        """Deactivate protocol (soft delete)"""
        if protocol_id in self.protocols:
            self.protocols[protocol_id].is_active = False
            return True
        return False

    def get_protocol_statistics(self) -> Dict[str, Any]:
        """Get statistics about protocol library"""
        total = len(self.protocols)
        active = len([p for p in self.protocols.values() if p.is_active])

        by_standard = {}
        for protocol in self.protocols.values():
            std = protocol.standard.value if isinstance(protocol.standard, TestStandard) else protocol.standard
            by_standard[std] = by_standard.get(std, 0) + 1

        return {
            'total_protocols': total,
            'active_protocols': active,
            'inactive_protocols': total - active,
            'by_standard': by_standard,
            'avg_duration_minutes': sum(p.estimated_duration for p in self.protocols.values()) / total if total > 0 else 0
        }
