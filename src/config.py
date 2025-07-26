from pathlib import Path
import yaml

APP_NAME = "readitnow"
CONFIG_DIR = Path.home() / ".config" / APP_NAME
CONFIG_FILE = CONFIG_DIR / "config.yaml"
CACHE_DIR = Path.home() / ".cache" / APP_NAME

DEFAULT_CONFIG = {
    'vault_path': str(Path.home() / "vault" / "ReadItLater Inbox"),
    'max_notes': 20,
    'excerpt_lines': 5,
    'keybindings': {
        'open_link': "enter",
        'open_file': "shift+enter",
        'up': "up",
        'down': "down",
        'left': "left",
        'right': "right",
        'page_up': "pageup",
        'page_down': "pagedown",
        'quit': "q",
    },
    'thumbnail_cache': str(CACHE_DIR / "thumbnails"),
}

def load_or_create_config() -> dict:
    """
    Loads configuration from the user's config directory.
    If no config file is found, it creates one with default values.
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    if not CONFIG_FILE.is_file():
        print(f"Configuration file not found. Creating a default one at: {CONFIG_FILE}")
        with open(CONFIG_FILE, 'w') as f:
            yaml.dump(DEFAULT_CONFIG, f, default_flow_style=False, sort_keys=False)

    with open(CONFIG_FILE, 'r') as f:
        config_data = yaml.safe_load(f)

    # Ensure thumbnail cache dir exists, creating it if necessary
    thumbnail_cache_path = Path(config_data.get('thumbnail_cache', DEFAULT_CONFIG['thumbnail_cache']))
    thumbnail_cache_path.mkdir(parents=True, exist_ok=True)
    config_data['thumbnail_cache'] = str(thumbnail_cache_path)

    # Ensure vault_path is expanded
    config_data['vault_path'] = str(Path(config_data['vault_path']).expanduser())

    return config_data 