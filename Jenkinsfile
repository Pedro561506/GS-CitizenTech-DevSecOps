
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Obtendo codigo do GitHub...'
                checkout scm
            }
        }

        stage('Verificar ambiente') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Testes Automatizados') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements-dev.txt
                    .venv/bin/python -m pytest -v
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline inicial executada com sucesso!'
        }
        failure {
            echo 'Falha na pipeline. Consulte os logs.'
        }
    }
}
