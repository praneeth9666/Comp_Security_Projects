FROM ubuntu:20.04

# tzdata tries to start a conversation on apt install, tell it no
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y curl tar build-essential python3 sudo gcc-multilib gdb libcap2-bin

# Make user ubuntu
RUN useradd -m -s /bin/bash -G sudo ubuntu && echo 'ubuntu ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

# Set the default user to 'ubuntu'
USER ubuntu

# Set the working directory
WORKDIR /home/ubuntu

# Build with:
#docker build -t project4 .

# Run with:
# docker run --privileged -it -v ./:/home/ubuntu/project4 project4
