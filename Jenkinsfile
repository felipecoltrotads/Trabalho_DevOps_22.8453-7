pipeline {
    agent any

    environment {
        // Define o local do composer
        COMPOSER = '/usr/local/bin/composer'
    }

    stages {
        stage('Checkout') {
            steps {
                // Faz o checkout do código do repositório
                git branch: 'main', url: 'https://github.com/felipecoltrotads/Trabalho_DevOps_22.8453-7.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Instala as dependências do Composer
                script {
                    sh "${env.COMPOSER} install --no-interaction"
                }
            }
        }

        stage('Run Tests') {
            steps {
                // Executa os testes com PHPUnit
                script {
                    sh 'php vendor/bin/phpunit'
                }
            }
        }
    }
}
