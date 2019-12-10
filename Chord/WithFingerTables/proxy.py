#!usr/bin/env python
# -*- coding: utf-8 -*-
import zmq
import os
import subprocess
import uuid
import string
import random
import hashlib
import sys

ctx = zmq.Context()
s = ctx.socket(zmq.REP)
s.bind("tcp://*:6060")
