mkdir -p raw_images
data/PENDING_LAB_NAMES.txt | wget -r -N -c -np -nH --cut-dirs=4 -P raw_images --user adviksh --ask-password -i - --base=https://physionet.org/files/mimic-cxr-jpg/2.1.0/