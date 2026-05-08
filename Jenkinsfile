pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'student-task-manager'
        SELENIUM_IMG = 'selenium-tests'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {

        stage('Code Linting') {
            steps {
                sh '''
                    python3 -m flake8 app.py --max-line-length=120 --statistics
                    echo 'Linting passed successfully.'
                '''
            }
        }

        stage('Code Build') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:latest .
                    echo 'Docker image built successfully.'
                '''
            }
        }

        stage('Containerized Deployment') {
            steps {
                sh '''
                    docker compose -f ${COMPOSE_FILE} down --remove-orphans || true
                    docker compose -f ${COMPOSE_FILE} up -d
                    sleep 20
                    docker compose -f ${COMPOSE_FILE} ps
                    echo 'Deployment completed.'
                '''
            }
        }

        stage('Containerized Selenium Testing') {
            steps {
                sh '''
                    docker build -f Dockerfile.selenium -t ${SELENIUM_IMG}:latest .
                    docker run --rm \
                        --network student-task-manager-pipeline_app-net \
                        -e APP_URL=http://web:5000 \
                        ${SELENIUM_IMG}:latest
                    echo 'Selenium tests passed.'
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
            cleanWs()
        }
        success {
            echo 'All stages passed!'
        }
        failure {
            echo 'Pipeline failed. Check console output for details.'
        }
    }
}
