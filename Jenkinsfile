pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'git@github.com:felipecoltrotads/Trabalho_DevOps_22.8453-7.git'
            }
        }
        stage('Testes') {
            steps {
                sh 'pytest'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
