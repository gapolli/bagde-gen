#!/usr/bin/env bash

chmod +x badge_gen.sh

echo "====== 🧪 PASSO 1: Inspecionando variáveis locais ======"
./badge_gen.sh env-check

echo -e "\n====== 📄 PASSO 2: Inserindo e Centralizando Badges ======"
./badge_gen.sh top "license" "tech Python 3.12" "tech Deploy passing success"

echo -e "\n====== 📊 PASSO 3: Rodando a suíte de validação do pytest ======"
./badge_gen.sh test
