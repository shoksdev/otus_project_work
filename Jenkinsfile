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
                    bash scripts/lint.sh
                '''
            }
        }

        stage('Start Selenoid') {
            steps {
                sh '''
                    # Останавливаем предыдущий запуск, если остался
                    docker-compose -f docker-compose.selenoid.yml down || true

                    # Скачиваем образы браузеров из browsers.json
                    docker-compose -f docker-compose.selenoid.yml pull || true

                    # Поднимаем Selenoid + Selenoid UI
                    docker-compose -f docker-compose.selenoid.yml up -d

                    # Ждём, пока Selenoid будет готов
                    timeout 60 bash -c 'until curl -s http://localhost:4444/status > /dev/null; do sleep 2; done'
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
            // Публикуем Allure-отчёт
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]

            // Архив результатов и видео
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'selenoid/video/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'selenoid/logs/**', allowEmptyArchive: true

            // Останавливаем Selenoid
            sh 'docker-compose -f docker-compose.selenoid.yml down || true'
        }
    }
}
