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
            // Always publish test results and stop K3s
            junit 'TEST-RESULTS.xml'
            sh 'sudo k3s-killall.sh' // Stop K3s
        }
    }
}
