@echo off

REM Desabilitar advertencia de Symlink porque hace el output extenso
set HF_HUB_DISABLE_SYMLINKS_WARNING=1

REM Precargar modelos de IA
py -c "from transformers import pipeline; pipeline('translation', model='Helsinki-NLP/opus-mt-es-en'); pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-offensive')"

REM Iniciar PixAda
py manage.py runserver
