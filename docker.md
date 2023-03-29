# Docker

It is a container engine that uses the Linux Kernel features like namespaces and control groups to create containers on top of an operating system. So you can call it OS-level virtualization.

## Container vs Image

A Docker image is a snapshot of the file system and application dependencies. It is an executable package of software that includes everything needed like application code, libraries, tools, dependencies, and other files to run an application.

A Docker container is a running instance of a Docker image. 

The key difference between a Docker image and a container is the writable layer on top of the image. This means, if you have five containers running from an image, all the containers share the same read-only layers from the image and only the top writable layer is different for all five containers.

This means, when you delete the container, the writable layer gets deleted.

## Core architecture

Docker engine is composed of the docker demon, an API interface and Docker CLI. Docker daemon (dockerd runs continuously as `dockerd`) systemd services. Its responsible for building the docker image.

To manage image and run containers, `dockerd` calls the `docker-containerd` APIs. `containerd` is another system daemon services that is responsible for downloding the images anr unning them as containers. It exposes its API to recive instructions from the `dockerd` services.

`runc` is the container runtime responsible for creating the namespaces and cgroups requiere for a container. It then runs the containers command inside thoes namespaces. 

## Difference between Docker engine & Docker daemon?

Docker engine is compose of the docker daemon, rest interface and the docker CLI. The daemon is the systemd dockerd service responsible for building the docker images and sending docker instruccions to containerd runtime.

The daemon recives the commands from the docker cliente through CLI or REST API. 

## Difference between containerd & runc?

containerd is responsible fro managing the containers and runc is responsible fro running the containers Icreate namespace, cgroupos and run commands inside the containers with the inputs of containerd.

## How to reduce image size?

### Minimal base images
 
By minimizing the number of layers in the image, it can help to reduce image size. Additionally, using Alpine Linux as a base image can further reduce the image size, as it includes only the necessary packages. The process involves identifying the essential dependencies for the application and creating a new image using the minimal base image and only the necessary dependencies. Finally, the resulting image can be optimized further by removing unnecessary files and packages.

### Multistage builds

The process involves creating two stages: a build stage and a runtime stage. The build stage compiles the code and generates an executable, while the runtime stage uses the executable to run the application. By separating the build and runtime environments, it is possible to use a minimal base image for the runtime stage, reducing the overall image size. Additionally, any unnecessary files and dependencies can be removed in the final stage, further reducing the image size. This method is particularly useful for applications with large dependencies or build tools that are not needed at runtime.

### Minimize the Number of Layers

By minimizing the number of layers, it can help to reduce image size and improve performance. The process involves consolidating commands into a single layer where possible, using multi-line commands, and reducing the use of intermediate containers. Additionally, using a tool like Docker Squash can further reduce the number of layers by merging multiple layers into a single layer. 

By minimizing the number of layers, it is possible to create smaller and more efficient images, which can improve deployment speed and reduce storage costs.

### Understanding cache

Docker caches intermediate layers during the build process, which can significantly speed up subsequent builds. However, it's essential to ensure that only the necessary steps are being cached. By structuring the Dockerfile in a way that takes advantage of caching, it's possible to avoid unnecessary builds and reduce build time. 

Due to this concept, it’s recommended to add the lines which are used for installing dependencies & packages earlier inside the Dockerfile – before the COPY commands.

For example, by placing frequently changed instructions at the end of the Dockerfile, it's possible to cache more of the earlier layers. Additionally, using the --no-cache option when building the image can force Docker to rebuild all layers, which can be useful when changes are made to the earlier layers. 

By understanding Docker's caching mechanism and structuring the Dockerfile appropriately, it's possible to significantly reduce build time and create smaller images.

