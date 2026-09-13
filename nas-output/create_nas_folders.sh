#!/bin/bash

set -e

############################################################
# NVR NAS FOLDER CREATION SCRIPT
# Generated automatically from nvr.xlsx
############################################################


############################################################
# CLUSTER      : clnvrm000
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm000
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000'


############################################################
# RESOURCE GROUP : clnvrm001
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm001/clnvrm001_p04'


############################################################
# RESOURCE GROUP : clnvrm002
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm002/clnvrm002_p04'


############################################################
# RESOURCE GROUP : clnvrm003
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm003/clnvrm003_p04'


############################################################
# RESOURCE GROUP : clnvrm004
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm004/clnvrm004_p04'


############################################################
# RESOURCE GROUP : clnvrm005
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm005/clnvrm005_p04'


############################################################
# RESOURCE GROUP : clnvrm006
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm006/clnvrm006_p04'


############################################################
# RESOURCE GROUP : clnvrm007
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm000/clnvrm007/clnvrm007_p04'


############################################################
# CLUSTER      : clnvrm010
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm010
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010'


############################################################
# RESOURCE GROUP : clnvrm011
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm011/clnvrm011_p04'


############################################################
# RESOURCE GROUP : clnvrm012
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm012/clnvrm012_p04'


############################################################
# RESOURCE GROUP : clnvrm013
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm013/clnvrm013_p04'


############################################################
# RESOURCE GROUP : clnvrm014
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm014/clnvrm014_p04'


############################################################
# RESOURCE GROUP : clnvrm015
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm015/clnvrm015_p04'


############################################################
# RESOURCE GROUP : clnvrm016
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm016/clnvrm016_p04'


############################################################
# RESOURCE GROUP : clnvrm017
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm010/clnvrm017/clnvrm017_p04'


############################################################
# CLUSTER      : clnvrm020
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm020
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020'


############################################################
# RESOURCE GROUP : clnvrm021
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm021/clnvrm021_p04'


############################################################
# RESOURCE GROUP : clnvrm022
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm022/clnvrm022_p04'


############################################################
# RESOURCE GROUP : clnvrm023
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm023/clnvrm023_p04'


############################################################
# RESOURCE GROUP : clnvrm024
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm024/clnvrm024_p04'


############################################################
# RESOURCE GROUP : clnvrm025
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm025/clnvrm025_p04'


############################################################
# RESOURCE GROUP : clnvrm026
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm026/clnvrm026_p04'


############################################################
# RESOURCE GROUP : clnvrm027
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm020/clnvrm027/clnvrm027_p04'


############################################################
# CLUSTER      : clnvrm030
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm030
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030'


############################################################
# RESOURCE GROUP : clnvrm031
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm031/clnvrm031_p04'


############################################################
# RESOURCE GROUP : clnvrm032
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm032/clnvrm032_p04'


############################################################
# RESOURCE GROUP : clnvrm033
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm033/clnvrm033_p04'


############################################################
# RESOURCE GROUP : clnvrm034
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm034/clnvrm034_p04'


############################################################
# RESOURCE GROUP : clnvrm035
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm035/clnvrm035_p04'


############################################################
# RESOURCE GROUP : clnvrm036
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm036/clnvrm036_p04'


############################################################
# RESOURCE GROUP : clnvrm037
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm030/clnvrm037/clnvrm037_p04'


############################################################
# CLUSTER      : clnvrm040
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm040
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040'


############################################################
# RESOURCE GROUP : clnvrm041
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm041/clnvrm041_p04'


############################################################
# RESOURCE GROUP : clnvrm042
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm042/clnvrm042_p04'


############################################################
# RESOURCE GROUP : clnvrm043
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm043/clnvrm043_p04'


############################################################
# RESOURCE GROUP : clnvrm044
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm044/clnvrm044_p04'


############################################################
# RESOURCE GROUP : clnvrm045
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm045/clnvrm045_p04'


############################################################
# RESOURCE GROUP : clnvrm046
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm046/clnvrm046_p04'


############################################################
# RESOURCE GROUP : clnvrm047
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm040/clnvrm047/clnvrm047_p04'


############################################################
# CLUSTER      : clnvrm050
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm050
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050'


############################################################
# RESOURCE GROUP : clnvrm051
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm051/clnvrm051_p04'


############################################################
# RESOURCE GROUP : clnvrm052
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm052/clnvrm052_p04'


############################################################
# RESOURCE GROUP : clnvrm053
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm053/clnvrm053_p04'


############################################################
# RESOURCE GROUP : clnvrm054
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm054/clnvrm054_p04'


############################################################
# RESOURCE GROUP : clnvrm055
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm055/clnvrm055_p04'


############################################################
# RESOURCE GROUP : clnvrm056
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm056/clnvrm056_p04'


############################################################
# RESOURCE GROUP : clnvrm057
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm050/clnvrm057/clnvrm057_p04'


############################################################
# CLUSTER      : clnvrm060
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm060
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060'


############################################################
# RESOURCE GROUP : clnvrm061
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm061/clnvrm061_p04'


############################################################
# RESOURCE GROUP : clnvrm062
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm062/clnvrm062_p04'


############################################################
# RESOURCE GROUP : clnvrm063
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm063/clnvrm063_p04'


############################################################
# RESOURCE GROUP : clnvrm064
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm064/clnvrm064_p04'


############################################################
# RESOURCE GROUP : clnvrm065
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm065/clnvrm065_p04'


############################################################
# RESOURCE GROUP : clnvrm066
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm066/clnvrm066_p04'


############################################################
# RESOURCE GROUP : clnvrm067
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm060/clnvrm067/clnvrm067_p04'


############################################################
# CLUSTER      : clnvrm070
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm070
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070'


############################################################
# RESOURCE GROUP : clnvrm071
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm071/clnvrm071_p04'


############################################################
# RESOURCE GROUP : clnvrm072
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm072/clnvrm072_p04'


############################################################
# RESOURCE GROUP : clnvrm073
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm073/clnvrm073_p04'


############################################################
# RESOURCE GROUP : clnvrm074
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm074/clnvrm074_p04'


############################################################
# RESOURCE GROUP : clnvrm075
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm075/clnvrm075_p04'


############################################################
# RESOURCE GROUP : clnvrm076
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm076/clnvrm076_p04'


############################################################
# RESOURCE GROUP : clnvrm077
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm070/clnvrm077/clnvrm077_p04'


############################################################
# CLUSTER      : clnvrm080
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm080
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080'


############################################################
# RESOURCE GROUP : clnvrm081
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm081/clnvrm081_p04'


############################################################
# RESOURCE GROUP : clnvrm082
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm082/clnvrm082_p04'


############################################################
# RESOURCE GROUP : clnvrm083
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm083/clnvrm083_p04'


############################################################
# RESOURCE GROUP : clnvrm084
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm084/clnvrm084_p04'


############################################################
# RESOURCE GROUP : clnvrm085
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm085/clnvrm085_p04'


############################################################
# RESOURCE GROUP : clnvrm086
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm086/clnvrm086_p04'


############################################################
# RESOURCE GROUP : clnvrm087
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm080/clnvrm087/clnvrm087_p04'


############################################################
# CLUSTER      : clnvrm090
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm090
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090'


############################################################
# RESOURCE GROUP : clnvrm091
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm091/clnvrm091_p04'


############################################################
# RESOURCE GROUP : clnvrm092
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm092/clnvrm092_p04'


############################################################
# RESOURCE GROUP : clnvrm093
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm093/clnvrm093_p04'


############################################################
# RESOURCE GROUP : clnvrm094
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm094/clnvrm094_p04'


############################################################
# RESOURCE GROUP : clnvrm095
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm095/clnvrm095_p04'


############################################################
# RESOURCE GROUP : clnvrm096
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm096/clnvrm096_p04'


############################################################
# RESOURCE GROUP : clnvrm097
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm090/clnvrm097/clnvrm097_p04'


############################################################
# CLUSTER      : clnvrm100
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm100
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100'


############################################################
# RESOURCE GROUP : clnvrm101
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p04'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p05'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p05'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p06'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p06'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p07'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p07'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p08'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p08'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p09'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p09'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p10'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p10'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p11'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p11'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p12'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p12'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p13'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p13'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p14'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p14'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p15'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p15'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p16'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p16'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p17'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p17'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p18'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p18'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p19'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p19'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p20'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p20'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p21'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p21'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p22'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p22'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p23'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p23'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p24'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p24'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p25'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p25'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p26'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p26'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p27'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p27'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p28'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm100/clnvrm101/clnvrm101_p28'


############################################################
# CLUSTER      : clnvrm110
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm110
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110'


############################################################
# RESOURCE GROUP : clnvrm111
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p04'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p05'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p05'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p06'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p06'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p07'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p07'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p08'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p08'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p09'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p09'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p10'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p10'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p11'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p11'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p12'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p12'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p13'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p13'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p14'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p14'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p15'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p15'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p16'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p16'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p17'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p17'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p18'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p18'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p19'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p19'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p20'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p20'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p21'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p21'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p22'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p22'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p23'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p23'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p24'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p24'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p25'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p25'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p26'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p26'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p27'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p27'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p28'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm110/clnvrm111/clnvrm111_p28'


############################################################
# CLUSTER      : clnvrm120
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm120
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120'


############################################################
# RESOURCE GROUP : clnvrm121
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p04'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p05'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p05'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p06'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p06'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p07'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p07'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p08'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p08'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p09'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p09'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p10'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p10'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p11'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p11'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p12'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p12'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p13'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p13'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p14'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p14'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p15'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p15'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p16'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p16'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p17'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p17'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p18'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p18'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p19'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p19'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p20'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p20'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p21'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p21'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p22'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p22'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p23'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p23'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p24'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p24'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p25'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p25'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p26'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p26'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p27'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p27'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p28'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm120/clnvrm121/clnvrm121_p28'


############################################################
# CLUSTER      : clnvrm130
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001mp/mtr-rec/clnvrm130
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130'


############################################################
# RESOURCE GROUP : clnvrm131
# PATH           : /ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131
############################################################

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131'
chown recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131'

# Core mount point folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/app'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/app'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/data'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/data'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/log'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/log'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p01'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p01'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p02'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p02'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p03'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p03'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p04'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p04'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p05'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p05'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p06'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p06'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p07'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p07'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p08'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p08'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p09'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p09'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p10'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p10'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p11'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p11'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p12'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p12'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p13'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p13'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p14'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p14'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p15'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p15'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p16'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p16'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p17'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p17'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p18'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p18'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p19'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p19'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p20'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p20'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p21'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p21'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p22'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p22'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p23'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p23'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p24'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p24'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p25'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p25'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p26'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p26'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p27'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p27'

mkdir -p '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p28'
chown -R recorder:recorder '/ifs/infstonas001mp/mtr-rec/clnvrm130/clnvrm131/clnvrm131_p28'


############################################################
# CLUSTER      : clnvrr100
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr100
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100'


############################################################
# RESOURCE GROUP : clnvrr101
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p04'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p05'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p05'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p06'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p06'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p07'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p07'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p08'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p08'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p09'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p09'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p10'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p10'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p11'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p11'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p12'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p12'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p13'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p13'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p14'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p14'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p15'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p15'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p16'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p16'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p17'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p17'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p18'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p18'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p19'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p19'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p20'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p20'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p21'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p21'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p22'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p22'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p23'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p23'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p24'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p24'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p25'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p25'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p26'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p26'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p27'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p27'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p28'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr100/clnvrr101/clnvrr101_p28'


############################################################
# CLUSTER      : clnvrr110
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr110
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110'


############################################################
# RESOURCE GROUP : clnvrr111
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p04'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p05'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p05'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p06'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p06'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p07'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p07'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p08'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p08'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p09'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p09'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p10'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p10'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p11'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p11'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p12'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p12'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p13'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p13'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p14'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p14'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p15'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p15'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p16'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p16'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p17'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p17'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p18'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p18'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p19'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p19'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p20'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p20'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p21'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p21'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p22'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p22'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p23'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p23'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p24'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p24'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p25'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p25'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p26'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p26'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p27'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p27'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p28'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr110/clnvrr111/clnvrr111_p28'


############################################################
# CLUSTER      : clnvrr120
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr120
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120'


############################################################
# RESOURCE GROUP : clnvrr121
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p04'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p05'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p05'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p06'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p06'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p07'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p07'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p08'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p08'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p09'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p09'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p10'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p10'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p11'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p11'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p12'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p12'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p13'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p13'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p14'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p14'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p15'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p15'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p16'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p16'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p17'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p17'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p18'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p18'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p19'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p19'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p20'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p20'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p21'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p21'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p22'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p22'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p23'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p23'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p24'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p24'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p25'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p25'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p26'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p26'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p27'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p27'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p28'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr120/clnvrr121/clnvrr121_p28'


############################################################
# CLUSTER      : clnvrr130
# CLUSTER TYPE : 1+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr130
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130'


############################################################
# RESOURCE GROUP : clnvrr131
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p04'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p05'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p05'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p06'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p06'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p07'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p07'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p08'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p08'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p09'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p09'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p10'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p10'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p11'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p11'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p12'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p12'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p13'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p13'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p14'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p14'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p15'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p15'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p16'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p16'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p17'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p17'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p18'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p18'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p19'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p19'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p20'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p20'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p21'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p21'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p22'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p22'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p23'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p23'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p24'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p24'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p25'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p25'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p26'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p26'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p27'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p27'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p28'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr130/clnvrr131/clnvrr131_p28'


############################################################
# CLUSTER      : clnvrr000
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr000
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000'


############################################################
# RESOURCE GROUP : clnvrr001
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr001/clnvrr001_p04'


############################################################
# RESOURCE GROUP : clnvrr002
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr002/clnvrr002_p04'


############################################################
# RESOURCE GROUP : clnvrr003
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr003/clnvrr003_p04'


############################################################
# RESOURCE GROUP : clnvrr004
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr004/clnvrr004_p04'


############################################################
# RESOURCE GROUP : clnvrr005
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr005/clnvrr005_p04'


############################################################
# RESOURCE GROUP : clnvrr006
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr006/clnvrr006_p04'


############################################################
# RESOURCE GROUP : clnvrr007
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr000/clnvrr007/clnvrr007_p04'


############################################################
# CLUSTER      : clnvrr010
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr010
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010'


############################################################
# RESOURCE GROUP : clnvrr011
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr011/clnvrr011_p04'


############################################################
# RESOURCE GROUP : clnvrr012
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr012/clnvrr012_p04'


############################################################
# RESOURCE GROUP : clnvrr013
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr013/clnvrr013_p04'


############################################################
# RESOURCE GROUP : clnvrr014
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr014/clnvrr014_p04'


############################################################
# RESOURCE GROUP : clnvrr015
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr015/clnvrr015_p04'


############################################################
# RESOURCE GROUP : clnvrr016
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr016/clnvrr016_p04'


############################################################
# RESOURCE GROUP : clnvrr017
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr010/clnvrr017/clnvrr017_p04'


############################################################
# CLUSTER      : clnvrr020
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr020
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020'


############################################################
# RESOURCE GROUP : clnvrr021
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr021/clnvrr021_p04'


############################################################
# RESOURCE GROUP : clnvrr022
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr022/clnvrr022_p04'


############################################################
# RESOURCE GROUP : clnvrr023
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr023/clnvrr023_p04'


############################################################
# RESOURCE GROUP : clnvrr024
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr024/clnvrr024_p04'


############################################################
# RESOURCE GROUP : clnvrr025
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr025/clnvrr025_p04'


############################################################
# RESOURCE GROUP : clnvrr026
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr026/clnvrr026_p04'


############################################################
# RESOURCE GROUP : clnvrr027
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr020/clnvrr027/clnvrr027_p04'


############################################################
# CLUSTER      : clnvrr030
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr030
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030'


############################################################
# RESOURCE GROUP : clnvrr031
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr031/clnvrr031_p04'


############################################################
# RESOURCE GROUP : clnvrr032
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr032/clnvrr032_p04'


############################################################
# RESOURCE GROUP : clnvrr033
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr033/clnvrr033_p04'


############################################################
# RESOURCE GROUP : clnvrr034
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr034/clnvrr034_p04'


############################################################
# RESOURCE GROUP : clnvrr035
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr035/clnvrr035_p04'


############################################################
# RESOURCE GROUP : clnvrr036
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr036/clnvrr036_p04'


############################################################
# RESOURCE GROUP : clnvrr037
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr030/clnvrr037/clnvrr037_p04'


############################################################
# CLUSTER      : clnvrr040
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr040
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040'


############################################################
# RESOURCE GROUP : clnvrr041
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr041/clnvrr041_p04'


############################################################
# RESOURCE GROUP : clnvrr042
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr042/clnvrr042_p04'


############################################################
# RESOURCE GROUP : clnvrr043
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr043/clnvrr043_p04'


############################################################
# RESOURCE GROUP : clnvrr044
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr044/clnvrr044_p04'


############################################################
# RESOURCE GROUP : clnvrr045
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr045/clnvrr045_p04'


############################################################
# RESOURCE GROUP : clnvrr046
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr046/clnvrr046_p04'


############################################################
# RESOURCE GROUP : clnvrr047
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr040/clnvrr047/clnvrr047_p04'


############################################################
# CLUSTER      : clnvrr050
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr050
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050'


############################################################
# RESOURCE GROUP : clnvrr051
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr051/clnvrr051_p04'


############################################################
# RESOURCE GROUP : clnvrr052
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr052/clnvrr052_p04'


############################################################
# RESOURCE GROUP : clnvrr053
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr053/clnvrr053_p04'


############################################################
# RESOURCE GROUP : clnvrr054
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr054/clnvrr054_p04'


############################################################
# RESOURCE GROUP : clnvrr055
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr055/clnvrr055_p04'


############################################################
# RESOURCE GROUP : clnvrr056
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr056/clnvrr056_p04'


############################################################
# RESOURCE GROUP : clnvrr057
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr050/clnvrr057/clnvrr057_p04'


############################################################
# CLUSTER      : clnvrr060
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr060
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060'


############################################################
# RESOURCE GROUP : clnvrr061
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr061/clnvrr061_p04'


############################################################
# RESOURCE GROUP : clnvrr062
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr062/clnvrr062_p04'


############################################################
# RESOURCE GROUP : clnvrr063
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr063/clnvrr063_p04'


############################################################
# RESOURCE GROUP : clnvrr064
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr064/clnvrr064_p04'


############################################################
# RESOURCE GROUP : clnvrr065
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr065/clnvrr065_p04'


############################################################
# RESOURCE GROUP : clnvrr066
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr066/clnvrr066_p04'


############################################################
# RESOURCE GROUP : clnvrr067
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr060/clnvrr067/clnvrr067_p04'


############################################################
# CLUSTER      : clnvrr070
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr070
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070'


############################################################
# RESOURCE GROUP : clnvrr071
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr071/clnvrr071_p04'


############################################################
# RESOURCE GROUP : clnvrr072
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr072/clnvrr072_p04'


############################################################
# RESOURCE GROUP : clnvrr073
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr073/clnvrr073_p04'


############################################################
# RESOURCE GROUP : clnvrr074
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr074/clnvrr074_p04'


############################################################
# RESOURCE GROUP : clnvrr075
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr075/clnvrr075_p04'


############################################################
# RESOURCE GROUP : clnvrr076
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr076/clnvrr076_p04'


############################################################
# RESOURCE GROUP : clnvrr077
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr070/clnvrr077/clnvrr077_p04'


############################################################
# CLUSTER      : clnvrr080
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr080
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080'


############################################################
# RESOURCE GROUP : clnvrr081
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr081/clnvrr081_p04'


############################################################
# RESOURCE GROUP : clnvrr082
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr082/clnvrr082_p04'


############################################################
# RESOURCE GROUP : clnvrr083
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr083/clnvrr083_p04'


############################################################
# RESOURCE GROUP : clnvrr084
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr084/clnvrr084_p04'


############################################################
# RESOURCE GROUP : clnvrr085
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr085/clnvrr085_p04'


############################################################
# RESOURCE GROUP : clnvrr086
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr086/clnvrr086_p04'


############################################################
# RESOURCE GROUP : clnvrr087
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr080/clnvrr087/clnvrr087_p04'


############################################################
# CLUSTER      : clnvrr090
# CLUSTER TYPE : 7+1
# NAS ROOT     : /ifs/infstonas001rp/rtr-rec/clnvrr090
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090'


############################################################
# RESOURCE GROUP : clnvrr091
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr091/clnvrr091_p04'


############################################################
# RESOURCE GROUP : clnvrr092
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr092/clnvrr092_p04'


############################################################
# RESOURCE GROUP : clnvrr093
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr093/clnvrr093_p04'


############################################################
# RESOURCE GROUP : clnvrr094
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr094/clnvrr094_p04'


############################################################
# RESOURCE GROUP : clnvrr095
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr095/clnvrr095_p04'


############################################################
# RESOURCE GROUP : clnvrr096
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr096/clnvrr096_p04'


############################################################
# RESOURCE GROUP : clnvrr097
# PATH           : /ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097
############################################################

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097'
chown recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097'

# Core mount point folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/app'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/app'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/data'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/data'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/log'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/log'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/etc/picata'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/etc/picata'

# Picata service folders

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p01'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p01'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p02'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p02'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p03'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p03'

mkdir -p '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p04'
chown -R recorder:recorder '/ifs/infstonas001rp/rtr-rec/clnvrr090/clnvrr097/clnvrr097_p04'


############################################################
# NAS FOLDER CREATION COMPLETE
############################################################

