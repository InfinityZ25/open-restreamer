# Open-Restreamer (Python)

ORP, is a free and opensource, self-hosted multicast restreaming service. The main idea is to solve my BIG issue with twitch never giving me quality selection, ergo me just streaming to many platforms at once, but I don't want to pay for anyone else's service to achieve this or settle for free 720p.

# How to use

The easiest way to build and run this project is to build the docker image and run it. You can use the following commands to do so:

```bash
# Build the container
docker build -t jcedeno/open-restreamer:latest .
# Push the container
docker push jcedeno/open-restreamer:latest
```

After that you can run the container with the following command:

```bash

```
## Conda
We use conda to manage our python environment, so you will need to install it first. You can find the installation instructions [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/). Look into this later https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html

# Contribute to the project

There will be some guidelines on how to properly contribute to the project, but for now, just fork the project and open a `PR -> Main` with your feature.

# License
MIT license, I only ask that if you DO in fact use my code, agree to credit all the project contributors. Also, please consider buying us a coffee :).
