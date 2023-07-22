#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# GitHub: https://github.com/btschwertfeger
#

"""
Module that provides an example usage for the KrakenSpotWebsocketClient.
It uses the Kraken Websocket API v2.

todo: implement this example
"""

from __future__ import annotations

# import asyncio
import logging
import logging.config

# import os
# import time
# from typing import Union

# from kraken.spot import KrakenSpotWSClientV2

logging.basicConfig(
    format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
    datefmt="%Y/%m/%d %H:%M:%S",
    level=logging.INFO,
)
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
