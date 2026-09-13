pipeline {
    agent any

    tools {
        // Имя, которое вы задали в Global Tool Configuration для Allure
        allure 'allure'
    }

    environment {
        PYTHONUNBUFFERED = '1'
        API_BASE_URL = "https://restful-booker.herokuapp.com"
        API_USERNAME = "admin"
        API_PASSWORD = "password123"
        UI_BASE_URL = "https://automationexercise.com"
        SELENOID_URL = 'http://selenoid:4444/wd/hub'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python env') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Ruff Check') {
            steps {
                sh '''
                    . .venv/bin/activate
                    ruff format .
                    ruff check --fix .
                '''
            }
        }

        stage('Start Selenoid') {
            steps {
                sh '''
                    docker compose pull || true
                    docker compose up -d

                    timeout 60 bash -c 'until curl -s http://selenoid:4444/status > /dev/null; do sleep 2; done'
                    echo "Selenoid is up"
                '''
            }
        }

        stage('Run UI Tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest tests/ --alluredir=allure-results
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'selenoid/video/**', allowEmptyArchive: true
            sh 'docker compose down || true'
        }
    }
}
