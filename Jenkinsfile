node {
  env.REGISTRY = 'git.devmem.ru'
  env.REGISTRY_CREDS_ID = 'gitea-user'
  env.IMAGE_OWNER = 'cr'
  env.IMAGE_NAME = 'soft'
  env.DOCKERFILE = './.docker/django/Dockerfile'
  env.LABEL_AUTHORS = 'Ilya Pavlov <piv@devmem.ru>'
  env.LABEL_TITLE = 'soft'
  env.LABEL_DESCRIPTION = 'Grab your favorite software from SamLab.ws'
  env.LABEL_URL = 'https://soft.devmem.ru'
  env.LABEL_CREATED = sh(script: "date '+%Y-%m-%dT%H:%M:%S%:z'", returnStdout: true).toString().trim()

  env.ANSIBLE_IMAGE = 'git.devmem.ru/cr/ansible:latest'
  env.ANSIBLE_CONFIG = '.ansible/ansible.cfg'
  env.ANSIBLE_PLAYBOOK = '.ansible/playbook.yml'
  env.ANSIBLE_INVENTORY = '.ansible/hosts'
  env.ANSIBLE_CREDS_ID = 'jenkins-ssh-key'
  env.ANSIBLE_VAULT_CREDS_ID = 'ansible-vault-password'

  properties([
    buildDiscarder(
      logRotator(
        daysToKeepStr: '60',
        numToKeepStr: '10'
      )
    )
  ])

  stage('Checkout') {
    def scmVars = checkout scm

    env.GIT_COMMIT = scmVars.GIT_COMMIT.take(7)
    env.GIT_URL = scmVars.GIT_URL.toString().trim()
  }

  stage('Build') {
    // Build image
    docker.withRegistry("https://${env.REGISTRY}", "${env.REGISTRY_CREDS_ID}") {
      env.DOCKER_BUILDKIT = 1
      env.CACHE_FROM = "${env.REGISTRY}/${env.IMAGE_OWNER}/${env.IMAGE_NAME}:latest"

      def myImage = docker.build(
        "${env.IMAGE_OWNER}/${env.IMAGE_NAME}:${env.GIT_COMMIT}",
        "--label \"org.opencontainers.image.created=${env.LABEL_CREATED}\" \
        --label \"org.opencontainers.image.authors=${env.LABEL_AUTHORS}\" \
        --label \"org.opencontainers.image.url=${env.LABEL_URL}\" \
        --label \"org.opencontainers.image.source=${env.GIT_URL}\" \
        --label \"org.opencontainers.image.version=${env.GIT_COMMIT}\" \
        --label \"org.opencontainers.image.revision=${env.GIT_COMMIT}\" \
        --label \"org.opencontainers.image.title=${env.LABEL_TITLE}\" \
        --label \"org.opencontainers.image.description=${env.LABEL_DESCRIPTION}\" \
        --progress=plain \
        --cache-from ${env.CACHE_FROM} \
        -f ${env.DOCKERFILE} ."
      )
      myImage.push()
      myImage.push('latest')
      // Untag and remove image by sha256 id
      sh "docker rmi -f \$(docker inspect -f '{{ .Id }}' ${myImage.id})"
    }
  }

  stage('Deploy') {
    docker.withRegistry("https://${env.REGISTRY}", "${env.REGISTRY_CREDS_ID}") {
      image = docker.image("${env.ANSIBLE_IMAGE}")
      image.pull()
      image.inside {
        sh 'ansible --version'
        withCredentials([usernamePassword(credentialsId: "${env.REGISTRY_CREDS_ID}", usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_PASSWORD')]) {
          ansiblePlaybook(
            colorized: true,
            playbook: "${env.ANSIBLE_PLAYBOOK}",
            inventory: "${env.ANSIBLE_INVENTORY}",
            credentialsId: "${env.ANSIBLE_CREDS_ID}",
            vaultCredentialsId: "${env.ANSIBLE_VAULT_CREDS_ID}"
          )
        }
      }
    }
  }
}
