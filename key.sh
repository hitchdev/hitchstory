#!/bin/bash
set -e
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

hitchrun() {
    podman run --privileged -it --rm \
        -v $PROJECT_DIR:/src \
        -v hitchstory-hitch-container:/gen \
        -v ~/.ssh/id_rsa:/root/.ssh/id_rsa \
        -v ~/.ssh/id_rsa.pub:/root/.ssh/id_rsa.pub \
        -p 5555:5555 \
        --workdir /src \
        hitchstory-hitch \
        $1
}


case "$1" in
    "clean")
        if podman volume exists hitchstory-hitch-container; then
            podman volume rm hitchstory-hitch-container
        fi
        if podman image exists hitchstory-hitch; then
            podman image rm -f hitchstory-hitch
        fi
        ;;
    "make")
        echo "building ci container..."
        if ! podman volume exists hitchstory-hitch-container; then
            podman volume create hitchstory-hitch-container
        fi
        podman build -f hitch/Dockerfile-hitch -t hitchstory-hitch $PROJECT_DIR
        ;;
    "bash")
        hitchrun "bash"
        ;;
    "--help")
        echo "Commands:"
        echo "./run.sh make     - build docker containers."
        ;;
    *)
        hitchrun "/venv/bin/python hitch/key.py $1 $2 $3 $4 $5 $6 $7 $8 $9"
        ;; 
esac

exit
