pipeline {
  agent any

  options {
    timestamps()
  }

  environment {
    // Set any needed env vars or credentials IDs here
    // DOCKERHUB_CRED = credentials('dockerhub-cred-id')
    // SONAR_TOKEN    = credentials('sonar-token-id')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build') {
      steps {
        sh 'echo "Build step — replace with your real build (e.g., docker build, mvn, npm)"'
        // examples:
        // sh 'docker build -t myapp:latest .'
        // sh 'npm ci && npm run build'
        // sh 'mvn -B -DskipTests package'
      }
    }

    stage('Test') {
      steps {
        sh 'echo "Test step — replace with your tests (e.g., pytest, npm test, mvn test)"'
        // examples:
        // sh 'pytest -q'
        // sh 'npm test -- --watch=false'
        // sh 'mvn -B test'
      }
      post {
        always {
          // If you have JUnit XML results:
          // junit 'reports/junit/*.xml'
        }
      }
    }

    stage('Code Quality') {
      steps {
        sh 'echo "Code Quality — e.g., sonar-scanner or eslint/flake8"'
        // examples:
        // sh 'sonar-scanner -Dsonar.projectKey=myapp -Dsonar.host.url=http://<sonar-host>:9000 -Dsonar.login=$SONAR_TOKEN'
        // sh 'flake8 .'
        // sh 'npx eslint .'
      }
    }

    stage('Security') {
      steps {
        sh 'echo "Security Scan — e.g., trivy/snyk/bandit"'
        // examples:
        // sh 'trivy fs --exit-code 0 --no-progress . || true'
        // sh 'trivy image myapp:latest || true'
        // sh 'bandit -r . || true'
      }
    }

    stage('Deploy (Staging)') {
      when { branch 'main' }
      steps {
        sh 'echo "Deploy to staging — e.g., docker compose up -d, kubectl apply -f ..."' 
      }
    }

    stage('Release') {
      when { branch 'main' }
      steps {
        sh 'echo "Release — tag & push artifacts/images (Docker Hub/ACR/etc.)"'
        // example:
        // withCredentials([usernamePassword(credentialsId: 'dockerhub-cred-id', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
        //   sh 'echo "$PASS" | docker login -u "$USER" --password-stdin'
        //   sh 'docker tag myapp:latest myuser/myapp:${BUILD_NUMBER}'
        //   sh 'docker push myuser/myapp:${BUILD_NUMBER}'
        // }
      }
    }

    stage('Monitoring Hook') {
      steps {
        sh 'echo "Notify/monitoring hook — e.g., curl to Datadog/New Relic/Slack"'
      }
    }
  }

  post {
    success {
      echo 'Pipeline finished successfully '
    }
    failure {
      echo 'Pipeline failed '
    }
    always {
      archiveArtifacts artifacts: '**/build/**', allowEmptyArchive: true
    }
  }
}
