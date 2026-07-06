{
    description = "Flake for TNBPF Tooling";

    inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/25.11";
    unstable.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    };

    outputs =
    {
      self,
      nixpkgs,
      unstable,
      ...
    }@inputs: {
        let
          pkgs = import nixpkgs {
            system = "x86_64-linux";
          };
          unstablePkgs = import unstable {
            system = "x86_64-linux";
          };
        in
        {
          devShell = pkgs.mkShell rec {
            name = "tnbpf dev env";
            packages = with pkgs; [
              # Development Tools
              python3
              binutils
            ];
          };
        }
      }
}