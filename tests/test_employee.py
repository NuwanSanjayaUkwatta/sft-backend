import unittest
from server import app
import json

class TestEmployeeAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Clean up any existing test data before running each test
        self.cleanup_test_data()

    def tearDown(self):
        # Clean up any test data after running each test
        self.cleanup_test_data()

    def cleanup_test_data(self):
        # Implement logic to clean up test data (e.g., delete test employees)
        pass

    def test_create_employee(self):
        data = {'name': 'John Doe', 'date_of_birth': '1990-01-01', 'department': 'IT', 'address': '123 Main St', 'contact_number': '123-456-7890'}
        response = self.app.post('/api/employees/create', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Employee saved successfully')

    def test_get_all_employees(self):
        response = self.app.get('/api/employees/all')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_employee_by_id(self):
        # Assuming there's an existing employee with ID 
        response = self.app.get('/api/employees/get/662e2864bedbe2f14a8735a7')
        self.assertIsInstance(response.json, dict)

    def test_update_employee(self):
        data = {'name': 'Jane Doe', 'department': 'HR'}
        # Assuming there's an existing employee with ID 
        response = self.app.put('/api/employees/update/662e2864bedbe2f14a8735a7', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Employee updated successfully')

    def test_delete_employee(self):
        # Assuming there's an existing employee with ID 
        response = self.app.delete('/api/employees/delete/662e2864bedbe2f14a8735a7')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Employee deleted successfully')

if __name__ == '__main__':
    unittest.main()
