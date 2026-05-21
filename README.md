# Starting The Project
1. Run nodeodm docker container
```bash
docker run -it -p 3000:3000 opendronemap/nodeodm
```
2. Run application docker container
```bash
```
3. Troubleshooting
    If you are using Linux/Ubuntu and running docker need suso access, please refere to any tutorial to register your curretn user as part of docker usergroup

# How The Docker Container of The App Works?
1. Creating python 3.10 env
2. Installing requirements.txt
3. Running ui/app.py