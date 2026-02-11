FROM mcr.microsoft.com/devcontainers/ruby:1.0.3-3-bookworm
# See URL for a list https://hub.docker.com/r/microsoft/devcontainers-ruby

# Refresh expired Yarn GPG key
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo gpg --dearmor -o /usr/share/keyrings/yarnkey.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

# Install aspell for spell checking
RUN sudo apt-get update -y
RUN sudo apt-get -y install python3-pip pipx aspell aspell-en locales nodejs npm

RUN pip3 install sentence-transformers --break-system-packages 

# Configure aspell on the system
RUN echo "en_US UTF-8" | sudo tee -a /etc/locale.gen
RUN sudo locale-gen en_US.UTF-8

# Install Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code
