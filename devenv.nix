{ pkgs, lib, config, ... }:

{
  # Project name
  name = "readitnow";

  # Enable Python language support
  languages.python = {
    enable = true;
    version = "3.11";
  };

  # Add required system packages
  packages = with pkgs; [
    # Development and utility tools
    git
    # Python packages will be managed separately through pip or other methods
  ];

  # Scripts for common development tasks
  scripts = {
    # Run the ReadItNow application
    "readitnow" = {
      exec = ''
        python src/readitnow/main.py "$@"
      '';
    };
    
    # Development mode - runs with debug flags
    "readitnow-dev" = {
      exec = ''
        python -u src/readitnow/main.py "$@"
      '';
    };

    # Install Python dependencies
    "install-deps" = {
      exec = ''
        pip install textual rich pyyaml python-frontmatter
      '';
    };
  };

  # Environment variables
  env = {
    # Add any environment variables needed
    PYTHONPATH = "${config.env.DEVENV_ROOT}/src";
  };
} 