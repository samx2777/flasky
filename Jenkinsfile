pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        DEPLOY_DIR = "/tmp/flask-deploy"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Cloning GitHub repository...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests using pytest...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest
                '''
            }
        }

        stage('Build Application') {
            steps {
                echo 'Preparing application for deployment...'
                sh '''
                    mkdir -p build
                    cp -r app.py requirements.txt build/
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Simulating deployment...'
                sh '''
                    rm -rf ${DEPLOY_DIR}
                    mkdir -p ${DEPLOY_DIR}
                    cp -r build/* ${DEPLOY_DIR}/
                    echo "Application deployed to ${DEPLOY_DIR}"
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for errors.'
        }
    }
}
