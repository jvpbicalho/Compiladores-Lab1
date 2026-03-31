#!/bin/bash

while true; do
    read -r linha
    linha=$(echo "$linha" | tr -d ' \t\r')
    echo "[SCANNER] Linha recebida: '$linha'"

done

