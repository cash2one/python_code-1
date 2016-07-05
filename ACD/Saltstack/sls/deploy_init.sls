{% set _user = 'qa' %}
{% set _group = 'qa' %}


"{{ _user }}_init":
  user.present:
    - name: {{ _user }}
    - gid_from_name: True
    - home: "/home/{{ _user }}"
#    - enforce_password: True
#    - password: '$6$774fe279c64de417$OpHLRCGaSIZpA.fiK1bKs/2zyR/WV/TA0jD3r28Nn376fYsyi4RjEZrs.8Vsdw/1huHftJaG7BrfE7VDBx3US0'
    - order: 1 


create_build_dir:
  file.directory:
    - name: "/home/qa/deployment/build"
    - user: qa
    - group: qa
    - makedirs: True
    - order: 2

create_script_dir:
  file.directory:
    - name: "/home/qa/deployment/script"
    - user: qa
    - group: qa
    - makedirs: True
    - order: 3

create_bak_dir:
  file.directory:
    - name: "/home/qa/deployment/bak"
    - user: qa
    - group: qa
    - makedirs: True
    - order: 4
create_srv_dir:
  file.directory:
    - name: "/srv"
    - user: qa
    - group: qa
    - makedirs: True
    - order: 5



create_srv_logs_dir:
  file.directory:
    - name: "/srv/logs"
    - user: qa
    - group: qa
    - makedirs: True
    - order: 6

create_package_dir:
  file.directory:
    - name: "/home/qa/deployment/package"
    - user: qa
    - group: qa
    - makedirs: True
    - order: 7