import unittest
from app import app

class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True 

    def test_home_status_code(self):
        response = self.app.get('/') 
        self.assertEqual(response.status_code, 200)

    def test_download_endpoint(self):
        response = self.app.get('/download')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Download successful', response.data.decode('utf-8'))

    def test_add_employee(self):
        response = self.app.post('/addemp', data=dict(
            emp_id="001", first_name="John", last_name="Doe", primary_skill="Python", location="NY"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('was successfully added to the database', response.data.decode('utf-8'))

    def test_get_employee(self):
        # Assuming you have a way to add an employee for testing purposes
        self.app.post('/addemp', data=dict(
            emp_id="001", first_name="John", last_name="Doe", primary_skill="Python", location="NY"
        ), follow_redirects=True)
        response = self.app.get('/getemp?emp_id=001')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Employee ID:<br>', response.data.decode('utf-8'))
        # Make sure to check for other details similarly

if __name__ == '__main__':
    unittest.main()
