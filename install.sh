#!/bin/bash -i

conda create -n GloDyNE python=3.7 -y
conda activate GloDyNE

pip install -r pre-requirements.txt
pip install -r requirements.txt