#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
from os import path
env.hosts = ['54.210.197.7', '54.237.45.180']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not path.exists(archive_path):
        return False
    try:
        filename = path.basename(archive_path)
        no_ext, _ = path.splitext(filename)
        remote_dir = '/data/web_static/releases/'
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(remote_dir, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(filename, remote_dir, no_ext))
        run('rm /tmp/{}'.format(filename))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(remote_dir, no_ext))
        run('rm -rf {}{}/web_static'.format(remote_dir, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(remote_dir, no_ext))
        return True
    except Exception as e:
        print(e)
        return False
