#!/bin/bash

# Verifica o número de commits no repositório
num_commits=$(git log --pretty=format:"%h" | wc -l)

# Define o número da versão como o número de commits + 1
versao=$((num_commits + 2))

# Realiza o add de todos os arquivos modificados
git add .

# Cria a mensagem de commit com a versão
commit_message="Versão $versao: Atualização automatizada"

# Realiza o commit com a mensagem gerada
git commit -m "$commit_message"

# Cria uma tag com a versão
git tag -a "v0.0$versao" -m "Versão $versao"

# Envia as alterações para o repositório remoto
git push origin main --tags --force

# Exibe uma mensagem de sucesso
echo "Commit realizado com a versão $versao."
