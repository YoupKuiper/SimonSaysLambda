import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

'''
Use context to setup env for tests
'''

from dbhandler import dbhandler
from TemplateBuilder import TemplateBuilder
from lambda_function import buildTemplate
