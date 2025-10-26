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
            echo "========== BUILD SUMMARY =========="
            
            // Archive test results
            junit testResults: 'test-results.xml', allowEmptyResults: true
            
            // Archive all reports
            archiveArtifacts artifacts: 'test-results.xml,coverage.xml,pylint-report.txt,htmlcov/**', 
                            allowEmptyArchive: true
            
            // Display test summary
            sh '''
                echo ""
                echo "========== TEST RESULTS =========="
                if [ -f test-results.xml ]; then
                    echo "✓ Test results: test-results.xml"
                    grep -o 'tests="[^"]*"' test-results.xml || echo "No test count found"
                fi
            '''
            
            // Display coverage summary
            sh '''
                . ${VENV_DIR}/bin/activate
                echo ""
                echo "========== COVERAGE SUMMARY =========="
                coverage report || true
            '''
            
            // Display lint summary
            sh '''
                echo ""
                echo "========== LINT REPORT =========="
                if [ -f pylint-report.txt ]; then
                    echo "✓ Pylint issues found: $(wc -l < pylint-report.txt) lines"
                    echo "First 10 issues:"
                    head -10 pylint-report.txt || true
                fi
            '''
            
            echo "========== ARTIFACTS SAVED =========="
            echo "Coverage Report: htmlcov/index.html"
            echo "Test Results: test-results.xml"
            echo "Coverage Data: coverage.xml"
            echo "Lint Report: pylint-report.txt"
            
            cleanWs()
        }
        success {
            echo ""
            echo "========== BUILD SUCCESSFUL =========="
            echo "✓ All tests passed!"
            echo "✓ Check Artifacts tab for reports"
        }
        failure {
            echo ""
            echo "========== BUILD FAILED =========="
            echo "✗ Tests failed - check logs above"
            echo "✗ See Artifacts tab for detailed reports"
        }
    }
    
}