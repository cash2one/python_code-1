{% set _user = 'qa' %}
{% set _group = 'qa' %}
{% set salt_dir = 'salt://packages' %}
{% set build_dir = '/home/qa/deployment/build' %}
{% set project_name = pillar['project_name'] %}
{% set log_dir = '/srv/logs' %}

include:
  - sls.deploy_init


sync_common_script:
  file.recurse:
    - name: "/home/qa/deployment/script"
    - source: salt://deploy_script/common
    - user: qa
    - group: qa
    - file_mode: '0755'

sync_script:
  file.recurse:
    - name: "/home/qa/deployment/script"
    - source: salt://deploy_script/{{ project_name }}
    - user: qa
    - group: qa
    - file_mode: '0755'

{% for _module, _fileName in  pillar.get('fileName',{}).items() %}

"rm_{{ _module }}":
  cmd.run:
    - name: "rm -rf /home/qa/deployment/build/{{ _module }}* "
    - cwd: {{ build_dir }}/
    - user: {{ _user }}
    - order: 10

"update {{ _module }}": 
  file.managed: 
    - name: {{ build_dir }}/{{ _fileName }}
    - source: {{ salt_dir }}/{{ project_name }}/{{ _fileName }}
    - user: {{ _user }}
    - group: {{ _group }}
    - mode: 755
    - order: 11 
{% endfor %}

rm_log:
  cmd.run:
    - name: "find . -ctime +7 | xargs rm -rf"
    - cwd: {{ log_dir }}
    - user: {{ _user }}
    - order: 50
