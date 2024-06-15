FROM python:3.11-bookworm

RUN  \
    pip install --upgrade pip && \
    pip install pytest tabulate pyparsing lark ruff jupyterlab pandas numpy matplotlib scipy openpyxl ipykernel && \
    wget -O /tmp/ifcopenshell_python.zip https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-311-v0.8.0-90ae709-linux64.zip && \
    mkdir -p ~/.local/lib/python3.11/site-packages && \
    unzip -d ~/.local/lib/python3.11/site-packages /tmp/ifcopenshell_python.zip

# OpenCascade Dependencies and python wrapper
RUN \ 
    apt-get update && \
    apt-get install -y libglu1-mesa-dev libgl1-mesa-dev libxmu-dev libxi-dev \
    libocct-data-exchange-dev \
    libocct-draw-dev \ 
    libocct-foundation-dev \
    libocct-modeling-algorithms-dev \ 
    libocct-modeling-data-dev \
    libocct-ocaf-dev \
    libocct-visualization-dev 

RUN pip install cadquery

RUN pip install jupytercad

RUN mkdir -p ~/.local/lib/python3.11/site-packages/OCC && \
    touch ~/.local/lib/python3.11/site-packages/OCC/__init__.py && \
    ln -s /usr/local/lib/python3.11/site-packages/OCP ~/.local/lib/python3.11/site-packages/OCC/Core

RUN mkdir /app
WORKDIR /app

CMD [ "/bin/bash"]