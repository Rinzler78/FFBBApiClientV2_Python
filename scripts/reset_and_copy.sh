#!/bin/bash

# Reset hard le dossier src (toutes les modifications non commit seront perdues)
echo "Deleting all files in src/"
rm -rf src/*

echo "Checking out src/"
git checkout -- src

# Copie les fichiers de .tmp/ dans src/ffbb_api_client_v2/models
echo "Copying files from .tmp/ to src/ffbb_api_client_v2/models/"
cp .tmp/* src/ffbb_api_client_v2/models/

echo "Reset and copy completed."
