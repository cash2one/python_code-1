create_build_dir:
  file.directory:
    - name: "/home/qa/deployment/buildtest"
    - user: qa
    - group: qa
    - makedirs: True

sync_script:
  file.recurse:
    - name: "/home/qa/deployment/buildtest"
    - source: salt://packages/script/{{ projectname }}
    - user: qa
    - file_mode: '0755'
