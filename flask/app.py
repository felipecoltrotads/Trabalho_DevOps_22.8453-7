import time
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelView
from sqlalchemy.exc import OperationalError
from prometheus_flask_exporter import PrometheusMetrics
import logging

application = Flask(__name__)

# Configuração de métricas Prometheus
metrics = PrometheusMetrics(application)

# Configuração de segurança
application.config['SECRET_KEY'] = 'chave_super_segura_12345'  # Substitua por uma chave mais forte

# Configuração do banco de dados
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:password@mariadb/student_db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o banco de dados e AppBuilder
database = SQLAlchemy(application)
app_manager = AppBuilder(application, database.session)

# Configuração de logs
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# Modelo - Tabela Estudante
class Estudante(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    primeiro_nome = database.Column(database.String(50), nullable=False)
    ultimo_nome = database.Column(database.String(50), nullable=False)
    classe = database.Column(database.String(50), nullable=False)
    materias = database.Column(database.String(200), nullable=False)
    registro = database.Column(database.String(20), unique=True, nullable=False)

# Tentativas de inicialização do banco
max_retries = 5
for attempt in range(max_retries):
    try:
        with application.app_context():
            database.create_all()
            # Adicionar usuário admin padrão
            if not app_manager.sm.find_user(username='superuser'):
                app_manager.sm.add_user(
                    username='superuser',
                    first_name='System',
                    last_name='Admin',
                    email='admin@domain.com',
                    role=app_manager.sm.find_role(app_manager.sm.auth_role_admin),
                    password='admin123'
                )
        log.info("Banco de dados configurado com sucesso.")
        break
    except OperationalError:
        if attempt < max_retries - 1:
            log.warning("Falha ao conectar ao banco. Tentando novamente em 3 segundos...")
            time.sleep(3)
        else:
            log.error("Exaustão de tentativas de conexão ao banco de dados.")
            raise

# Visão para o modelo Estudante
class EstudanteView(ModelView):
    datamodel = SQLAInterface(Estudante)
    list_columns = ['id', 'primeiro_nome', 'ultimo_nome', 'classe', 'materias', 'registro']

# Adicionar visão ao painel
app_manager.add_view(
    EstudanteView,
    "Gerenciamento de Estudantes",
    icon="fa-graduation-cap",
    category="Estudantes",
)

# Rota para obter lista de estudantes
@application.route('/estudantes', methods=['GET'])
def obter_estudantes():
    estudantes = Estudante.query.all()
    resultado = [{'id': estudante.id, 'primeiro_nome': estudante.primeiro_nome, 'ultimo_nome': estudante.ultimo_nome, 'classe': estudante.classe, 'materias': estudante.materias, 'registro': estudante.registro} for estudante in estudantes]
    return jsonify(resultado)

# Rota para adicionar estudante
@application.route('/estudantes', methods=['POST'])
def criar_estudante():
    dados = request.get_json()
    novo_estudante = Estudante(
        primeiro_nome=dados['primeiro_nome'],
        ultimo_nome=dados['ultimo_nome'],
        classe=dados['classe'],
        materias=dados['materias'],
        registro=dados['registro']
    )
    database.session.add(novo_estudante)
    database.session.commit()
    log.info(f"Estudante {dados['primeiro_nome']} {dados['ultimo_nome']} adicionado com sucesso.")
    return jsonify({'mensagem': 'Estudante criado com sucesso!'}), 201

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5050, debug=True)
