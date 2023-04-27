{
  description = "A basic flake with a shell";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      devShell = pkgs.mkShell {
        nativeBuildInputs = with pkgs; [ 
          python310
          python310Packages.beautifulsoup4
          python310Packages.python-dotenv
          python310Packages.pillow
          python310Packages.discordpy 
          python310Packages.pytesseract
        ];
        buildInputs = [ ];
      };
    });
}
