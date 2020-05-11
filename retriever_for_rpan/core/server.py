#  Retriever For RPAN - Unofficial streaming utility for the Reddit Public Access Network
#  Copyright (C) 2020 warpspeedchic
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module defines a server which runs the Flask app on localhost, so it can interpret reddit's callbacks.
"""
from typing import Optional

import psutil
from waitress import serve

from core.flaskapp import app


def get_port_blocker_name() -> Optional[str]:
    """
    Looks through system-wide connections to see if the required port is taken.
    If it is, it returns the name of the process that's using the port

    :return: process name
    """
    for connection in psutil.net_connections():
        if connection.laddr.port == 65010:
            process = psutil.Process(connection.pid)
            return process.name()
    return None


def run():
    """
    Starts a waitress server on localhost.
    """
    serve(app, host='0.0.0.0', port=65010, _quiet=True)
