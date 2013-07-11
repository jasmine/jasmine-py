from __future__ import absolute_import
import os
import sys

if __name__ == "__main__":
    __package__ = "jasmine.bin"

    sys.path = [os.path.join(os.path.dirname(__file__), '../..')] + sys.path

    from jasmine.ci import CIRunner

    CIRunner().run()