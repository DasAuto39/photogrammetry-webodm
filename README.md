# Requirements
Have docker installed

# Quickstart
1. Run nodeodm docker container
    ```bash
    docker run -it -d -p 3000:3000 --name nodeodm opendronemap/nodeodm --network host
    ```
2. Run application docker container
    ```bash
    docker run -d --name robot-perception --network host -v ./datasets:/app/datasets -v ./output:/app/output ghcr.io/anisamsrh/persepsi-robot:latest
    ```
3. Quick Troubleshooting : \
    If you are using Linux/Ubuntu and running docker need sudo access, please refere to any tutorial to register your curret user as part of docker usergroup

# Advance Usage (CLI)
1. Make Robot UR take pictures
    ```bash
    python3 ur.py
    ```

2. Do ODM on specific folder of dataset
    ```bash
    ./run_odm.sh datasets/
    ```

3. Build the docker image yourself
    ```bash
    docker-compose up -d --build
    ```
    and run it
    ```bash
    docker-compose up -d --build
    ```