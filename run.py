# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2013 Daniel Lombraña González
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa. If not, see <http://www.gnu.org/licenses/>.
from pybossa.core import create_app

if __name__ == "__main__":  # pragma: no cover
    app = create_app()
    #logging.basicConfig(level=logging.NOTSET)
    app.run(host=app.config['HOST'], port=app.config['PORT'],
            debug=app.config.get('DEBUG', True))
else:
    app = create_app()
