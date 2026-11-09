
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

        stage('Analise SonarQube') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline e analise SonarQube executadas com sucesso!'
        }

        failure {
            echo 'Falha na pipeline. Consulte os logs.'
        }
    }
}
