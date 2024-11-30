from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Configuração da aplicação Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mariadb/alunos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Aluno
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    ra = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Aluno {self.nome}>'

# Rotas
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([{'id': aluno.id, 'nome': aluno.nome, 'ra': aluno.ra} for aluno in alunos])

@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.get_json()
    novo_aluno = Aluno(nome=dados['nome'], ra=dados['ra'])
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'}), 201

@app.route('/alunos/<int:id>', methods=['GET'])
def obter_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    return jsonify({'id': aluno.id, 'nome': aluno.nome, 'ra': aluno.ra})

@app.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    dados = request.get_json()
    aluno = Aluno.query.get_or_404(id)
    aluno.nome = dados['nome']
    aluno.ra = dados['ra']
    db.session.commit()
    return jsonify({'mensagem': 'Aluno atualizado com sucesso!'})

@app.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno deletado com sucesso!'})

# Inicialização da aplicação
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Garante que o banco e as tabelas sejam criados
    app.run(host='0.0.0.0', port=5000)
