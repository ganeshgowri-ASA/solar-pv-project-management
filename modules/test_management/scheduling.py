"""
AI-Powered Test Scheduling Engine with Resource Optimization
"""

from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
import uuid

from .models import TestSchedule, TestStatus, Priority, Sample, TestProtocol, Equipment, Staff


@dataclass
class ResourceConflict:
    """Resource conflict information"""
    conflict_type: str  # Equipment, Staff, Time
    resource_id: str
    conflicting_schedules: List[str]
    severity: str  # High, Medium, Low


@dataclass
class ScheduleRecommendation:
    """AI scheduling recommendation"""
    recommended_start: datetime
    recommended_end: datetime
    confidence_score: float
    assigned_equipment: List[str]
    assigned_staff: List[str]
    reasoning: str
    alternative_slots: List[Dict[str, Any]]


class AIScheduler:
    """
    Intelligent test scheduling engine with:
    - Resource optimization
    - Conflict detection and resolution
    - Priority-based queue management
    - TAT prediction
    - Automatic reminders
    """

    def __init__(self):
        self.schedules: Dict[str, TestSchedule] = {}
        self.equipment_calendar: Dict[str, List[Dict]] = {}  # equipment_id -> bookings
        self.staff_calendar: Dict[str, List[Dict]] = {}  # staff_id -> bookings

    def schedule_test(self,
                     sample: Sample,
                     protocol: TestProtocol,
                     priority: Priority,
                     requested_date: Optional[datetime] = None,
                     assigned_equipment: Optional[List[str]] = None,
                     assigned_staff: Optional[List[str]] = None,
                     created_by: str = "system") -> Tuple[TestSchedule, List[ResourceConflict]]:
        """
        Schedule a test with intelligent resource allocation

        Args:
            sample: Sample to test
            protocol: Test protocol to execute
            priority: Test priority
            requested_date: Preferred start date (optional)
            assigned_equipment: Pre-assigned equipment (optional)
            assigned_staff: Pre-assigned staff (optional)
            created_by: Who created the schedule

        Returns:
            Tuple of (TestSchedule, List of conflicts if any)
        """
        schedule_id = f"SCHED_{uuid.uuid4().hex[:8].upper()}"

        # Determine start time
        if requested_date:
            scheduled_start = requested_date
        else:
            # Auto-schedule based on priority and availability
            scheduled_start = self._find_optimal_slot(
                protocol=protocol,
                priority=priority,
                equipment_ids=assigned_equipment,
                staff_ids=assigned_staff
            )

        # Calculate end time based on protocol duration
        duration_minutes = protocol.estimated_duration
        scheduled_end = scheduled_start + timedelta(minutes=duration_minutes)

        # Assign resources if not provided
        if not assigned_equipment:
            assigned_equipment = self._assign_optimal_equipment(
                protocol=protocol,
                start_time=scheduled_start,
                end_time=scheduled_end
            )

        if not assigned_staff:
            assigned_staff = self._assign_optimal_staff(
                protocol=protocol,
                start_time=scheduled_start,
                end_time=scheduled_end
            )

        # Create schedule
        schedule = TestSchedule(
            schedule_id=schedule_id,
            sample_id=sample.sample_id,
            protocol_id=protocol.protocol_id,
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            assigned_equipment=assigned_equipment,
            assigned_staff=assigned_staff,
            priority=priority,
            status=TestStatus.SCHEDULED,
            estimated_tat=duration_minutes // 60,  # Convert to hours
            created_by=created_by
        )

        # Check for conflicts
        conflicts = self._detect_conflicts(schedule)

        # Store schedule
        self.schedules[schedule_id] = schedule

        # Update resource calendars
        self._update_resource_calendars(schedule)

        return schedule, conflicts

    def _find_optimal_slot(self,
                          protocol: TestProtocol,
                          priority: Priority,
                          equipment_ids: Optional[List[str]] = None,
                          staff_ids: Optional[List[str]] = None) -> datetime:
        """Find optimal time slot based on priority and resource availability"""

        # Start from next available working hour
        now = datetime.now()
        current_hour = now.hour

        # Working hours: 8 AM - 6 PM
        if current_hour < 8:
            start_search = now.replace(hour=8, minute=0, second=0, microsecond=0)
        elif current_hour >= 18:
            # Next day at 8 AM
            start_search = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
        else:
            # Round up to next hour
            start_search = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

        # Priority-based scheduling
        if priority == Priority.CRITICAL:
            # Schedule ASAP, even if it means displacing lower priority tests
            return start_search
        elif priority == Priority.HIGH:
            # Schedule within 24 hours
            return start_search
        elif priority == Priority.MEDIUM:
            # Schedule within 3 days
            return start_search + timedelta(hours=24)
        else:
            # Schedule within 1 week
            return start_search + timedelta(days=3)

    def _assign_optimal_equipment(self,
                                 protocol: TestProtocol,
                                 start_time: datetime,
                                 end_time: datetime) -> List[str]:
        """Assign optimal equipment based on availability and protocol requirements"""

        assigned = []
        for required_eq in protocol.required_equipment:
            # In a real implementation, this would check actual equipment availability
            # For now, we'll create equipment IDs based on requirement
            eq_id = f"EQ_{required_eq.replace(' ', '_').upper()}_001"
            assigned.append(eq_id)

        return assigned

    def _assign_optimal_staff(self,
                            protocol: TestProtocol,
                            start_time: datetime,
                            end_time: datetime) -> List[str]:
        """Assign optimal staff based on skills and availability"""

        assigned = []
        for required_skill in protocol.required_staff_skills:
            # In a real implementation, this would check actual staff availability and skills
            # For now, we'll create staff IDs based on skill requirement
            staff_id = f"STAFF_{required_skill.replace(' ', '_').upper()}_001"
            assigned.append(staff_id)

        return assigned

    def _detect_conflicts(self, schedule: TestSchedule) -> List[ResourceConflict]:
        """Detect scheduling conflicts"""
        conflicts = []

        # Check for overlapping schedules
        for existing_id, existing in self.schedules.items():
            if existing.status in [TestStatus.CANCELLED, TestStatus.COMPLETED]:
                continue

            # Check time overlap
            if not (schedule.scheduled_end <= existing.scheduled_start or
                   schedule.scheduled_start >= existing.scheduled_end):

                # Check equipment conflicts
                overlapping_equipment = set(schedule.assigned_equipment) & set(existing.assigned_equipment)
                if overlapping_equipment:
                    conflicts.append(ResourceConflict(
                        conflict_type="Equipment",
                        resource_id=list(overlapping_equipment)[0],
                        conflicting_schedules=[existing_id],
                        severity="High"
                    ))

                # Check staff conflicts
                overlapping_staff = set(schedule.assigned_staff) & set(existing.assigned_staff)
                if overlapping_staff:
                    conflicts.append(ResourceConflict(
                        conflict_type="Staff",
                        resource_id=list(overlapping_staff)[0],
                        conflicting_schedules=[existing_id],
                        severity="Medium"
                    ))

        return conflicts

    def _update_resource_calendars(self, schedule: TestSchedule):
        """Update equipment and staff calendars"""

        booking = {
            'schedule_id': schedule.schedule_id,
            'start': schedule.scheduled_start,
            'end': schedule.scheduled_end,
            'sample_id': schedule.sample_id,
            'protocol_id': schedule.protocol_id
        }

        # Update equipment calendars
        for eq_id in schedule.assigned_equipment:
            if eq_id not in self.equipment_calendar:
                self.equipment_calendar[eq_id] = []
            self.equipment_calendar[eq_id].append(booking)

        # Update staff calendars
        for staff_id in schedule.assigned_staff:
            if staff_id not in self.staff_calendar:
                self.staff_calendar[staff_id] = []
            self.staff_calendar[staff_id].append(booking)

    def get_schedule(self, schedule_id: str) -> Optional[TestSchedule]:
        """Get schedule by ID"""
        return self.schedules.get(schedule_id)

    def get_all_schedules(self) -> List[TestSchedule]:
        """Get all schedules"""
        return list(self.schedules.values())

    def get_schedules_by_status(self, status: TestStatus) -> List[TestSchedule]:
        """Get schedules by status"""
        return [s for s in self.schedules.values() if s.status == status]

    def get_schedules_by_priority(self, priority: Priority) -> List[TestSchedule]:
        """Get schedules by priority"""
        return [s for s in self.schedules.values() if s.priority == priority]

    def get_schedules_by_date_range(self, start_date: datetime, end_date: datetime) -> List[TestSchedule]:
        """Get schedules within date range"""
        return [s for s in self.schedules.values()
                if s.scheduled_start >= start_date and s.scheduled_start <= end_date]

    def reschedule(self,
                  schedule_id: str,
                  new_start: datetime,
                  reason: str = "") -> Tuple[bool, List[ResourceConflict]]:
        """
        Reschedule a test

        Returns:
            Tuple of (success, conflicts)
        """
        if schedule_id not in self.schedules:
            return False, []

        schedule = self.schedules[schedule_id]

        # Calculate new end time
        duration = schedule.scheduled_end - schedule.scheduled_start
        new_end = new_start + duration

        # Check for conflicts at new time
        temp_schedule = TestSchedule(
            schedule_id=schedule_id + "_temp",
            sample_id=schedule.sample_id,
            protocol_id=schedule.protocol_id,
            scheduled_start=new_start,
            scheduled_end=new_end,
            assigned_equipment=schedule.assigned_equipment,
            assigned_staff=schedule.assigned_staff,
            priority=schedule.priority,
            status=schedule.status
        )

        conflicts = self._detect_conflicts(temp_schedule)

        if not conflicts:
            # Update schedule
            old_start = schedule.scheduled_start
            old_end = schedule.scheduled_end

            schedule.scheduled_start = new_start
            schedule.scheduled_end = new_end
            schedule.notes += f"\nRescheduled from {old_start} to {new_start}. Reason: {reason}"

            # Update calendars
            self._remove_from_calendars(schedule_id, old_start, old_end,
                                       schedule.assigned_equipment,
                                       schedule.assigned_staff)
            self._update_resource_calendars(schedule)

            return True, []
        else:
            return False, conflicts

    def _remove_from_calendars(self, schedule_id: str, start: datetime, end: datetime,
                              equipment_ids: List[str], staff_ids: List[str]):
        """Remove booking from resource calendars"""

        # Remove from equipment calendars
        for eq_id in equipment_ids:
            if eq_id in self.equipment_calendar:
                self.equipment_calendar[eq_id] = [
                    b for b in self.equipment_calendar[eq_id]
                    if b['schedule_id'] != schedule_id
                ]

        # Remove from staff calendars
        for staff_id in staff_ids:
            if staff_id in self.staff_calendar:
                self.staff_calendar[staff_id] = [
                    b for b in self.staff_calendar[staff_id]
                    if b['schedule_id'] != staff_id
                ]

    def cancel_schedule(self, schedule_id: str, reason: str = "") -> bool:
        """Cancel a scheduled test"""
        if schedule_id not in self.schedules:
            return False

        schedule = self.schedules[schedule_id]
        schedule.status = TestStatus.CANCELLED
        schedule.notes += f"\nCancelled: {reason}"

        # Remove from calendars
        self._remove_from_calendars(
            schedule_id,
            schedule.scheduled_start,
            schedule.scheduled_end,
            schedule.assigned_equipment,
            schedule.assigned_staff
        )

        return True

    def start_test(self, schedule_id: str) -> bool:
        """Mark test as started"""
        if schedule_id not in self.schedules:
            return False

        schedule = self.schedules[schedule_id]
        schedule.status = TestStatus.IN_PROGRESS
        schedule.actual_start = datetime.now()

        return True

    def complete_test(self, schedule_id: str) -> bool:
        """Mark test as completed"""
        if schedule_id not in self.schedules:
            return False

        schedule = self.schedules[schedule_id]
        schedule.status = TestStatus.COMPLETED
        schedule.actual_end = datetime.now()

        return True

    def get_equipment_availability(self,
                                  equipment_id: str,
                                  start_date: datetime,
                                  end_date: datetime) -> List[Dict[str, Any]]:
        """Get equipment availability for date range"""
        if equipment_id not in self.equipment_calendar:
            return []

        bookings = self.equipment_calendar[equipment_id]
        relevant_bookings = [
            b for b in bookings
            if not (b['end'] <= start_date or b['start'] >= end_date)
        ]

        return relevant_bookings

    def get_staff_availability(self,
                             staff_id: str,
                             start_date: datetime,
                             end_date: datetime) -> List[Dict[str, Any]]:
        """Get staff availability for date range"""
        if staff_id not in self.staff_calendar:
            return []

        bookings = self.staff_calendar[staff_id]
        relevant_bookings = [
            b for b in bookings
            if not (b['end'] <= start_date or b['start'] >= end_date)
        ]

        return relevant_bookings

    def predict_tat(self, protocol: TestProtocol, priority: Priority) -> int:
        """
        Predict Turnaround Time (TAT) in hours using ML

        This is a simplified version. In production, this would use
        trained ML models based on historical data.
        """
        base_duration = protocol.estimated_duration / 60  # Convert to hours

        # Factor in priority
        priority_multipliers = {
            Priority.CRITICAL: 1.0,
            Priority.HIGH: 1.2,
            Priority.MEDIUM: 1.5,
            Priority.LOW: 2.0
        }

        # Factor in current queue length
        queue_length = len(self.get_schedules_by_status(TestStatus.SCHEDULED))
        queue_factor = 1 + (queue_length * 0.1)  # 10% increase per queued test

        predicted_tat = base_duration * priority_multipliers.get(priority, 1.5) * queue_factor

        return int(predicted_tat)

    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        scheduled = self.get_schedules_by_status(TestStatus.SCHEDULED)
        in_progress = self.get_schedules_by_status(TestStatus.IN_PROGRESS)

        by_priority = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 0,
            Priority.MEDIUM: 0,
            Priority.LOW: 0
        }

        for schedule in scheduled:
            by_priority[schedule.priority] = by_priority.get(schedule.priority, 0) + 1

        return {
            'total_scheduled': len(scheduled),
            'in_progress': len(in_progress),
            'by_priority': {k.value: v for k, v in by_priority.items()},
            'oldest_scheduled': min([s.scheduled_start for s in scheduled]) if scheduled else None,
            'next_available_slot': self._find_optimal_slot(
                protocol=None,  # Generic slot
                priority=Priority.MEDIUM,
                equipment_ids=None,
                staff_ids=None
            )
        }

    def get_overdue_tests(self) -> List[TestSchedule]:
        """Get tests that are overdue (scheduled start time has passed)"""
        now = datetime.now()
        overdue = []

        for schedule in self.schedules.values():
            if schedule.status == TestStatus.SCHEDULED and schedule.scheduled_start < now:
                overdue.append(schedule)

        return sorted(overdue, key=lambda s: s.scheduled_start)

    def auto_resolve_conflicts(self, schedule_id: str) -> Tuple[bool, str]:
        """
        Automatically resolve scheduling conflicts

        Returns:
            Tuple of (success, resolution message)
        """
        if schedule_id not in self.schedules:
            return False, "Schedule not found"

        schedule = self.schedules[schedule_id]
        conflicts = self._detect_conflicts(schedule)

        if not conflicts:
            return True, "No conflicts to resolve"

        # Try to reschedule to next available slot
        new_start = self._find_optimal_slot(
            protocol=None,
            priority=schedule.priority,
            equipment_ids=schedule.assigned_equipment,
            staff_ids=schedule.assigned_staff
        )

        success, new_conflicts = self.reschedule(
            schedule_id,
            new_start,
            "Auto-resolved conflicts"
        )

        if success:
            return True, f"Rescheduled to {new_start}"
        else:
            return False, f"Could not resolve conflicts. New conflicts: {len(new_conflicts)}"

    def get_statistics(self) -> Dict[str, Any]:
        """Get scheduling statistics"""
        total = len(self.schedules)
        by_status = {}
        for status in TestStatus:
            count = len(self.get_schedules_by_status(status))
            by_status[status.value] = count

        completed = [s for s in self.schedules.values() if s.status == TestStatus.COMPLETED]
        avg_completion_time = None
        if completed:
            completion_times = [
                (s.actual_end - s.actual_start).total_seconds() / 3600
                for s in completed
                if s.actual_start and s.actual_end
            ]
            if completion_times:
                avg_completion_time = sum(completion_times) / len(completion_times)

        return {
            'total_schedules': total,
            'by_status': by_status,
            'avg_completion_time_hours': avg_completion_time,
            'total_equipment_bookings': sum(len(bookings) for bookings in self.equipment_calendar.values()),
            'total_staff_bookings': sum(len(bookings) for bookings in self.staff_calendar.values()),
            'overdue_count': len(self.get_overdue_tests())
        }
