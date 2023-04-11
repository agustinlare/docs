#!/bin/bash

find /var/lib/docker/containers -name \*.log -ls | sort -r -n -k7 | head -n 10 | awk '{print $7}'