# Desabilitar advertencia de Symlink porque hace el output extenso
$env:HF_HUB_DISABLE_SYMLINKS_WARNING="1"


# Precargar modelos de IA
py -c "from transformers import pipeline; pipeline('translation', model='Helsinki-NLP/opus-mt-es-en'); pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-offensive')"

# Iniciar PixAda
py manage.py runserver
