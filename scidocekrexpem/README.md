# Sci-Docker-ExpeM

## Why?

Tiziano told me to ease all the possible stuff. I am not good at that after all!

## How?

 ```sh
git clone https://github.com/edoardoramalli/SciExpeM_API.git
cd SciExpeM_API/scidocekrexpem
docker build --platform=linux/amd64 -t sciexpem sciexpem:latest -f Dockerfile .
docker run -it --platform=linux/amd64 --name sciexpem --rm -h sciexpem sciexpem/sciexpem:latest
 ```
