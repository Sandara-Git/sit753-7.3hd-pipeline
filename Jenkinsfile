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
            -e TPATH="$TPATH" \
            -v "$PWD":/workspace \
            -w /workspace \
            myapp:latest \
            bash -lc '
              set -e
              python3 --version
              pip show pytest coverage || true

              # run pytest; keep exit code for handling "no tests collected" (5)
              coverage run -m pytest -q "$TPATH" --junitxml=build/test-results/junit.xml || code=$?

              # always try to emit coverage.xml
              coverage xml -o coverage.xml || true

              # Treat "no tests collected" (5) as success so pipeline continues
              if [ "${code:-0}" = "5" ]; then
                echo "No tests collected — continuing (scaffold mode)."
                exit 0
              else
                exit "${code:-0}"
              fi
            '

          # Host-side safety net: ensure files exist even if container didn’t write them
          [ -f build/test-results/junit.xml ] || cat > build/test-results/junit.xml <<EOF
    <?xml version="1.0" encoding="UTF-8"?>
    <testsuite name="empty" tests="0" failures="0" errors="0" skipped="0"></testsuite>
    EOF
          [ -f coverage.xml ] || echo "<coverage/>" > coverage.xml

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
          echo "== Health check (retry up to 30s) =="
          for i in $(seq 1 30); do
            if curl -fsS "$URL_HEALTH" >/dev/null 2>&1 || curl -fsS "$URL_ROOT" >/dev/null 2>&1; then
              echo "App is up"
              exit 0
            fi
            sleep 1
          done
          echo "App did not become healthy in time"
          exit 1
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
          echo "Pushing ${IMAGE} ..."
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
