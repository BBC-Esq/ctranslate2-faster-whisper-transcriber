import ctranslate2
import yaml
import platform
import os
import sys

def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False) and relative_path == "config.yaml":
        return os.path.join(os.path.dirname(sys.executable), relative_path)
    elif hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class CheckQuantizationSupport:

    excluded_types = ['int16', 'int8', 'int8_float32', 'int8_float16', 'int8_bfloat16']

    def has_cuda_device(self):
        cuda_device_count = ctranslate2.get_cuda_device_count()
        return cuda_device_count > 0

    def get_supported_quantizations_cuda(self):
        cuda_quantizations = ctranslate2.get_supported_compute_types("cuda")
        excluded_types = self.excluded_types
        return [q for q in cuda_quantizations if q not in excluded_types]

    def get_supported_quantizations_cpu(self):
        cpu_quantizations = ctranslate2.get_supported_compute_types("cpu")
        excluded_types = self.excluded_types
        return [q for q in cpu_quantizations if q not in excluded_types]

    def update_supported_quantizations(self):
        cpu_quantizations = self.get_supported_quantizations_cpu()
        # print(f"Found CPU quantizations: {cpu_quantizations}")
        self._update_supported_quantizations_in_config("cpu", cpu_quantizations)

        if self.has_cuda_device():
            cuda_quantizations = self.get_supported_quantizations_cuda()
            # print(f"Found CUDA quantizations: {cuda_quantizations}")
            self._update_supported_quantizations_in_config("cuda", cuda_quantizations)

    def _update_supported_quantizations_in_config(self, device, quantizations):
        config_path = get_resource_path("config.yaml")
        # print(f"Looking for config at: {config_path}")
        
        try:
            with open(config_path, "r") as f:
                config = yaml.safe_load(f) or {}
                # print(f"Loaded config: {config}")
        except FileNotFoundError:
            config = {}
        
        if not isinstance(config, dict):
            config = {}

        if "supported_quantizations" not in config:
            config["supported_quantizations"] = {}

        config["supported_quantizations"][device] = quantizations
        # print(f"Saving config to: {config_path}")
        # print(f"With content: {config}")

        with open(config_path, "w") as f:
            yaml.safe_dump(config, f, default_style="'")
