import argparse
from create_experiment import create_experiment
import json
import os
import sys
import copy
# Python program to print all paths from a source to destination.

parser = argparse.ArgumentParser()

parser.add_argument("-epath", "--experiments_path",
                    help="path of the directory where experiment folder locates")
parser.add_argument("-cfg", "--config_file",
                    help="config file for creating experiments")

args = parser.parse_args()

if not os.path.isfile(args.config_file):
    print("Config file does not exist")
    sys.exit(0)

with open(args.config_file) as json_file:
    config = json.load(json_file)

experiments_path = args.experiments_path
prefix = config['experiments_prefix']

del config['experiments_path'], config['experiments_prefix']

keys = list(config.keys())

paths = []
path = dict(config)
def traverse_config(data, pathLen):
    global path
    path[keys[pathLen]] = data

    if (pathLen == len(keys)-1):
        paths.append(path)
        path = dict(path)
        return


    pathLen+=1

    for i in config[keys[pathLen]]:
        traverse_config(i, pathLen)


traverse_config(config['data_path'][0], 0)

if not os.path.isdir(experiments_path):
    os.makedirs(experiments_path)

if args.config_file != os.path.join(experiments_path,'exp.json'):
    with open(args.config_file) as json_file:
        f = open(os.path.join(experiments_path,'exp.json'), 'w')
        for line in json_file.readlines():
            f.write(line)
        f.close()


from create_experiment import create_experiment
i = 0
for cfg in paths:
    cfg['experiment_path'] = os.path.join(experiments_path,
                                          prefix+'_'+str(i))
    if not os.path.isdir(cfg['experiment_path']):
        os.makedirs(cfg['experiment_path'])

    create_experiment(cfg)

    i += 1