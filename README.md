# Requirements
1. Have docker installed
2. 
# Starting The Project
1. Run nodeodm docker container
```bash
docker run -it -d -p 3000:3000 --name nodeodm opendronemap/nodeodm --network host
```
2. Run application docker container
```bash
docker-compose up -d
```
3. Troubleshooting
    If you are using Linux/Ubuntu and running docker need sudo access, please refere to any tutorial to register your curretn user as part of docker usergroup
