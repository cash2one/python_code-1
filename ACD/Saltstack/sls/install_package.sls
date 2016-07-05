{% set package_dir = pillar['package_dir'] %}
{% set package_filename = pillar['package_filename'] %}
{% set user = 'qa' %}
{% set group = 'qa' %}
{% set source_dir = 'salt://packages/base_package' %}

"sync {{ package_filename }}":
  file.managed:    
    - name: "/home/qa/deployment/packages/{{ package_filename }}"
    - source: {{ source_dir }}/{{ package_filename }}
    - user: {{ user }}
    - group: {{ group }}
    - mode: 640


"unzip_{{ package_filename }}":
  cmd.run:
    - name: "tar -zxvf /home/qa/deployment/packages/{{ package_filename }} -C {{ package_dir }} 1>/dev/null "
    - cwd: "/home/qa/deployment/packages/"
    - user: {{ user }}
