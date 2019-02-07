pipeline {
    agent none
    environment {
        DOCKER_REPO = "pyouroboros/ouroboros"
        GIT_REPO = 'pyouroboros/ouroboros'
        VERSION_FILE = "pyouroboros/__init__.py"
        FLAKE_FILES = "ouroboros *.py pyouroboros/*.py"
        TAG = ""
        GIT_TOKEN = credentials('github-jenkins-token')
        PYPI_CREDS = credentials('pypi-creds-dirtycajunrice')
    }
    stages {
        stage('Flake8 + Run Once') {
            agent { label 'amd64'}
            steps {
                sh """
                    python3 -m venv venv && venv/bin/pip install flake8 && venv/bin/python -m flake8 --max-line-length 120 ${FLAKE_FILES}
                    venv/bin/python -m pip install -r requirements.txt && venv/bin/python ouroboros --log-level debug --run-once
                    rm -rf venv/
                """
                script {
                    TAG = sh(returnStdout: true, script: 'grep -i version ${VERSION_FILE} | cut -d" " -f3 | tr -d \\"').trim()
                }
            }
        }
        stage('Docker Builds') {
            when {
                anyOf {
                    branch 'master'
                    branch 'develop'
                }
            }
            parallel {
                stage('amd64') {
                    agent { label 'amd64'}
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                def image = docker.build("${DOCKER_REPO}:${TAG}-amd64")
                                image.push()
                                
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${DOCKER_REPO}:develop-amd64")
                                image.push()
                            }
                        }
                    }
                }
                stage('ARMv6') {
                    agent { label 'arm64'}
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                def image = docker.build("${DOCKER_REPO}:${TAG}-arm", "-f Dockerfile.arm .")
                                image.push()
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${DOCKER_REPO}:develop-arm", "-f Dockerfile.arm .")
                                image.push()
                            }
                        }
                    }
                }
                stage('ARM64v8') {
                    agent { label 'arm64'}
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                def image = docker.build("${DOCKER_REPO}:${TAG}-arm64", "-f Dockerfile.arm64 .")
                                image.push()
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${DOCKER_REPO}:develop-arm64", "-f Dockerfile.arm64 .")
                                image.push()
                            }
                        }
                    }
                }
            }
        }
        stage('Releases') {
            when {
                anyOf {
                    branch 'master'
                    branch 'develop'
                }
            }
            parallel {
                stage('Docker Manifest') {
                    agent { label 'amd64'}
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                sh(script: """
                                    docker manifest create ${DOCKER_REPO}:${TAG} ${DOCKER_REPO}:${TAG}-amd64 ${DOCKER_REPO}:${TAG}-arm64 ${DOCKER_REPO}:${TAG}-arm
                                    docker manifest inspect ${DOCKER_REPO}:${TAG}
                                    docker manifest push -p ${DOCKER_REPO}:${TAG}
                                    docker manifest create ${DOCKER_REPO}:latest ${DOCKER_REPO}:${TAG}-amd64 ${DOCKER_REPO}:${TAG}-arm64 ${DOCKER_REPO}:${TAG}-arm
                                    docker manifest inspect ${DOCKER_REPO}:latest
                                    docker manifest push -p ${DOCKER_REPO}:latest
                                    """
                                )
                            } else if (BRANCH_NAME == 'develop') {
                                sh(script: """
                                    docker manifest create ${DOCKER_REPO}:develop ${DOCKER_REPO}:develop-amd64 ${DOCKER_REPO}:develop-arm64 ${DOCKER_REPO}:develop-arm
                                    docker manifest inspect ${DOCKER_REPO}:develop
                                    docker manifest push -p ${DOCKER_REPO}:develop
                                    """
                            }
                        }
                    }
                }
                stage('GitHub') {
                    when { branch 'master' }
                    agent { label 'amd64'}
                    steps {
                        sh """
                            git remote set-url origin "https://${GIT_TOKEN_USR}:${GIT_TOKEN_PSW}@github.com/${GIT_REPO}.git" 
                            git tag ${TAG}
                            git push --tags
                        """
                    }
                }
                stage('PyPi') {
                    when { branch 'master' }
                    agent { label 'amd64'}
                    steps {
                        sh """
                            python3 -m venv venv && venv/bin/pip install twine
                            venv/bin/python setup.py sdist && venv/bin/python -m twine --skip-existing -u ${PYPI_CREDS_USR} -p ${PYPI_CREDS_PSW} upload dist/*
                            git tag ${TAG}
                            git push --tags
                        """
                    }
                }
            }
        }
    }
}
