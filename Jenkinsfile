pipeline {
    agent any
    
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
                    pylint src/ --output-format=parseable > pylint-report.txt || true
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    echo "Running pytest..."
                    PYTHONPATH=${WORKSPACE}:${PYTHONPATH} pytest tests/ -v --cov=src --cov-report=xml --cov-report=html
                '''
            }
        }
    }
    
    post {
        always {
            echo "============Build Summary==============="
            junit testResults: 'test-results.xml', allowEmptyResults: true, skipPublishingChecks: true

            // Archive Coverage Report
            publishHTML([
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Code Coverage Report',
                keepAll: true,
                alwaysLinkToLastBuild: true
            ])
            archiveArtifacts artifacts: 'pylint-report.txt', allowEmptyArchive: true
            archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
            sh '''
            if [ -f test-results.xml ]; then
                echo "✓ Test results saved: test-results.xml"
            fi
            
            if [ -f coverage.xml ]; then
                
                grep -o 'lines-valid="[^"]*"' coverage.xml || true
                grep -o 'lines-covered="[^"]*"' coverage.xml || true
            fi
            
            if [ -f pylint-report.txt ]; then
                echo "✓ Linting report saved"
                wc -l pylint-report.txt
            fi
        '''
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
}