FROM mcr.microsoft.com/devcontainers/ruby:0-2.7

# Install aspell for spell checking
RUN sudo apt-get update -y && sudo apt-get -y install aspell aspell-en locales
RUN echo "en_US UTF-8" | sudo tee -a /etc/locale.gen
RUN sudo locale-gen en_US.UTF-8
