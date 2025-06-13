# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2023 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pylint: disable=unused-import

"""This module provides the Kraken Futures clients"""

from kraken.base_api import FuturesAsyncClient
from kraken.futures.funding import Funding
from kraken.futures.market import Market
from kraken.futures.trade import Trade
from kraken.futures.user import User
from kraken.futures.ws_client import FuturesWSClient

__all__ = [
    "Funding",
    "FuturesAsyncClient",
    "FuturesWSClient",
    "Market",
    "Trade",
    "User",
]
