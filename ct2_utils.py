import ctranslate2
import yaml
import platform

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
        self._update_supported_quantizations_in_config("cpu", cpu_quantizations)

        if self.has_cuda_device():
            cuda_quantizations = self.get_supported_quantizations_cuda()
            self._update_supported_quantizations_in_config("cuda", cuda_quantizations)

    def _update_supported_quantizations_in_config(self, device, quantizations):
        try:
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
        except FileNotFoundError:
            config = {}

        if "supported_quantizations" not in config:
            config["supported_quantizations"] = {}

        config["supported_quantizations"][device] = quantizations

        with open("config.yaml", "w") as f:
            yaml.safe_dump(config, f, default_style="'")
        
        # print(f"Updated {device} quantizations in config.yaml to: {quantizations}")
