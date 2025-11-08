"""
Advanced Sample Tracking with QR/Barcode and Blockchain Chain of Custody
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid
import io
import base64
try:
    import qrcode
    import segno
    from barcode import EAN13, Code128
    from barcode.writer import ImageWriter
    BARCODE_AVAILABLE = True
except ImportError:
    BARCODE_AVAILABLE = False

from .models import Sample, SampleStatus, ChainOfCustody


class SampleTracker:
    """Manages sample tracking with QR codes and blockchain audit trail"""

    def __init__(self):
        self.samples: Dict[str, Sample] = {}
        self.chain_of_custody: Dict[str, List[ChainOfCustody]] = {}  # sample_id -> list of custody records

    def register_sample(self,
                       sample_name: str,
                       sample_type: str,
                       manufacturer: str,
                       model: str,
                       batch_number: str,
                       serial_number: str,
                       quantity: int = 1,
                       customer: str = "",
                       project_id: str = "",
                       registered_by: str = "system",
                       storage_conditions: Optional[Dict] = None,
                       metadata: Optional[Dict] = None) -> Sample:
        """
        Register new sample in system

        Args:
            sample_name: Name/identifier for the sample
            sample_type: Type (Module, Cell, String, etc.)
            manufacturer: Manufacturer name
            model: Model number
            batch_number: Batch/lot number
            serial_number: Serial number
            quantity: Number of samples
            customer: Customer name
            project_id: Associated project ID
            registered_by: Who registered the sample
            storage_conditions: Storage requirements
            metadata: Additional metadata

        Returns:
            Created Sample object
        """
        sample_id = f"SAMPLE_{uuid.uuid4().hex[:8].upper()}"

        # Generate QR code
        qr_data = {
            'sample_id': sample_id,
            'type': sample_type,
            'manufacturer': manufacturer,
            'model': model,
            'serial': serial_number
        }
        qr_code = self._generate_qr_code(str(qr_data))

        # Generate barcode (using sample_id)
        barcode = self._generate_barcode(sample_id)

        sample = Sample(
            sample_id=sample_id,
            sample_name=sample_name,
            sample_type=sample_type,
            manufacturer=manufacturer,
            model=model,
            batch_number=batch_number,
            serial_number=serial_number,
            quantity=quantity,
            status=SampleStatus.REGISTERED,
            qr_code=qr_code,
            barcode=barcode,
            registered_date=datetime.now(),
            registered_by=registered_by,
            current_location="Receiving",
            customer=customer,
            project_id=project_id,
            storage_conditions=storage_conditions or {},
            metadata=metadata or {}
        )

        self.samples[sample_id] = sample

        # Create initial chain of custody record
        self._add_custody_record(
            sample_id=sample_id,
            event_type="Registered",
            from_location="",
            to_location="Receiving",
            handled_by=registered_by,
            notes=f"Sample registered: {sample_name}"
        )

        return sample

    def _generate_qr_code(self, data: str) -> str:
        """Generate QR code as base64 string"""
        if not BARCODE_AVAILABLE:
            return f"QR_CODE_PLACEHOLDER_{data[:20]}"

        try:
            # Using segno for QR code generation
            qr = segno.make(data, micro=False)
            buffer = io.BytesIO()
            qr.save(buffer, kind='png', scale=5)
            buffer.seek(0)
            qr_base64 = base64.b64encode(buffer.read()).decode()
            return qr_base64
        except Exception as e:
            print(f"QR code generation error: {e}")
            return f"QR_CODE_PLACEHOLDER_{data[:20]}"

    def _generate_barcode(self, code: str) -> str:
        """Generate barcode as base64 string"""
        if not BARCODE_AVAILABLE:
            return f"BARCODE_PLACEHOLDER_{code}"

        try:
            # Use Code128 for alphanumeric support
            barcode_class = Code128
            buffer = io.BytesIO()
            barcode_instance = barcode_class(code, writer=ImageWriter())
            barcode_instance.write(buffer)
            buffer.seek(0)
            barcode_base64 = base64.b64encode(buffer.read()).decode()
            return barcode_base64
        except Exception as e:
            print(f"Barcode generation error: {e}")
            return f"BARCODE_PLACEHOLDER_{code}"

    def _add_custody_record(self,
                           sample_id: str,
                           event_type: str,
                           from_location: str,
                           to_location: str,
                           handled_by: str,
                           temperature: Optional[float] = None,
                           humidity: Optional[float] = None,
                           photos: Optional[List[str]] = None,
                           notes: str = "") -> ChainOfCustody:
        """Add chain of custody record (blockchain-style)"""

        # Get previous record's hash
        previous_hash = None
        if sample_id in self.chain_of_custody and self.chain_of_custody[sample_id]:
            previous_hash = self.chain_of_custody[sample_id][-1].current_hash

        record_id = f"COC_{uuid.uuid4().hex[:12].upper()}"

        custody_record = ChainOfCustody(
            record_id=record_id,
            sample_id=sample_id,
            timestamp=datetime.now(),
            event_type=event_type,
            from_location=from_location,
            to_location=to_location,
            handled_by=handled_by,
            temperature=temperature,
            humidity=humidity,
            photos=photos or [],
            notes=notes,
            previous_hash=previous_hash
        )

        # Add to chain
        if sample_id not in self.chain_of_custody:
            self.chain_of_custody[sample_id] = []
        self.chain_of_custody[sample_id].append(custody_record)

        return custody_record

    def move_sample(self,
                   sample_id: str,
                   to_location: str,
                   handled_by: str,
                   temperature: Optional[float] = None,
                   humidity: Optional[float] = None,
                   photos: Optional[List[str]] = None,
                   notes: str = "") -> bool:
        """
        Move sample to new location and record in chain of custody

        Args:
            sample_id: Sample identifier
            to_location: Destination location
            handled_by: Person handling the move
            temperature: Optional temperature reading
            humidity: Optional humidity reading
            photos: Optional photo documentation
            notes: Additional notes

        Returns:
            Success status
        """
        if sample_id not in self.samples:
            return False

        sample = self.samples[sample_id]
        from_location = sample.current_location

        # Update sample location
        sample.current_location = to_location

        # Add custody record
        self._add_custody_record(
            sample_id=sample_id,
            event_type="Moved",
            from_location=from_location,
            to_location=to_location,
            handled_by=handled_by,
            temperature=temperature,
            humidity=humidity,
            photos=photos,
            notes=notes
        )

        return True

    def update_sample_status(self,
                           sample_id: str,
                           new_status: SampleStatus,
                           handled_by: str,
                           notes: str = "") -> bool:
        """Update sample status"""
        if sample_id not in self.samples:
            return False

        sample = self.samples[sample_id]
        old_status = sample.status
        sample.status = new_status

        # Record status change in custody chain
        self._add_custody_record(
            sample_id=sample_id,
            event_type=f"Status Changed: {old_status.value} → {new_status.value}",
            from_location=sample.current_location,
            to_location=sample.current_location,
            handled_by=handled_by,
            notes=notes
        )

        return True

    def add_photo_documentation(self,
                              sample_id: str,
                              photo_paths: List[str],
                              handled_by: str,
                              notes: str = "") -> bool:
        """Add photo documentation to sample"""
        if sample_id not in self.samples:
            return False

        sample = self.samples[sample_id]
        sample.photos.extend(photo_paths)

        # Record in custody chain
        self._add_custody_record(
            sample_id=sample_id,
            event_type="Photo Documentation",
            from_location=sample.current_location,
            to_location=sample.current_location,
            handled_by=handled_by,
            photos=photo_paths,
            notes=notes
        )

        return True

    def get_sample(self, sample_id: str) -> Optional[Sample]:
        """Get sample by ID"""
        return self.samples.get(sample_id)

    def get_sample_by_barcode(self, barcode: str) -> Optional[Sample]:
        """Find sample by barcode"""
        for sample in self.samples.values():
            if sample.barcode == barcode or sample.sample_id in barcode:
                return sample
        return None

    def get_all_samples(self) -> List[Sample]:
        """Get all samples"""
        return list(self.samples.values())

    def get_samples_by_status(self, status: SampleStatus) -> List[Sample]:
        """Get samples by status"""
        return [s for s in self.samples.values() if s.status == status]

    def get_samples_by_location(self, location: str) -> List[Sample]:
        """Get samples at specific location"""
        return [s for s in self.samples.values() if s.current_location == location]

    def get_chain_of_custody(self, sample_id: str) -> List[ChainOfCustody]:
        """Get complete chain of custody for sample"""
        return self.chain_of_custody.get(sample_id, [])

    def verify_chain_integrity(self, sample_id: str) -> Dict[str, Any]:
        """
        Verify blockchain integrity of chain of custody

        Returns:
            Verification result with details
        """
        if sample_id not in self.chain_of_custody:
            return {
                'valid': False,
                'error': 'No chain of custody found'
            }

        chain = self.chain_of_custody[sample_id]
        errors = []

        for i, record in enumerate(chain):
            # Verify hash
            if not record.verify_hash():
                errors.append(f"Record {i}: Hash verification failed")

            # Verify chain linkage
            if i > 0:
                expected_previous_hash = chain[i-1].current_hash
                if record.previous_hash != expected_previous_hash:
                    errors.append(f"Record {i}: Chain break - previous hash mismatch")

        return {
            'valid': len(errors) == 0,
            'total_records': len(chain),
            'errors': errors
        }

    def search_samples(self, query: str) -> List[Sample]:
        """Search samples by various fields"""
        query = query.lower()
        results = []

        for sample in self.samples.values():
            if (query in sample.sample_id.lower() or
                query in sample.sample_name.lower() or
                query in sample.manufacturer.lower() or
                query in sample.model.lower() or
                query in sample.serial_number.lower() or
                query in sample.batch_number.lower()):
                results.append(sample)

        return results

    def get_sample_history(self, sample_id: str) -> Dict[str, Any]:
        """Get complete history of sample including all events"""
        if sample_id not in self.samples:
            return {'error': 'Sample not found'}

        sample = self.samples[sample_id]
        chain = self.chain_of_custody.get(sample_id, [])

        return {
            'sample': sample.to_dict(),
            'chain_of_custody': [c.to_dict() for c in chain],
            'total_events': len(chain),
            'current_location': sample.current_location,
            'current_status': sample.status.value if isinstance(sample.status, Enum) else sample.status,
            'days_in_system': (datetime.now() - sample.registered_date).days if isinstance(sample.registered_date, datetime) else 0
        }

    def get_location_inventory(self) -> Dict[str, List[Sample]]:
        """Get inventory grouped by location"""
        inventory = {}
        for sample in self.samples.values():
            location = sample.current_location
            if location not in inventory:
                inventory[location] = []
            inventory[location].append(sample)
        return inventory

    def get_expiring_samples(self, days: int = 30) -> List[Sample]:
        """Get samples expiring within specified days"""
        from datetime import timedelta
        threshold = datetime.now() + timedelta(days=days)

        expiring = []
        for sample in self.samples.values():
            if sample.expiry_date and isinstance(sample.expiry_date, datetime):
                if sample.expiry_date <= threshold:
                    expiring.append(sample)

        return expiring

    def get_statistics(self) -> Dict[str, Any]:
        """Get sample tracking statistics"""
        total = len(self.samples)

        by_status = {}
        for status in SampleStatus:
            count = len(self.get_samples_by_status(status))
            by_status[status.value] = count

        by_location = {}
        for sample in self.samples.values():
            loc = sample.current_location
            by_location[loc] = by_location.get(loc, 0) + 1

        total_custody_records = sum(len(chain) for chain in self.chain_of_custody.values())

        return {
            'total_samples': total,
            'by_status': by_status,
            'by_location': by_location,
            'total_custody_records': total_custody_records,
            'avg_custody_records_per_sample': total_custody_records / total if total > 0 else 0
        }

    def export_sample_data(self, sample_id: str) -> Dict[str, Any]:
        """Export complete sample data including chain of custody"""
        if sample_id not in self.samples:
            return {'error': 'Sample not found'}

        sample = self.samples[sample_id]
        chain = self.chain_of_custody.get(sample_id, [])

        return {
            'sample_data': sample.to_dict(),
            'chain_of_custody': [record.to_dict() for record in chain],
            'integrity_check': self.verify_chain_integrity(sample_id),
            'export_timestamp': datetime.now().isoformat()
        }
