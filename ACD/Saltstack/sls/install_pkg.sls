{% set pkg_name = pillar['pkg_name'] %}
mypkgs:
  pkg.installed:
    - pkgs:
      - {{ pkg_name }}
