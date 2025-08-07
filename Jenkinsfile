pipeline {
    agent any

    stages {
        stage('Run CI/CD Pipeline') {
            steps {
                // Run the main CI script
                sh './run_ci.sh'
            }
        }
    }

    post {
        always {
            // Always publish test results and stop Minikube
            junit 'TEST-RESULTS.xml'
            sh 'minikube stop'
        }
    }
}
