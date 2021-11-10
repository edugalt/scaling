import os

from analysis import DATABASES, MODELS

# read from env.
required_successes = int(os.getenv('REQUIRED_SUCCESSES', 8))

database = os.getenv('DATASET', 'new_dataset') ###
model = os.getenv('MODEL')

if database == 'new_dataset':
    print('NOTE: dataset should be added to `new_dataset/generic_dataset.txt`.')
    print('NOTE: If you change the dataset after running the analysis, you must remove the '
          'corresponding results `_results/*new_dataset*` or the returned values are of the old dataset.')
'''    
if database == 'covid19':
    print('NOTE: dataset should be added to `covid19/covid19.txt`.')
    print('NOTE: If you change the dataset after running the analysis, you must remove the '
          'corresponding results `_results/*new_dataset*` or the returned values are of the old dataset.') 
'''
# Number of samples for bootstrap (default: 0 do not compute errors)
samples = int(os.getenv('ERROR_SAMPLES', 0))
if samples == 0:
    print('NOTE: Not running bootstrap. Use "ERROR_SAMPLES=10" to run bootstrap with 10 samples')

available_models = ['%s: \'%s\'' % (MODELS[model_].description, model_) for model_ in MODELS.keys()]
available_models = '\n  '.join(available_models)

if model is None:
    message = 'ERROR: MODEL must be an environment variable with one of the available models:\n  %s' % available_models
    message += '\n Example: MODEL=LogNormalAnalysis python -m analyze'
    print(message)
    print('Exiting...')
    exit(0)

if model not in MODELS:
    raise IndexError('MODEL "%s" invalid.\nAvailable models:\n  %s' % (model, available_models))
Model = MODELS[model]
Model.samples = samples

if database not in DATABASES:
    raise IndexError('Dataset "%s" is invalid.' % database)

print('Running analysis for model "%s" on dataset "%s" for "%d" successes.' %
      (model, database, required_successes))

# run the analysis
analysis = Model(database, required_successes=required_successes)

print('beta = %f' % analysis.beta[0])
if analysis.beta[1] is not None:
    print('bootstrap error = %f' % analysis.beta[1])
print('p_value = %f' % analysis.p_value)
print('BIC = %f' % analysis.bic)
