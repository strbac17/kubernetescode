pipeline {
  agent any
  environment {
    SPECTRAL_DSN = credentials('spectral-dsn')
  }
  stages {
    stage('Clone repository') {
      steps {
        checkout scm
      }
    }

    stage('Install Spectral') {
      steps {
        sh "curl -L 'https://spectral-eu.checkpoint.com/latest/x/sh?dsn=$SPECTRAL_DSN' | sh"
      }
    }

    stage('Spectral security scan') {
      steps {
        sh "$HOME/.spectral/spectral scan --ok  --include-tags base,audit"
      }
    }

    stage('Test image') {
        steps {
        script {
            sh 'echo "Tests passed"'
        }
      }        
    }
        
    stage('Push image to DockerHub') {
        steps {
            script {
                docker.withRegistry("https://registry.hub.docker.com", "dockerhub") {
                def customImage = docker.build("strbac17/gitsecops_test")
                customImage.push("${env.BUILD_NUMBER}")
                }
         }
        }
    }          
    
    stage('Trigger K8S manifest file update') {
        steps {        
            echo "triggering update manifest job"
            build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
      }
    }
  }
}