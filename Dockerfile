FROM    ghcr.io/swaglive/jinja2:3.1.2

COPY    pre-entrypoint.py post-entrypoint.py /usr/local/bin/