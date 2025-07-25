{ pkgs, config, ... }:

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
    python311Packages.textual
    python311Packages.rich
    python311Packages.pyyaml
    python311Packages.python-frontmatter
  ];

  # Scripts for common development tasks
  scripts = {
    # Run the ReadItNow application
    "readitnow" = {
      exec = ''
        python src/main.py "$@"
      '';
    };
    
    # Development mode - runs with debug flags
    "readitnow-dev" = {
      exec = ''
        python -u src/main.py "$@"
      '';
    };
  };

  # Environment variables
  env = {
    # Add any environment variables needed
    PYTHONPATH = "${config.env.DEVENV_ROOT}/src";
  };
} 