#!/bin/bash
if [ -e "../../../python_embeded/python" ]; then
    echo Custom Python build of ComfyUI standalone executable detected:
    echo "$(readlink -f "../../python_embeded/python")"
    echo --------------------------------------------------
    ../../../python_embeded/python changeRestore.py ${1:+"$1"} #One-liner is za bezt
else
    echo "Custom Python not found. Use system's Python executable instead:"
    echo "$(which python)"
    echo --------------------------------------------------
    python.exe changeRestore.py ${1:+"$1"}
fi