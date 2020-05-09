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

from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))
CONFIG_DIR = path.join(ROOT_DIR, 'config.yml')
GUI_RESOURCES_DIR = path.join(ROOT_DIR, 'data/')
