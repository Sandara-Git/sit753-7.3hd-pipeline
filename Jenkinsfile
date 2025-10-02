pipeline {
  agent any
  options { ansiColor('xterm') }   
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
        sh '''#!/usr/bin/env bash
          set -euo pipefail

          echo "== Prepare reports dir =="
          mkdir -p build/test-results

          echo "== Detect tests path =="
          TPATH="."
          if [ -d tests ]; then
            TPATH="tests"
          elif [ -d app/tests ]; then
            TPATH="app/tests"
          fi
          echo "Using TPATH=${TPATH}"

          echo "== Run pytest inside the image =="
          docker run --rm \
            -v "$PWD":/workspace \
            -w /workspace \
            myapp:latest \
            bash -lc '
              set -e
              python3 --version
              pip show pytest coverage || true
              coverage run -m pytest -q "$TPATH" --junitxml=build/test-results/junit.xml || code=$?
              coverage xml -o coverage.xml || true
              if [ "${code:-0}" = "5" ]; then
                echo "No tests collected — continuing (scaffold mode)."
                exit 0
              else
                exit "${code:-0}"
              fi
            '

          echo "== After test run, show report files =="
          ls -la build/test-results || true
          ls -la coverage.xml || true
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'build/test-results/junit.xml'
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
            # sonar-scanner reads SONAR_HOST_URL/SONAR_TOKEN from withSonarQubeEnv/credentials
            ${SCANNER_HOME}/bin/sonar-scanner
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
