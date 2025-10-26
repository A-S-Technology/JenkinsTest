pipeline {
    // specify where the pipeline will run. Any means it can run on any available agents
    agent any

    triggers {
        // sets pipeline triggers when the push event happens in the connected GitHUB repo
        githubPush()
    }

    options {
        // add timestamp to the console log
        timestamps()
        // abort if it runs longer than 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        // keep only last 20 builds to save spaces
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }
    // environment variables available throughout the pipeline
    environment {
        PYTHON_VERSION = '3.9'
        VENV_DIR = "${WORKSPACE}/.venv"
    }
    parameters {
        string(
            name: "GREET",
            defaultValue: 'Hello',
            description: 'greetings'
        )
    }
    //Now we define the stages
    stages {
        stage('GREET'){
            steps {
                script {
                    echo "${params.GREET}, World"
                }
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
                echo "Repository checked out from ${env.GIT_URL}"
            }
        }
        stage("setup python env"){
            steps {
                sh '''
                    echo "setting up python virtual environment"
                    python3 -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage("Lint code"){
            steps {
                sh '''
                    source ${VENV_DIR}/bin/activate
                    echo "Running pylint.."
                    pylint src/ --exit-zero --format=parseable > pylint-report.txt || true
                    cat pylint-report.txt
                '''
            }
        }
        stage("Run unit tests"){
            steps {
                sh '''
                    source ${VENV_DIR}/bin/activate
                    echo "Running pytest with coverage..."
                    pytest tests/ -v --cov=src --cov-report=xml --cov-report=html
                '''
            }
        }
        stage("Code coverage reprot"){
            steps {
                sh '''
                    source ${VENV_DIR}/bin/activate
                    echo "Generating coverage report..."
                    coverage report
                '''
            }
        }
    }
    post {
        always {
            // archives test results
            junit 'test-results/*.xml' || true
            // publuhes HTML coverage reports in jenkins
            publishHTML target: [
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Code Coverage Report'
            ]
            // archive lint report as artifacts as build artifacts
            archiveArtifacts artifacts: 'pylint-report.txt', allowEmptyArchive: true
        }
        success {
            echo "All tests passed"
        }
        failure {
            echo "X tests failed!"
        }
        cleanup {
            // delete workspace files after the piepline finishes to save disk space
            cleanWs()
        }
    }

}