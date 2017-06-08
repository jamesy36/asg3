#!/usr/bin/env python3
import sys
from socket import * 
import time
import select

def reducer(groupMed, file):
	#groupMed like group of Medium/intermediate hah
	