import os

import numpy as np

from analysis import DATABASES, MODELS

# force all warnings to be errors
np.seterr(all='raise')

# read from env.
required_successes = os.getenv('REQUIRED_SUCCESSES')
database = os.getenv('DATABASE')
model = os.getenv('MODEL')

if required_successes is None or database is None or model is None:
    available_databases = '\n\t'.join(DATABASES.keys())
    available_models = '\n\t'.join(MODELS.keys())
    message = 'Available databases:\n\t%s\nAvailable models:\n\t%s' % \
              (available_databases, available_models)

    print(message)
    print("INFO: to run this file, you must set environment variables MODEL, REQUIRED_SUCCESSES, and DATABASE. "
          "For example,\n"
          "\tDATABASE=brazil_aids_2010 MODEL=LogNormalAnalysis REQUIRED_SUCCESSES=8 python -m analysis_run")
    print("\tAvailable models and analysis are listed above.")
    exit(1)

required_successes = int(required_successes)

Model = MODELS[model]
if database not in DATABASES:
    raise IndexError('Database "%s" is invalid.' % database)

print('Running analysis for model "%s" on database "%s" for "%d" successes.' %
      (database, model, required_successes))

# run the analysis
Model(database, required_successes=required_successes)
