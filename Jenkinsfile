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
        sh '''
          set -eo pipefail
          echo "== Show test candidates =="
          find . -maxdepth 3 -type f \\( -name "test_*.py" -o -name "*_test.py" \\) -print || true

          echo "== Run tests with coverage inside container =="
          mkdir -p tests/reports

          docker run --rm \
            -v "$PWD":/workspace \
            -w /workspace \
            myapp:latest \
            bash -lc "set -e
                      python3 --version
                      pip show pytest coverage || true
                      # run tests explicitly in ./tests so discovery can't miss them
                      coverage run -m pytest -q tests --junitxml=tests/reports/junit.xml || exit_code=\\$?
                      coverage xml -o coverage.xml || true
                      # treat 'no tests collected' (5) as success while scaffolding; otherwise propagate exit
                      if [ \\\"\\${exit_code}\\\" = \\\"5\\\" ]; then
                        echo 'No tests collected — continuing (scaffold mode).'
                        exit 0
                      else
                        exit \\\"\\${exit_code:-0}\\\"
                      fi"
          echo "== After test run, show report files =="
          ls -la tests/reports || true
          ls -la coverage.xml || true
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'tests/reports/junit.xml'
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
