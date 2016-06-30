{% set start_service = pillar['start_service'] %}
{% set dir = '/home/qa/deployment/script' %}
{% set user = 'qa' %}
  
"rum_cmd":
  cmd.run:
    - name: "/home/qa/deployment/script/{{ start_service }} restart "
    - cwd: {{ dir }}/
    - user: {{ user }}
