node {
  env.REGISTRY = 'registry.home.devmem.ru'
  env.IMAGE_NAME = 'soft'
  env.DOCKERFILE = './.docker/django/Dockerfile'
  env.ANSIBLE_IMAGE = 'cytopia/ansible:latest-infra'
  env.ANSIBLE_CONFIG = '.ansible/ansible.cfg'
  env.ANSIBLE_PLAYBOOK = '.ansible/playbook.yml'
  env.ANSIBLE_INVENTORY = '.ansible/hosts'
  env.ANSIBLE_CREDENTIALS_ID = 'jenkins-ssh-key'
  env.ANSIBLE_VAULT_CREDENTIALS_ID = 'ansible-vault-password'

  stage('Checkout') {
    def scmVars = checkout scm

    env.GIT_COMMIT = scmVars.GIT_COMMIT.take(7)
  }

  stage('Build') {
    // Build image
    docker.withRegistry("https://${env.REGISTRY}") {
      env.DOCKER_BUILDKIT = 1
      env.CACHE_FROM = "${env.REGISTRY}/${env.IMAGE_NAME}:latest"

      def myImage = docker.build("${env.IMAGE_NAME}:${env.GIT_COMMIT}", "--progress=plain --cache-from ${env.CACHE_FROM} -f ${env.DOCKERFILE} .")
      myImage.push()
      myImage.push('latest')
      // Untag and remove image by sha256 id
      sh "docker rmi -f \$(docker inspect -f '{{ .Id }}' ${myImage.id})"
    }
  }

  stage('Deploy') {
    docker.image("${env.ANSIBLE_IMAGE}").inside {
      sh 'ansible --version'
      ansiblePlaybook(
        playbook: "${env.ANSIBLE_PLAYBOOK}",
        inventory: "${env.ANSIBLE_INVENTORY}",
        credentialsId: "${env.ANSIBLE_CREDENTIALS_ID}",
        vaultCredentialsId: "${env.ANSIBLE_VAULT_CREDENTIALS_ID}",
        colorized: true)
    }
  }
}
