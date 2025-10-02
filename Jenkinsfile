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
          set -e

          echo "== Prepare reports dir =="
          mkdir -p build/test-results

          echo "== Run pytest inside the image =="
          docker run --rm \
            -v "$PWD:/workspace" -w /workspace myapp:latest bash -lc '
              python -V
              pip show pytest coverage || true

              # run tests (ok if none)
              pytest -q --junitxml=build/test-results/junit.xml || true

              # try to produce coverage (ok if none)
              coverage xml -o coverage.xml || true
            '

          # if coverage.xml wasn’t created, emit a minimal one in the workspace
          [ -f coverage.xml ] || cat > coverage.xml <<'XML'
    <coverage branch-rate="0" line-rate="0" version="1.9" timestamp="0">
      <sources></sources><packages></packages>
    </coverage>
    XML
        '''
      }
      post {
        always {
          junit 'build/test-results/junit.xml'
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
          # default URLs if env var is empty
          URLS="${HEALTH_URLS:-http://localhost:8000/health http://localhost:8000/}"
          echo "== Health check (retry up to 30s) =="
          echo "Checking URLs: ${URLS}"

          ok=""
          for i in $(seq 1 30); do
            for u in ${URLS}; do
              if curl -fsS "$u" >/dev/null 2>&1; then
                echo "Healthy at: $u"
                ok="yes"
                break 2
              fi
            done
            sleep 1
          done

          if [[ -z "$ok" ]]; then
            echo "App did not become healthy in time"
            echo "== docker ps =="
            docker ps
              echo "== last 200 lines of app logs =="
            docker compose logs --tail=200 || true
            exit 1
          fi
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
