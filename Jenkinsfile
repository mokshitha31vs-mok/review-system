pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\MOKSHITHA\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        IMAGE_NAME = 'mmokshitha/review-system'
        IMAGE_TAG = 'v1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Check Python') {
            steps {
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat '"%PYTHON%" -m pytest -v test_v1.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME%:%IMAGE_TAG% .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    bat '''
                        docker login -u "%DOCKER_USER%" --password-stdin < nul
                    '''
                    powershell '''
                        $securePassword = ConvertTo-SecureString $env:DOCKER_PASS -AsPlainText -Force
                        $credential = New-Object System.Management.Automation.PSCredential($env:DOCKER_USER, $securePassword)
                        $credential.Password | docker login --username $env:DOCKER_USER --password-stdin
                        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                        docker push "$env:IMAGE_NAME`:$env:IMAGE_TAG"
                        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                        docker logout
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'V1 tests passed and Docker image published successfully!'
        }

        failure {
            echo 'Pipeline failed. Check Console Output for the exact error.'
        }
    }
}
