PunSSH
------

Git based SSH tunnel concentrator / jump host configuration.

Design
======

* Git repository on jumphost using:
  * [push-to-deploy][1] for tunnel configurations.
  * [post-receive][2] hook which updates ``.ssh/authorized-keys``
* One or more systemd/launchd job on client which:
  1. Receives tunnel configuration directly from jumphost using ``ssh``.
  2. Sets up forward/reverse tunnel restarting it when necessary.

[1](https://github.blog/2015-02-06-git-2-3-has-been-released/#push-to-deploy)
[2](https://git-scm.com/docs/githooks#post-receive)
