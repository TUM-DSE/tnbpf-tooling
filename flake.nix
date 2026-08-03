{
    description = "Flake for TNBPF Tooling";

    inputs = {
    	nixpkgs.url = "github:NixOS/nixpkgs/26.05";
	systems.url = "github:nix-systems/default";
	utils = {
		url = "github:numtide/flake-utils";
		inputs.systems.follows = "systems";
	};
    };

    outputs =
    {
      self,
      nixpkgs,
      utils,
      ...
    }: utils.lib.eachDefaultSystem (
	system:
	let
	pkgs = import nixpkgs {
          inherit system;
        };
	pythonWithPkgs = pkgs.python3.withPackages (python-pkgs: with python-pkgs; [
		# add packages here if needed
	]);
        in
	{
	  devShells.default = pkgs.mkShell {
		packages = [
			pkgs.binutils
			pythonWithPkgs
		];
		shellHook = ''
			export VENV_DIR="$PWD/.venv"
			if [ ! -d "$VENV_DIR" ]; then
				${pythonWithPkgs}/bin/python -m venv $VENV_DIR
			fi
			source $VENV_DIR/activate
		'';
	  };
	  # https://stackoverflow.com/a/79879457
	  
	}
    );
}
