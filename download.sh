#!/bin/bash

set -e
set -x

docker login --username '$oauthtoken' --password $NGC_CLI_API_KEY nvcr.io
echo "Logged in to NGC registry"

echo "Pulling bionemo_esmfold_nim:24.03.01"
docker pull nvcr.io/nvidia/nim/bionemo_esmfold_nim:24.03.01
echo "Pulled bionemo_esmfold_nim:24.03.01"

echo "Downloading weights and models for ESMFold"
mkdir -p esmfold-nim/{weights,models}
ngc registry model download-version nvidia/nim/bionemo-esmfold:protein-folding_noarchx1_bf16_24.03 --dest esmfold-nim/models/
curl -L https://dl.fbaipublicfiles.com/fair-esm/models/esmfold_3B_v1.pt --output esmfold-nim/weights/esmfold_3B_v1.pt
curl -L https://dl.fbaipublicfiles.com/fair-esm/models/esm2_t36_3B_UR50D.pt --output esmfold-nim/weights/esm2_t36_3B_UR50D.pt
curl -L https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t36_3B_UR50D-contact-regression.pt --output esmfold-nim/weights/esm2_t36_3B_UR50D-contact-regression.pt
echo "Downloaded weights and models for ESMFold"


echo "Pulling bionemo_diffdock_nim:24.03.04"
docker pull nvcr.io/nvidia/nim/bionemo_diffdock_nim:24.03.04
echo "Pulled bionemo_diffdock_nim:24.03.04"

echo "Downloading weights and models for DiffDock"
ngc registry model download-version "nvidia/nim/bionemo-diffdock:molecular-docking_noarchx1_fp32_24.03.04"
echo "Downloaded weights and models for DiffDock"


echo "Installing some additional Ubuntu packages"
sudo apt-get update
sudo apt-get install -y openbabel
echo "Installed openbabel"

echo "All Done!"