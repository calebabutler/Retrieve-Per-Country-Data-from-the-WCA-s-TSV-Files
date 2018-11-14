#!/usr/bin/env python3
import urllib.request
url = "http://www.worldcubeassociation.org/results/misc/WCA_export.tsv.zip"
urllib.request.urlretrieve(url, "WCA_export.tsv.zip")
