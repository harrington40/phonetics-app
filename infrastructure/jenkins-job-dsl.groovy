#!/bin/bash
# Jenkins Job DSL for Phonetics App CI/CD

# This file can be used with Jenkins Job DSL plugin
# Place in: $JENKINS_HOME/jobs/*/groovy-jobs/

pipelineJob('phonetics-app-pipeline') {
  description('CI/CD Pipeline for Phonetics Learning App')
  
  properties {
    disableConcurrentBuilds()
    buildDiscarder {
      strategy {
        logRotator {
          daysToKeepStr('30')
          numToKeepStr('10')
          artifactDaysToKeepStr('-1')
          artifactNumToKeepStr('5')
        }
      }
    }
  }

  triggers {
    githubPush()
  }

  definition {
    cps {
      script(readFileAsString('Jenkinsfile'))
      sandbox(true)
    }
  }
}
