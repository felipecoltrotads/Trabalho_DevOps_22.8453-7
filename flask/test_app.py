import unittest
from app import app, db

class TestAluno(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def test_cadastro_aluno(self):
        response = self.client.post('/alunos', json={'nome': 'Felipe', 'ra': '123456'})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
