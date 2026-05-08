pipeline {
    agent any

    environment {
        IMAGE_NAME   = 'student-task-manager'
        SELENIUM_IMG = 'selenium-tests'
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {

        // ────────────────────────────────────────────────────
        // STAGE 1: CODE LINTING
        // Runs flake8 to check Python code style (PEP 8)
        // ────────────────────────────────────────────────────
        stage('Code Linting') {
            steps {
                sh '''
                    pip install flake8 --quiet
                    flake8 app.py --max-line-length=120 --statistics
                    echo 'Linting passed successfully.'
                '''
            }
        }

        // ────────────────────────────────────────────────────
        // STAGE 2: CODE BUILD
        // Builds the Docker image for the Flask application
        // ────────────────────────────────────────────────────
        stage('Code Build') {
            steps {
                sh '''
                    docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                    docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                    echo 'Docker image built successfully.'
                '''
            }
        }

        // ────────────────────────────────────────────────────
        // STAGE 3: CONTAINERIZED DEPLOYMENT
        // Deploys the app using Docker Compose
        // ────────────────────────────────────────────────────
        stage('Containerized Deployment') {
            steps {
                sh '''
                    # Stop and remove any existing containers
                    docker compose -f ${COMPOSE_FILE} down --remove-orphans || true
                    # Start fresh deployment
                    docker compose -f ${COMPOSE_FILE} up -d
                    # Wait for the app to become healthy
                    sleep 20
                    # Verify containers are running
                    docker compose -f ${COMPOSE_FILE} ps
                    echo 'Containerized deployment completed.'
                '''
            }
        }

        // ────────────────────────────────────────────────────
        // STAGE 4: CONTAINERIZED SELENIUM TESTING
        // Builds Selenium Docker image and runs tests
        // ────────────────────────────────────────────────────
        stage('Containerized Selenium Testing') {
            steps {
                sh '''
                    # Build the Selenium test Docker image
                    docker build -f Dockerfile.selenium -t ${SELENIUM_IMG}:latest .
                    # Run tests inside Docker, connected to the same network as the app
                    docker run --rm \
                        --network student-task-manager_app-net \
                        -e APP_URL=http://web:5000 \
                        ${SELENIUM_IMG}:latest
                    echo 'Selenium tests completed successfully.'
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished. Cleaning up workspace.'
            cleanWs()
        }
        success {
            echo 'All stages passed. Application deployed and tested successfully!'
        }
        failure {
            echo 'Pipeline failed. Check console output for details.'
            sh 'docker compose -f ${COMPOSE_FILE} logs || true'
        }
    }
}
