pipeline {
  agent any

  options {
    buildDiscarder(logRotator(numToKeepStr: '10', daysToKeepStr: '60'))
    parallelsAlwaysFailFast()
    disableConcurrentBuilds()
  }

  triggers {
    cron('H 8 * * 6')
  }

  environment {
    REGISTRY = 'git.devmem.ru'
    REGISTRY_URL = "https://${REGISTRY}"
    REGISTRY_CREDS_ID = 'gitea-user'
    IMAGE_OWNER = 'projects'
    IMAGE_BASENAME = 'samgrabby'
    IMAGE_FULLNAME = "${REGISTRY}/${IMAGE_OWNER}/${IMAGE_BASENAME}"
    IMAGE_ALT_TAG = 'latest'
    DOCKERFILE = '.docker/django/ci.Dockerfile'
    LABEL_AUTHORS = 'Ilya Pavlov <piv@devmem.ru>'
    LABEL_TITLE = 'samgrabby'
    LABEL_DESCRIPTION = 'samgrabby'
    LABEL_URL = 'https://soft.devmem.ru'
    LABEL_CREATED = sh(script: "date '+%Y-%m-%dT%H:%M:%S%:z'", returnStdout: true).toString().trim()
    REVISION = GIT_COMMIT.take(7)

    GPG_KEY_CREDS_ID = 'jenkins-gpg-key'
    HELM_CHART_GIT_URL = 'https://git.devmem.ru/projects/helm-charts.git'

    ANSIBLE_IMAGE = "${REGISTRY}/${IMAGE_OWNER}/ansible:base"
    ANSIBLE_CONFIG = '.ansible/ansible.cfg'
    ANSIBLE_PLAYBOOK = '.ansible/playbook.yml'
    ANSIBLE_INVENTORY = '.ansible/hosts'
    ANSIBLE_CREDS_ID = 'jenkins-ssh-key'
    ANSIBLE_VAULT_CREDS_ID = 'ansible-vault-password'
  }

  parameters {
    booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Deploy this revision?')
    booleanParam(name: 'BUMP_HELM', defaultValue: false, description: 'Bump Helm chart version?')
    booleanParam(name: 'REBUILD', defaultValue: false, description: 'Reduild this revision image?')
    string(name: 'ANSIBLE_EXTRAS', defaultValue: '', description: 'ansible-playbook extra params')
  }

  stages {
    stage('Build image (cache)') {
      when {
        branch 'main'
        not {
          anyOf {
            expression { params.DEPLOY }
            expression { params.REBUILD }
            triggeredBy 'TimerTrigger'
            triggeredBy cause: 'UserIdCause'
            changeRequest()
          }
        }
      }
      steps {
        script {
          buildDockerImage(
            dockerFile: "${DOCKERFILE}",
            tag: "${REVISION}",
            altTag: "${IMAGE_ALT_TAG}",
            useCache: true,
            cacheFrom: "${IMAGE_FULLNAME}:${IMAGE_ALT_TAG}"
          )
        }
      }
    }

    stage('Build image (no cache)') {
      when {
        branch 'main'
        anyOf {
          expression { params.REBUILD }
          triggeredBy 'TimerTrigger'
        }
      }
      steps {
        script {
          buildDockerImage(
            dockerFile: "${DOCKERFILE}",
            tag: "${REVISION}",
            altTag: "${IMAGE_ALT_TAG}"
          )
        }
      }
    }

    stage('Bump Helm chart version') {
      when {
        branch 'main'
        expression { params.BUMP_HELM }
      }
      steps {
        script {
          bumpHelmChartVersion()
        }
      }
    }

    stage('Deploy') {
      agent {
        docker {
          image env.ANSIBLE_IMAGE
          registryUrl env.REGISTRY_URL
          registryCredentialsId env.REGISTRY_CREDS_ID
          alwaysPull true
          reuseNode true
        }
      }
      when {
        branch 'main'
        beforeAgent true
        expression { params.DEPLOY }
      }
      steps {
        sh 'ansible --version'
        withCredentials([
          usernamePassword(credentialsId: "${REGISTRY_CREDS_ID}", usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_PASSWORD')
          ]) {
          ansiblePlaybook(
            colorized: true,
            credentialsId: "${ANSIBLE_CREDS_ID}",
            vaultCredentialsId: "${ANSIBLE_VAULT_CREDS_ID}",
            playbook: "${ANSIBLE_PLAYBOOK}",
            extras: "${params.ANSIBLE_EXTRAS} --syntax-check"
          )
          ansiblePlaybook(
            colorized: true,
            credentialsId: "${ANSIBLE_CREDS_ID}",
            vaultCredentialsId: "${ANSIBLE_VAULT_CREDS_ID}",
            playbook: "${ANSIBLE_PLAYBOOK}",
            extras: "${params.ANSIBLE_EXTRAS}"
          )
        }
      }
    }
  }

  post {
    always {
      emailext(
        to: '$DEFAULT_RECIPIENTS',
        subject: '$DEFAULT_SUBJECT',
        body: '$DEFAULT_CONTENT'
      )
    }
  }
}
