{% set desc_dir = pillar['desc_dir'] %}
{% set log_dir = '/srv/logs' %}
{% set _user = 'qa' %}
{% set _group = 'qa' %}
{% set build_dir = '/home/qa/deployment/build' %}





{% for _module, _fileName in  pillar.get('fileName',{}).items() %}

"unzip_{{ _module }}":
  cmd.run:
    - name: "tar -xzf {{ _fileName }}"
    - cwd: {{ build_dir }}
    - user: {{ _user }}
    - order: 22


"rm_{{ _module }}":
  cmd.run:
    - name: "rm -rf {{ _module  }}"
    - cwd: {{ desc_dir }}
    - user: {{ _user }}
    - order: 23  


"cp_{{ _module }}":
  cmd.run:
    - name: "cp -rf {{ _module }} {{ desc_dir }}"
    - cwd: {{ build_dir }}
    - user: {{ _user }}
    - order: 24
    
{% endfor %}


