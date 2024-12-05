import pytest
from flask import Flask
from flask.testing import FlaskClient

# Importar a aplicação Flask
from app import application  # Assumindo que a aplicação principal é "application" no app.py

@pytest.fixture
def test_client():
    with application.test_client() as client:
        yield client

def test_obter_estudantes(test_client: FlaskClient):
    """Teste para a rota GET /estudantes"""
    resposta = test_client.get('/estudantes')
    assert resposta.status_code == 200
    assert isinstance(resposta.json, list)

def test_criar_estudante(test_client: FlaskClient):
    """Teste para a rota POST /estudantes"""
    estudante_novo = {
        "primeiro_nome": "João",
        "ultimo_nome": "Pereira",
        "classe": "1-B",
        "materias": "Matemática, Física",
        "registro": "12345"
    }
    resposta = test_client.post('/estudantes', json=estudante_novo)
    assert resposta.status_code == 201
    assert resposta.json['mensagem'] == 'Estudante criado com sucesso!'
