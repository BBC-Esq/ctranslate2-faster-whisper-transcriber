import ctranslate2
import yaml

class CheckQuantizationSupport:
    def has_cuda_device(self):
        cuda_device_count = ctranslate2.get_cuda_device_count()
        return cuda_device_count > 0

    def get_supported_quantizations_cuda(self):
        cuda_quantizations = ctranslate2.get_supported_compute_types("cuda")
        return [q for q in cuda_quantizations if q != 'int16']

    def get_supported_quantizations_cpu(self):
        cpu_quantizations = ctranslate2.get_supported_compute_types("cpu")
        return [q for q in cpu_quantizations if q != 'int16']

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
        
        print(f"Updated {device} quantizations in config.yaml to: {quantizations}")

if __name__ == "__main__":
    quantization_checker = CheckQuantizationSupport()
    quantization_checker.update_supported_quantizations()
