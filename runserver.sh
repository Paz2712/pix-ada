set -e

# Desabilitar advertencia de Symlink porque hace el output extenso
export HF_HUB_DISABLE_SYMLINKS_WARNING=1

# Precargar modelos de IA
python - << 'EOF'
from transformers import pipeline
pipeline('translation', model='Helsinki-NLP/opus-mt-es-en')
pipeline('text-classification', model='cardiffnlp/twitter-roberta-base-offensive')
EOF

# Iniciar PixAda
python manage.py runserver
