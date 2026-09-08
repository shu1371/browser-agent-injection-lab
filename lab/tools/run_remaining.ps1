[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$lab = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $lab
$env:PYTHONIOENCODING = 'utf-8'
python experiments.py init
python experiments.py attack 8
python experiments.py defense_label 8
python experiments.py defense_policy 8
