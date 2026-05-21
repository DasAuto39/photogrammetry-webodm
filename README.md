# Requirements
Have docker installed

# Starting The Project
1. Run nodeodm docker container
```bash
docker run -it -d -p 3000:3000 --name nodeodm opendronemap/nodeodm --network host
```
2. Run application docker container
```bash
docker-compose up -d
```
3. Quick Troubleshooting : \
    If you are using Linux/Ubuntu and running docker need sudo access, please refere to any tutorial to register your curretn user as part of docker usergroup

# Advance Usage (CLI)
1. Make Robot UR take pictures
```bash
python3 ur.py
```

2. Do ODM on specific folder of dataset
```bash
./run_odm.sh datasets/
```
