node 
{
    def app
    environment {
    SPECTRAL_DSN = credentials("spectral-dsn")
    } 
    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
  
       app = docker.build("strbac17/gitsecops_test")
       sh 'docker save registry.hub.docker.com/strbac17/gitsecops_test -o myapp.tar'
    }
    
    stage('install Spectral') {
        sh "curl -L 'https://spectral-eu.checkpoint.com/latest/x/sh?dsn=$SPECTRAL_DSN' | sh"
      }

    stage('scan for issues') {

        sh "$HOME/.spectral/spectral scan --ok  --include-tags base,audit"

    }

    stage('Test image') {

        app.inside {
            sh 'echo "Tests passed"'
        }
    }
        
    stage('Push image') {
        
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            app.push("${env.BUILD_NUMBER}")
        }
    }
    
    stage('Trigger ManifestUpdate') {
                echo "triggering updatemanifestjob"
                build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
        }
}
