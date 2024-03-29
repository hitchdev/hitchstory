#!/bin/bash
set -e
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_NAME=$(cat $PROJECT_DIR/hitch/PROJECT_NAME | tr -d '\n')
if [ -z "$PROJECT_NAME" ]; then
    echo "PROJECT_NAME file must be set with project name."
    exit 1
fi
FOLDER_HASH=$(echo $PROJECT_DIR | md5sum | cut -c 1-5)
GEN_VOLUME_NAME=hitch-vol-${PROJECT_NAME}-${FOLDER_HASH}
IMAGE_NAME=hitch-${FOLDER_HASH}-${PROJECT_NAME}

hitchrun() {
    podman run --privileged -it --rm \
        --network host \
        -v $PROJECT_DIR:/src \
        -v $GEN_VOLUME_NAME:/gen \
        -e STORYMODE=$STORYMODE \
        --workdir /src \
        $IMAGE_NAME \
        $1
}


case "$1" in
    "clean")
        case "$2" in
            "all")
                if podman image exists $IMAGE_NAME; then
                    podman image rm -f $IMAGE_NAME
                fi
                if podman volume exists $GEN_VOLUME_NAME; then
                    podman volume rm -f $GEN_VOLUME_NAME
                fi
                ;;
            "gen")
                if podman volume exists $GEN_VOLUME_NAME; then
                    podman volume rm -f $GEN_VOLUME_NAME
                fi
                podman volume create $GEN_VOLUME_NAME
                ;;
            "dbcache")
                hitchrun "find /gen -name datacache-*.tar -delete"
                ;;
            "compose")
                hitchrun "podman-compose -f hitch/podman-compose.yml down --remove-orphans"
                ;;
            "prune")
                hitchrun "podman system prune --all"
                ;;
            *)
                echo "Invalid clean target. ./run.sh clean [all]"
                exit 1
                ;;
        esac
        ;;
    "make")
        case "$2" in
            "")
                echo "building ci container..."
                if ! podman volume exists $GEN_VOLUME_NAME; then
                    podman volume create $GEN_VOLUME_NAME
                fi
                podman build -f hitch/Dockerfile-hitch -t $IMAGE_NAME $PROJECT_DIR
                hitchrun "virtualenv --python=python3 /gen/venv"
                hitchrun "/gen/venv/bin/pip install setuptools-rust"
                hitchrun "/gen/venv/bin/pip install -r /src/hitch/hitchreqs.txt"
                hitchrun "podman-compose -f hitch/podman-compose.yml build"
                ;;
            "compose")
                hitchrun "podman-compose -f hitch/podman-compose.yml build $3"
                ;;
            "hitchreqs")
                hitchrun "/gen/venv/bin/pip-compile hitch/hitchreqs.in -o hitch/hitchreqs.txt"
                ;;
            *)
                echo "Invalid make target. ./run.sh make [compose|hitchreqs]"
                exit 1
                ;;
            esac
        ;;
    "kill"):
        podman stop --latest -t 1
        ;;
    "pytest")
        hitchrun "/gen/venv/bin/pytest $2 $3 $4 $5 $6 $7 $8 $9"
        ;;
    "docgen")
        hitchrun "/gen/venv/bin/python hitch/docgen.py"
        ;;
    "bash")
        hitchrun "bash"
        ;;
    "bdd")
        hitchrun "/gen/venv/bin/python hitch/cli.py bdd $2 $3 $4 $5 $6 $7 $8 $9"
        ;;
    "rbdd")
        hitchrun "/gen/venv/bin/python hitch/cli.py rbdd $2 $3 $4 $5 $6 $7 $8 $9"
        ;;
    "vbdd")
        hitchrun "/gen/venv/bin/python hitch/cli.py vbdd $2 $3 $4 $5 $6 $7 $8 $9"
        ;;
    "regression")
        hitchrun "/gen/venv/bin/python hitch/cli.py regression"
        ;;
    "docdb")
        hitchrun "/gen/venv/bin/python hitch/cli.py docdb"
        ;;
    *)
        hitchrun "$1 $2 $3 $4 $5 $6 $7 $8 $9"
        ;; 
esac

exit
