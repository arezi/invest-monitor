#!/usr/bin/env python3

from app.webapp import app

import os

if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 4000)))
