FROM mcr.microsoft.com/devcontainers/ruby:1.0.3-3-bookworm
# See URL for a list https://hub.docker.com/r/microsoft/devcontainers-ruby

# Install aspell for spell checking
RUN sudo apt-get update -y && sudo apt-get -y install aspell aspell-en locales
RUN echo "en_US UTF-8" | sudo tee -a /etc/locale.gen
RUN sudo locale-gen en_US.UTF-8
