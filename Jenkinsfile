
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
    }

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
                sh 'docker --version'
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

        stage('Quality Gate') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'sonarqube-token',
                        variable: 'SONAR_TOKEN'
                    )
                ]) {
                    sh '''
                        .venv/bin/python - <<'PY'
import json
import os
import time
import urllib.request
import urllib.parse
from pathlib import Path

server = "http://sonarqube:9000"
task_file = Path(".scannerwork/report-task.txt")

if not task_file.exists():
    raise SystemExit(
        "ERRO: report-task.txt nao encontrado."
    )

properties = {}

for line in task_file.read_text().splitlines():
    if "=" in line:
        key, value = line.split("=", 1)
        properties[key] = value

ce_task_id = properties.get("ceTaskId")

if not ce_task_id:
    raise SystemExit("ERRO: ceTaskId nao encontrado.")

token = os.environ["SONAR_TOKEN"]

def consultar(caminho):
    url = server + caminho
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": "Bearer " + token
        }
    )
    with urllib.request.urlopen(
        request, timeout=15
    ) as response:
        return json.load(response)

print("Aguardando processamento SonarQube...")

analysis_id = None

for tentativa in range(30):
    resultado = consultar(
        "/api/ce/task?id=" +
        urllib.parse.quote(ce_task_id)
    )

    tarefa = resultado["task"]
    status = tarefa["status"]

    print("Processamento:", status)

    if status == "SUCCESS":
        analysis_id = tarefa.get("analysisId")
        break

    if status in ("FAILED", "CANCELED"):
        raise SystemExit(
            "ERRO: processamento SonarQube " + status
        )

    time.sleep(5)

if not analysis_id:
    raise SystemExit(
        "ERRO: analise nao concluida no prazo."
    )

resultado = consultar(
    "/api/qualitygates/project_status?analysisId=" +
    urllib.parse.quote(analysis_id)
)

quality_gate = resultado["projectStatus"]["status"]

print("QUALITY GATE:", quality_gate)

if quality_gate != "OK":
    raise SystemExit(
        "BLOQUEADO: Quality Gate reprovado."
    )

print("Quality Gate aprovado!")
PY
                    '''
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t citizentech-api:$BUILD_NUMBER .'
            }
        }

        stage('Analise Trivy') {
            steps {
                sh '''
                    echo "Iniciando analise de seguranca Trivy..."

                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      -v trivy_cache:/root/.cache/ \
                      aquasec/trivy:latest image \
                      --scanners vuln \
                      --severity HIGH,CRITICAL \
                      --format json \
                      "citizentech-api:$BUILD_NUMBER" > trivy-report.json

                    echo "Relatorio JSON gerado."

                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      -v trivy_cache:/root/.cache/ \
                      aquasec/trivy:latest image \
                      --scanners vuln \
                      --severity HIGH,CRITICAL \
                      --format table \
                      "citizentech-api:$BUILD_NUMBER"

                    echo "Verificando vulnerabilidades CRITICAL..."

                    docker run --rm \
                      -v /var/run/docker.sock:/var/run/docker.sock \
                      -v trivy_cache:/root/.cache/ \
                      aquasec/trivy:latest image \
                      --scanners vuln \
                      --severity CRITICAL \
                      --exit-code 1 \
                      "citizentech-api:$BUILD_NUMBER"

                    echo "Analise Trivy concluida sem vulnerabilidades CRITICAL."
                '''
            }

            post {
                always {
                    archiveArtifacts(
                        artifacts: 'trivy-report.json',
                        allowEmptyArchive: true
                    )
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline DevSecOps aprovada!'
        }

        failure {
            echo 'Pipeline bloqueada ou com erro. Consulte os logs.'
        }

        always {
            echo 'Execucao finalizada.'
        }
    }
}
