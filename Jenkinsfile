pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        DEPLOY_DIR = "C:\\tmp\\flask-deploy"
    }

    stages {

        stage('Clone Repository') {
            steps {
                echo 'Cloning GitHub repository...'
                checkout scm
            }
        }

        stage('Install & Test') {
            steps {
                echo 'Installing dependencies and running tests...'
                bat '''
                    python -m venv %VENV_DIR%
                    call %VENV_DIR%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    python -m pytest
                '''
            }
        }

        stage('Build Application') {
            steps {
                echo 'Preparing application for deployment...'
                bat '''
                    if exist build rmdir /s /q build
                    mkdir build
                    copy app.py build\\
                    copy requirements.txt build\\
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                echo 'Simulating deployment...'
                bat '''
                    if exist %DEPLOY_DIR% rmdir /s /q %DEPLOY_DIR%
                    mkdir %DEPLOY_DIR%
                    xcopy build %DEPLOY_DIR% /E /I /Y
                    echo Application deployed to %DEPLOY_DIR%
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
