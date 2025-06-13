full_install_libs = [
    "pyside6==6.8.2.1"
]

priority_libs = {
    "cp311": {
        "GPU": [
            "https://download.pytorch.org/whl/cu126/torch-2.6.0%2Bcu126-cp311-cp311-win_amd64.whl#sha256=5ddca43b81c64df8ce0c59260566e648ee46b2622ab6a718e38dea3c0ca059a1",
            "nvidia-cuda-runtime-cu12==12.6.77",
            "nvidia-cublas-cu12==12.6.4.1",
            "nvidia-cuda-nvrtc-cu12==12.6.77",
            "nvidia-cuda-nvcc-cu12==12.6.77",
            "nvidia-cudnn-cu12==9.5.1.17",
        ],
        "CPU": [
            "https://download.pytorch.org/whl/cpu/torch-2.6.0%2Bcpu-cp311-cp311-win_amd64.whl#sha256=24c9d3d13b9ea769dd7bd5c11cfa1fc463fd7391397156565484565ca685d908"
        ]
    },
    "cp312": {
        "GPU": [
            "https://download.pytorch.org/whl/cu126/torch-2.6.0%2Bcu126-cp312-cp312-win_amd64.whl#sha256=b10c39c83e5d1afd639b5c9f5683b351e97e41390a93f59c59187004a9949924",
            "nvidia-cuda-runtime-cu12==12.6.77",
            "nvidia-cublas-cu12==12.6.4.1",
            "nvidia-cuda-nvrtc-cu12==12.6.77",
            "nvidia-cuda-nvcc-cu12==12.6.77",
            "nvidia-cudnn-cu12==9.5.1.17",

        ],
        "CPU": [
            "https://download.pytorch.org/whl/cpu/torch-2.6.0%2Bcpu-cp312-cp312-win_amd64.whl#sha256=4027d982eb2781c93825ab9527f17fbbb12dbabf422298e4b954be60016f87d8"
        ]
    }
}

libs = [
    "av==14.1.0",
    "certifi==2025.01.31",
    "cffi==1.17.1",
    "charset-normalizer==3.4.1",
    "colorama==0.4.6",
    "coloredlogs==15.0.1",
    "ctranslate2==4.5.0",
    "faster-whisper==1.1.1",
    "filelock==3.17.0",
    "flatbuffers==25.2.10",
    "fsspec==2025.2.0",
    "huggingface-hub==0.28.1",
    "humanfriendly==10.0",
    "idna==3.10",
    "mpmath==1.3.0",
    "nltk==3.9.1",
    "numpy==1.26.4",
    "onnxruntime==1.20.1",
    "packaging==24.2",
    "protobuf==5.29.3",
    "psutil==6.1.1",
    "pycparser==2.22",
    "pyinstaller==6.11.1",
    "pyreadline3==3.5.4",
    "PyYAML==6.0.2",
    "regex==2024.11.6",
    "requests==2.32.3",
    "sounddevice==0.5.1",
    "sympy==1.13.1",
    "tokenizers==0.21.0",
    "tqdm==4.67.1",
    "typing_extensions==4.12.2",
    "urllib3==2.3.0",
]
