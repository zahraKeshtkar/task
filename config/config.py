import yaml

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open('config.yaml', 'r') as file:
                cls._instance.config = yaml.safe_load(file)
        return cls._instance

    def get_config(self):
        return self.config


