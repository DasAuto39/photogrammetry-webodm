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
    docker-compose up -d
    ```

# ODM Options
To experiment with combinations of ODM options, you can edit file run_odm.sh
| Option Name | Alternative / Supported Values | Description |
| :--- | :--- | :--- |
| **`feature-quality`** | `"ultra"`, `"highest"`, `"high"`, `"medium"`, `"low"`, `"lowest"` | Image feature detection quality level. |
| **`min-num-features`** | Positive integer (Default: `10000`, e.g., `4000`, `8000`, `16000`) | Minimum number of keypoints to extract per image. |
| **`matcher-type`** | `"flann"`, `"bruteforce"`, `"bow"` | The algorithm used for matching features between images. |
| **`mesh-octree-depth`** | Integer from `1` to `14` (Default: `9`) | Density and detail level of the 3D mesh structure. |
| **`mesh-size`** | Positive integer (e.g., `100000`, `200000`, `400000`) | Maximum vertex/polygon count limit for the mesh. |
| **`use-3dmesh`** | `true`, `false` | Enables or disables the generation of a 3D mesh model. |
| **`pc-quality`** | `"ultra"`, `"high"`, `"medium"`, `"low"`, `"lowest"` | Point cloud density and generation quality. |
| **`ignore-gsd`** | `true`, `false` | Bypasses the default GSD limit to process photos at full resolution. |
| **`bg-removal`** | `true`, `false` | Automatically detects and removes sky/horizon backgrounds. |
