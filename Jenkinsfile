pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Setup Environment') {
            steps {
                script {
                    echo "Encerrando serviços existentes, se houver..."
                    sh """
                        docker compose -f ${DOCKER_COMPOSE_FILE} down || echo 'Nenhum serviço ativo encontrado'
                    """
                    echo "Subindo serviços..."
                    sh """
                        docker compose -f ${DOCKER_COMPOSE_FILE} up --build -d
                        docker compose -f ${DOCKER_COMPOSE_FILE} ps
                    """
                }
            }
        }

        stage('Application Health Check') {
            steps {
                script {
                    echo "Realizando checagem de saúde do Flask..."
                    retry(30) {
                        sh '''
                            curl --fail -X GET http://localhost:5000/alunos -o /dev/null || {
                                echo "Servidor não respondeu, nova tentativa..."
                                exit 1
                            }
                        '''
                        echo "Servidor Flask está em execução!"
                    }
                }
            }
        }

        stage('API Tests Execution') {
            steps {
                script {
                    echo "Iniciando testes da API..."
                    sh '''
                        RESPONSE_CODE_GET=$(curl -s -o /dev/null -w "%{http_code}" -X GET http://localhost:5000/alunos)
                        if [ "$RESPONSE_CODE_GET" -ne 200 ]; then
                            echo "Falha no teste GET /alunos. Código: $RESPONSE_CODE_GET"
                            exit 1
                        fi
                        echo "Teste GET /alunos passou com sucesso (Código: $RESPONSE_CODE_GET)"

                        RESPONSE_CODE_POST=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:5000/alunos \
                        -H "Content-Type: application/json" \
                        -d '{
                            "nome": "Aluno Teste",
                            "sobrenome": "Teste",
                            "turma": "Turma 1",
                            "disciplinas": "História, Geografia"
                        }')
                        if [ "$RESPONSE_CODE_POST" -ne 201 ]; then
                            echo "Falha no teste POST /alunos. Código: $RESPONSE_CODE_POST"
                            exit 1
                        fi
                        echo "Teste POST /alunos passou com sucesso (Código: $RESPONSE_CODE_POST)"
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "Encerrando serviços e finalizando pipeline..."
            sh "docker compose -f ${DOCKER_COMPOSE_FILE} down"
        }
        success {
            echo "Pipeline executada com sucesso!"
        }
        failure {
            echo "Erro durante a execução do pipeline. Verifique os logs."
        }
    }
}
