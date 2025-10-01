pipeline {
  agent any
  options { timestamps(); ansiColor('xterm') }
  environment { SCANNER_HOME = tool 'sonar-scanner' }

  stages {
    stage('Checkout') { steps { checkout scm } }

    stage('Build') {
      steps {
        sh '''
          echo "== Build Docker image =="
          docker build -t myapp:latest .
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          echo "== Run tests with coverage =="
          coverage run -m pytest -q
          coverage xml -o coverage.xml || true
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'tests/**/junit*.xml'
          archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
        }
      }
    }

    stage('Code Quality') {
      environment { SONAR_TOKEN = credentials('sonar-token-id') }
      steps {
        withSonarQubeEnv('local-sonar') {
          sh '''
            echo "== SonarQube scan =="
            ${SCANNER_HOME}/bin/sonar-scanner -Dsonar.login=$SONAR_TOKEN
          '''
        }
      }
    }

    stage('Security') {
      steps {
        sh '''
          echo "== Trivy FS scan (repo) =="
          trivy fs --exit-code 0 --no-progress . || true
          echo "== Trivy image scan =="
          trivy image --exit-code 0 --no-progress myapp:latest || true
        '''
      }
    }

    stage('Deploy (Staging)') {
      when { branch 'main' }
      steps {
        sh '''
          echo "== Deploy to staging =="
          docker compose down || true
          docker compose up -d
          docker ps
          echo "== Health check =="
          curl -sS http://localhost:8000/health || true
        '''
      }
    }

    stage('Release') {
      when { branch 'main' }
      environment { DOCKERHUB = credentials('dockerhub-cred-id') }
      steps {
        sh '''
          echo "${DOCKERHUB_PSW}" | docker login -u "${DOCKERHUB_USR}" --password-stdin
          IMAGE="docker.io/${DOCKERHUB_USR}/myapp"
          docker tag myapp:latest $IMAGE:${BUILD_NUMBER}
          docker tag myapp:latest $IMAGE:latest
          docker push $IMAGE:${BUILD_NUMBER}
          docker push $IMAGE:latest
        '''
      }
    }

    stage('Monitoring Hook') {
      steps {
        sh 'echo "Monitoring placeholder — add Slack/Datadog/Prometheus pushgateway as needed"'
      }
    }
  }

  post {
    success { echo "Pipeline succeeded" }
    failure { echo "Pipeline failed" }
  }
}
