import ctranslate2
import platform
import os
import sys

from config.manager import config_manager
from utils import get_resource_path

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
        config_manager.set_supported_quantizations("cpu", cpu_quantizations)

        if self.has_cuda_device():
            cuda_quantizations = self.get_supported_quantizations_cuda()
            config_manager.set_supported_quantizations("cuda", cuda_quantizations)