pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/felipecoltrotads/Trabalho_DevOps_22.8453-7.git'
            }
        }
        stage('Run Tests') {
            steps {
                sh '/Trabalho_DevOps/flask/test_app.py'
            }
        }
        stage('Build Docker Images') {
            steps {
                sh 'docker-compose -f /Trabalho_DevOps/docker-compose.yml build'
                sh 'docker-compose -f /Trabalho_DevOps/docker-compose.yml up -d'
            }
        }
        stage('Deploy Application') {
            steps {
                sh 'docker-compose -f /Trabalho_DevOps/docker-compose.yml up -d'
            }
        }
    }
}
