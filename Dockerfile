FROM python:3.11-bookworm

RUN  \
    pip install --upgrade pip && \
    pip install pytest tabulate pyparsing lark ruff jupyterlab pandas numpy matplotlib scipy openpyxl && \
    wget -O /tmp/ifcopenshell_python.zip https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-311-v0.8.0-9de173d-linux64.zip && \
    mkdir -p ~/.local/lib/python3.11/site-packages && \
    unzip -d ~/.local/lib/python3.11/site-packages /tmp/ifcopenshell_python.zip

RUN mkdir /app
WORKDIR /app

CMD [ "/bin/bash"]