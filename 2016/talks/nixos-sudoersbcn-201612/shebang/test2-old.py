#! /usr/bin/env nix-shell
#! nix-shell -i python2 -p python27 python27Packages.requests2
#! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs-channels/archive/nixos-14.12.tar.gz
import test
