"""
Data Ingestion and Validation Module
Supports Excel, CSV, equipment files (.ivc, JSON, XML), and image analysis
"""

from typing import List, Dict, Optional, Any, Tuple, TYPE_CHECKING
import io
import json
import xml.etree.ElementTree as ET
from datetime import datetime

if TYPE_CHECKING:
    import pandas as pd

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    pd = None


class DataIngestor:
    """Handles data import, validation, and normalization"""

    def __init__(self):
        self.validation_rules: Dict[str, Dict] = {}
        self._initialize_validation_rules()

    def _initialize_validation_rules(self):
        """Initialize standard validation rules for common measurements"""

        # PV Module measurements
        self.validation_rules['Voc'] = {
            'type': 'float',
            'min': 0,
            'max': 100,
            'unit': 'V',
            'description': 'Open Circuit Voltage'
        }

        self.validation_rules['Isc'] = {
            'type': 'float',
            'min': 0,
            'max': 20,
            'unit': 'A',
            'description': 'Short Circuit Current'
        }

        self.validation_rules['Vmp'] = {
            'type': 'float',
            'min': 0,
            'max': 100,
            'unit': 'V',
            'description': 'Voltage at Maximum Power'
        }

        self.validation_rules['Imp'] = {
            'type': 'float',
            'min': 0,
            'max': 20,
            'unit': 'A',
            'description': 'Current at Maximum Power'
        }

        self.validation_rules['Pmax'] = {
            'type': 'float',
            'min': 0,
            'max': 500,
            'unit': 'W',
            'description': 'Maximum Power'
        }

        self.validation_rules['FF'] = {
            'type': 'float',
            'min': 0.5,
            'max': 1.0,
            'unit': '',
            'description': 'Fill Factor'
        }

        self.validation_rules['Efficiency'] = {
            'type': 'float',
            'min': 0,
            'max': 30,
            'unit': '%',
            'description': 'Conversion Efficiency'
        }

        self.validation_rules['Temperature'] = {
            'type': 'float',
            'min': -50,
            'max': 100,
            'unit': '°C',
            'description': 'Temperature'
        }

        self.validation_rules['Irradiance'] = {
            'type': 'float',
            'min': 0,
            'max': 1500,
            'unit': 'W/m²',
            'description': 'Irradiance'
        }

    def import_from_excel(self, file_path: str, sheet_name: str = 0) -> Tuple[Any, List[str]]:
        """
        Import data from Excel file

        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name or index

        Returns:
            Tuple of (DataFrame, list of errors)
        """
        if not PANDAS_AVAILABLE:
            return None, ["pandas is not available"]

        errors = []

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Basic validation
            if df.empty:
                errors.append("Excel file is empty")

            return df, errors

        except Exception as e:
            errors.append(f"Error reading Excel file: {str(e)}")
            return None, errors

    def import_from_csv(self, file_path: str, delimiter: str = ',') -> Tuple[Any, List[str]]:
        """
        Import data from CSV file

        Args:
            file_path: Path to CSV file
            delimiter: CSV delimiter

        Returns:
            Tuple of (DataFrame, list of errors)
        """
        if not PANDAS_AVAILABLE:
            return None, ["pandas is not available"]

        errors = []

        try:
            df = pd.read_csv(file_path, delimiter=delimiter)

            if df.empty:
                errors.append("CSV file is empty")

            return df, errors

        except Exception as e:
            errors.append(f"Error reading CSV file: {str(e)}")
            return None, errors

    def import_ivc_file(self, file_content: str) -> Tuple[Dict[str, Any], List[str]]:
        """
        Import IV curve data from .ivc file

        Args:
            file_content: Content of .ivc file

        Returns:
            Tuple of (parsed data dict, list of errors)
        """
        errors = []
        data = {
            'metadata': {},
            'iv_curve': [],
            'parameters': {}
        }

        try:
            lines = file_content.split('\n')

            # Parse metadata (typically in header)
            in_data_section = False

            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('[DATA]') or line.startswith('Voltage'):
                    in_data_section = True
                    continue

                if not in_data_section:
                    # Parse metadata
                    if ':' in line:
                        key, value = line.split(':', 1)
                        data['metadata'][key.strip()] = value.strip()
                else:
                    # Parse IV data
                    parts = line.split()
                    if len(parts) >= 2:
                        try:
                            voltage = float(parts[0])
                            current = float(parts[1])
                            data['iv_curve'].append({
                                'voltage': voltage,
                                'current': current
                            })
                        except ValueError:
                            continue

            # Calculate parameters if IV curve exists
            if data['iv_curve']:
                data['parameters'] = self._calculate_iv_parameters(data['iv_curve'])

            return data, errors

        except Exception as e:
            errors.append(f"Error parsing IVC file: {str(e)}")
            return data, errors

    def import_json_file(self, file_content: str) -> Tuple[Dict[str, Any], List[str]]:
        """
        Import data from JSON file

        Args:
            file_content: JSON file content

        Returns:
            Tuple of (parsed data, list of errors)
        """
        errors = []

        try:
            data = json.loads(file_content)
            return data, errors

        except json.JSONDecodeError as e:
            errors.append(f"JSON parsing error: {str(e)}")
            return {}, errors

    def import_xml_file(self, file_content: str) -> Tuple[Dict[str, Any], List[str]]:
        """
        Import data from XML file

        Args:
            file_content: XML file content

        Returns:
            Tuple of (parsed data dict, list of errors)
        """
        errors = []
        data = {}

        try:
            root = ET.fromstring(file_content)

            def parse_element(element):
                """Recursively parse XML element"""
                result = {}

                # Add attributes
                if element.attrib:
                    result['@attributes'] = element.attrib

                # Add text content
                if element.text and element.text.strip():
                    result['@text'] = element.text.strip()

                # Add child elements
                for child in element:
                    child_data = parse_element(child)
                    if child.tag in result:
                        # Convert to list if multiple elements with same tag
                        if not isinstance(result[child.tag], list):
                            result[child.tag] = [result[child.tag]]
                        result[child.tag].append(child_data)
                    else:
                        result[child.tag] = child_data

                return result

            data = {root.tag: parse_element(root)}
            return data, errors

        except ET.ParseError as e:
            errors.append(f"XML parsing error: {str(e)}")
            return data, errors

    def _calculate_iv_parameters(self, iv_curve: List[Dict[str, float]]) -> Dict[str, float]:
        """Calculate IV curve parameters"""
        if not iv_curve:
            return {}

        voltages = [point['voltage'] for point in iv_curve]
        currents = [point['current'] for point in iv_curve]

        # Find Voc (voltage when current ~ 0)
        voc = max(voltages)

        # Find Isc (current when voltage ~ 0)
        isc = max(currents)

        # Find maximum power point
        max_power = 0
        vmp = 0
        imp = 0

        for point in iv_curve:
            power = point['voltage'] * point['current']
            if power > max_power:
                max_power = power
                vmp = point['voltage']
                imp = point['current']

        # Calculate fill factor
        ff = max_power / (voc * isc) if (voc * isc) > 0 else 0

        return {
            'Voc': voc,
            'Isc': isc,
            'Vmp': vmp,
            'Imp': imp,
            'Pmax': max_power,
            'FF': ff
        }

    def validate_measurement(self, measurement_name: str, value: Any) -> Dict[str, Any]:
        """
        Validate a single measurement against rules

        Args:
            measurement_name: Name of measurement
            value: Measurement value

        Returns:
            Validation result dictionary
        """
        result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'normalized_value': value
        }

        if measurement_name not in self.validation_rules:
            result['warnings'].append(f"No validation rules defined for {measurement_name}")
            return result

        rules = self.validation_rules[measurement_name]

        # Type validation
        expected_type = rules.get('type', 'float')
        try:
            if expected_type == 'float':
                normalized_value = float(value)
            elif expected_type == 'int':
                normalized_value = int(value)
            elif expected_type == 'str':
                normalized_value = str(value)
            else:
                normalized_value = value

            result['normalized_value'] = normalized_value

        except (ValueError, TypeError) as e:
            result['valid'] = False
            result['errors'].append(f"Type conversion error: expected {expected_type}, got {type(value).__name__}")
            return result

        # Range validation
        if 'min' in rules and normalized_value < rules['min']:
            result['valid'] = False
            result['errors'].append(
                f"{measurement_name} = {normalized_value} is below minimum {rules['min']} {rules.get('unit', '')}"
            )

        if 'max' in rules and normalized_value > rules['max']:
            result['valid'] = False
            result['errors'].append(
                f"{measurement_name} = {normalized_value} exceeds maximum {rules['max']} {rules.get('unit', '')}"
            )

        # Warning thresholds
        if 'warning_min' in rules and normalized_value < rules['warning_min']:
            result['warnings'].append(
                f"{measurement_name} = {normalized_value} is below recommended minimum {rules['warning_min']}"
            )

        if 'warning_max' in rules and normalized_value > rules['warning_max']:
            result['warnings'].append(
                f"{measurement_name} = {normalized_value} exceeds recommended maximum {rules['warning_max']}"
            )

        return result

    def validate_dataset(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate entire dataset

        Args:
            data: Dictionary of measurement names to values

        Returns:
            Validation summary
        """
        results = {
            'valid': True,
            'total_measurements': len(data),
            'validated_measurements': 0,
            'errors': [],
            'warnings': [],
            'details': {}
        }

        for measurement_name, value in data.items():
            validation = self.validate_measurement(measurement_name, value)
            results['details'][measurement_name] = validation

            if not validation['valid']:
                results['valid'] = False
                results['errors'].extend(validation['errors'])

            results['warnings'].extend(validation['warnings'])
            results['validated_measurements'] += 1

        return results

    def normalize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize data (convert units, standardize formats)

        Args:
            data: Raw data dictionary

        Returns:
            Normalized data dictionary
        """
        normalized = {}

        for key, value in data.items():
            validation = self.validate_measurement(key, value)
            normalized[key] = validation['normalized_value']

        return normalized

    def detect_data_anomalies(self, data: Dict[str, Any]) -> List[str]:
        """
        Detect anomalies in data using statistical methods

        Args:
            data: Data dictionary

        Returns:
            List of anomaly descriptions
        """
        anomalies = []

        # Check for physically impossible values
        if 'Voc' in data and 'Vmp' in data:
            if data['Vmp'] > data['Voc']:
                anomalies.append("Vmp cannot be greater than Voc")

        if 'Isc' in data and 'Imp' in data:
            if data['Imp'] > data['Isc']:
                anomalies.append("Imp cannot be greater than Isc")

        if 'Voc' in data and 'Isc' in data and 'Pmax' in data:
            theoretical_max = data['Voc'] * data['Isc']
            if data['Pmax'] > theoretical_max:
                anomalies.append(f"Pmax ({data['Pmax']}W) exceeds theoretical maximum ({theoretical_max:.2f}W)")

        if 'FF' in data:
            if data['FF'] > 1.0:
                anomalies.append("Fill Factor cannot exceed 1.0")
            if data['FF'] < 0.5:
                anomalies.append("Fill Factor is unusually low (< 0.5) - possible measurement error")

        if 'Efficiency' in data:
            if data['Efficiency'] > 30:
                anomalies.append("Efficiency > 30% is highly unusual for standard PV modules")

        return anomalies

    def suggest_corrections(self, data: Dict[str, Any], validation_result: Dict[str, Any]) -> List[str]:
        """
        Suggest corrections for invalid data

        Args:
            data: Original data
            validation_result: Validation result from validate_dataset

        Returns:
            List of correction suggestions
        """
        suggestions = []

        for measurement_name, details in validation_result['details'].items():
            if not details['valid']:
                rules = self.validation_rules.get(measurement_name, {})

                # Suggest clamping to range
                if 'min' in rules and data[measurement_name] < rules['min']:
                    suggestions.append(
                        f"Consider rechecking {measurement_name}. "
                        f"Expected minimum: {rules['min']} {rules.get('unit', '')}"
                    )

                if 'max' in rules and data[measurement_name] > rules['max']:
                    suggestions.append(
                        f"Consider rechecking {measurement_name}. "
                        f"Expected maximum: {rules['max']} {rules.get('unit', '')}"
                    )

        return suggestions

    def add_validation_rule(self, measurement_name: str, rule: Dict[str, Any]):
        """Add custom validation rule"""
        self.validation_rules[measurement_name] = rule

    def export_validation_report(self,
                                data: Dict[str, Any],
                                validation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Export comprehensive validation report

        Args:
            data: Original data
            validation_result: Validation result

        Returns:
            Comprehensive report dictionary
        """
        anomalies = self.detect_data_anomalies(data)
        suggestions = self.suggest_corrections(data, validation_result)

        return {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'validation_summary': {
                'valid': validation_result['valid'],
                'total_measurements': validation_result['total_measurements'],
                'validated_measurements': validation_result['validated_measurements'],
                'error_count': len(validation_result['errors']),
                'warning_count': len(validation_result['warnings'])
            },
            'errors': validation_result['errors'],
            'warnings': validation_result['warnings'],
            'anomalies': anomalies,
            'suggestions': suggestions,
            'details': validation_result['details']
        }
