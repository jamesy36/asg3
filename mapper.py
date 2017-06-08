#!/usr/bin/env python3
import sys
from socket import * 
import time
import select


def mapper(file, offset, size):