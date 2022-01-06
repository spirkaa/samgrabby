node {
  env.REGISTRY = 'registry.home.devmem.ru'
  env.IMAGE_NAME = 'soft'
  env.DOCKERFILE = './.docker/django/Dockerfile'
  env.ANSIBLE_IMAGE = 'cytopia/ansible:latest-infra'

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
    env.ANSIBLE_CONFIG = '.ansible/ansible.cfg'

    docker.image("${env.ANSIBLE_IMAGE}").inside {
      sh 'ansible --version'
      ansiblePlaybook(
        playbook: '.ansible/playbook.yml',
        inventory: '.ansible/hosts',
        credentialsId: 'jenkins-ssh-key',
        vaultCredentialsId: 'ansible-vault-password',
        colorized: true)
    }
  }
}
