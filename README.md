Reproduce the bug of gevent's monkey_patch breaking multiprocess.
```
pip install gevent

python run.py  # success
python run.py break  # fail due to the bug
```
