pipeline {
    agent any

    stages {
        stage('Run CI/CD Pipeline') {
            steps {
                sh 'chmod +x run_ci.sh' // Make the script executable
                sh './run_ci.sh'
            }
        }
    }

    post {
        always {
            junit 'TEST-RESULTS.xml'
            sh 'sudo k3s-killall.sh'
        }
    }
}
