#!/usr/bin/env bash

cd $HOME/server
make docker_build

cd $HOME/fGPT
make docker_build

cd $HOME/transformers-playground
make docker_build

cd $HOME/ollama-webui
docker compose build
