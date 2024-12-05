pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/felipecoltrotads/Trabalho_DevOps_22.8453-7.git'
        TARGET_BRANCH = 'main'
    }

    stages {
        stage('Obter Código') {
            steps {
                // Fazer o checkout do código fonte a partir do repositório
                checkout scm: [$class: 'GitSCM', branches: [[name: "${TARGET_BRANCH}"]], userRemoteConfigs: [[url: "${REPO_URL}"]]]
            }
        }

        stage('Compilar e Publicar') {
            steps {
                script {
                    // Construir imagens Docker e iniciar os containers
                    sh '''
                        docker-compose build
                        docker-compose up -d
                    '''
                }
            }
        }

        stage('Executar Testes') {
            steps {
                script {
                    // Aguardar inicialização e rodar testes
                    sh '''
                        sleep 40
                        docker-compose run --rm test
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Execução do pipeline concluída.'
        }
        success {
            echo 'Execução bem-sucedida!'
        }
        failure {
            echo 'Erro na execução do pipeline.'
        }
    }
}
