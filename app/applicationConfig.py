##read from appConfig.txt
config_file_path = 'appConfig.txt'

def read_from_config(file_path):
    appConfig = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            appConfig[key.strip()] = value.strip().strip('"')
    return appConfig

app_config = read_from_config(config_file_path)
