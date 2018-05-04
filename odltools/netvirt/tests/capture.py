import sys
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from contextlib import contextmanager


@contextmanager
def capture(command=None, *args, **kwargs):
    out = sys.stdout
    sys.stdout = StringIO()
    try:
        command(*args, **kwargs)
        sys.stdout.seek(0)
        yield sys.stdout.read()
    finally:
        sys.stdout = out
