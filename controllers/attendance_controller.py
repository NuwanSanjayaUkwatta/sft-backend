from flask import jsonify, request
from models.employee import Employee
from models.attendance import Attendance

import logging

logger = logging.getLogger(__name__)

def mark():
    try:
        # Parse request data
        data = request.json
        employee_id = data.get('employee_id')
        date = data.get('date')
        time = data.get('time')
        status = data.get('status', 'present')  # Default value is 'present' if not provided

        # Check if employee exists
        employee = Employee.objects(id=employee_id).first()
        if not employee:
            logger.error("Employee not found")
            return jsonify({"error": "Employee not found"}), 404

        # Check if attendance record already exists for the employee on the same date
        existing_attendance = Attendance.objects(employee=employee, date=date, time=time).first()
        if existing_attendance:
            logger.error("Attendance record already exists for the employee on the same date")
            return jsonify({"error": "Attendance record already exists for the employee on the same date"}), 400

        # Create attendance record
        attendance = Attendance(employee=employee, date=date, time=time, status=status)
        attendance.save()

        logger.info("Attendance marked successfully")
        return jsonify({"message": "Attendance marked successfully"}), 201

    except Exception as e:
        logger.error("Error marking attendance: %s", str(e))
        return jsonify({"error": str(e)}), 500

def edit(attendance_id):
    try:
        # Parse request data
        data = request.json
        date = data.get('date')
        time = data.get('time')
        status = data.get('status')

        # Check if attendance record exists
        attendance = Attendance.objects(id=attendance_id).first()
        if not attendance:
            return jsonify({"error": "Attendance record not found"}), 404

        # Check if another attendance record already exists for the employee on the same date
        if date and attendance.date != date:
            existing_attendance = Attendance.objects(employee=attendance.employee, date=date, time=time).first()
            if existing_attendance:
                return jsonify({"error": "Another attendance record already exists for the employee on the same date"}), 400

        # Update attendance record
        if date:
            attendance.date = date
        if time:
            attendance.time = time
        if status:
            attendance.status = status
        attendance.save()

        return jsonify({"message": "Attendance record updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_all_attendance():
    try:
        # Get all attendance records from the database
        attendance_records = Attendance.objects.all()

        # Serialize the attendance data
        attendance_data = []
        for record in attendance_records:
            employee = Employee.objects(id=record.employee.id).first()  # Assuming there's a reference to Employee in Attendance
            if employee:  # Make sure the employee exists
                attendance_data.append({
                    "employee_name": employee.name,
                    "employee_id": str(employee.id),
                    "date": record.date,
                    "time": record.time,
                    "status": record.status
                })

        return jsonify({"attendance": attendance_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500