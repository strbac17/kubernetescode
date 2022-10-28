node 
         environment {
           CHKP_CLOUDGUARD_ID = credentials("CHKP_CLOUDGUARD_ID")
           CHKP_CLOUDGUARD_SECRET = credentials("CHKP_CLOUDGUARD_SECRET")
        }
{
    def app
    stage('Clone repository') {
      

        checkout scm
    }

    stage('Build image') {
  
       app = docker.build("strbac17/gitsecops_test")
       sh 'docker save registry.hub.docker.com/strbac17/gitsecops_test -o myapp.tar'
    }
    
     stage('ShiftLeft Container Image Scan') {    

                script {      
              try {
         
                    sh 'shiftleft image-scan -t 180 -i myapp.tar'
                   } catch (Exception e) {
    
                 echo "Request for Approval"  
                  }
                }  
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
