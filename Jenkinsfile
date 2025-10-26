pipeline {
    // specify where the pipeline will run. Any means it can run on any available agents
    agent any
}
triggers {
    githubPush()
}

options {
    timestamps()
    timeout(time: 30, unit: 'MINUTES')
    buildDiscarder(logRotator(numToKeepStr: '20'))
}

environment {
    VENV_DIR = "${WORKSPACE}/.venv"
}

stages {
    stage('Checkout') {
        steps {
            checkout scm
            echo "Repository checked out"
        }
    }
    
    stage('Setup Python Environment') {
        steps {
            sh '''
                echo "Setting up Python virtual environment..."
                python3 -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
            '''
        }
    }
    
    stage('Lint Code') {
        steps {
            sh '''
                . ${VENV_DIR}/bin/activate
                echo "Running pylint..."
                pylint src/ --exit-zero --format=parseable > pylint-report.txt || true
            '''
        }
    }
    
    stage('Run Unit Tests') {
        steps {
            sh '''
                . ${VENV_DIR}/bin/activate
                echo "Running pytest..."
                pytest tests/ -v --cov=src --cov-report=xml --cov-report=html
            '''
        }
    }
}

post {
    always {
        echo "Build completed"
    }
    success {
        echo "✓ Tests passed!"
    }
    failure {
        echo "✗ Tests failed!"
    }
    cleanup {
        cleanWs()
    }
}