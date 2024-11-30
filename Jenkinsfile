pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Initialize Environment') {
            steps {
                script {
                    echo "Desligando quaisquer serviços ativos..."
                    sh "docker compose -f ${DOCKER_COMPOSE_FILE} down || echo 'Nada para desligar'"
                    echo "Iniciando os serviços..."
                    sh "docker compose -f ${DOCKER_COMPOSE_FILE} up --build -d"
                    sh "docker compose -f ${DOCKER_COMPOSE_FILE} ps"
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    echo "Verificando se a aplicação Flask está pronta..."
                    retry(30) {
                        sh '''
                            curl --fail -X GET http://localhost:5000/alunos -o /dev/null \
                            || (echo "Servidor ainda não está pronto, tentando novamente..." && exit 1)
                        '''
                        echo "Servidor Flask está operacional!"
                    }
                }
            }
        }

        stage('Run API Tests') {
            steps {
                script {
                    echo "Executando testes na API..."
                    sh '''
                        STATUS_GET=$(curl -s -o /dev/null -w "%{http_code}" -X GET http://localhost:5000/alunos)
                        if [ "$STATUS_GET" -ne 200 ]; then
                            echo "Falha no teste GET /alunos com código $STATUS_GET"
                            exit 1
                        fi
                        echo "Teste GET /alunos bem-sucedido com código $STATUS_GET"

                        STATUS_POST=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5000/alunos \
                        -H "Content-Type: application/json" \
                        -d '{
                            "nome": "Novo Aluno",
                            "sobrenome": "Sobrenome",
                            "turma": "Turma1",
                            "disciplinas": "Matemática, Ciências"
                        }')
                        if [ "$STATUS_POST" -ne 201 ]; then
                            echo "Falha no teste POST /alunos com código $STATUS_POST"
                            exit 1
                        fi
                        echo "Teste POST /alunos bem-sucedido com código $STATUS_POST"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finalizada, limpando ambiente..."
            sh "docker compose -f ${DOCKER_COMPOSE_FILE} down"
        }
        success {
            echo "Pipeline concluída com sucesso!"
        }
        failure {
            echo "Pipeline falhou! Verifique os logs para detalhes."
        }
    }
}
