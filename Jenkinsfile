pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\MOKSHITHA\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        DOCKER = 'C:\\Users\\MOKSHITHA\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
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

        stage('Check Docker Access') {
            steps {
                bat '"%DOCKER%" info'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER%" --version'
                bat '"%DOCKER%" build -t %IMAGE_NAME%:%IMAGE_TAG% .'
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
                    powershell '''
                        $ErrorActionPreference = "Stop"

                        $username = $env:DOCKER_USER.Trim()
                        $token = $env:DOCKER_PASS.Trim()
                        $docker = $env:DOCKER

                        if ([string]::IsNullOrWhiteSpace($username)) {
                            throw "Docker Hub username is empty."
                        }

                        if ([string]::IsNullOrWhiteSpace($token)) {
                            throw "Docker Hub token is empty."
                        }

                        $token | & $docker login --username $username --password-stdin

                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker Hub login failed."
                        }

                        Write-Host "Docker Hub login successful."

                        & $docker push "$env:IMAGE_NAME`:$env:IMAGE_TAG"

                        if ($LASTEXITCODE -ne 0) {
                            throw "Docker Hub image push failed."
                        }

                        Write-Host "Docker image pushed successfully."
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