def test_cadastro_aluno(client):
    response = client.post('/cadastro', json={'nome': 'Teste', 'RA': '12345'})
    assert response.status_code == 200
    assert response.json['message'] == 'Cadastro realizado com sucesso'
