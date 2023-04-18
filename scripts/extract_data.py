import os
import numpy as np
import pandas as pd

def readdata(filename : str, delzero = True):
    filedf = pd.read_table(filename, sep='\s+').fillna(0)
    #print(filedf)
    names = filedf.columns
    #filematrix = np.genfromtxt(filename, skip_header=1, filling_values = 0)
    #filematrix = filematrix.T
    #with open(filename,'r') as f:
    #    names = f.readline().split()
    # create dictionary with different data groups
    # {dg1: Dataframe(index=T, specie:[,,,] ...)
    # delete 0 or NaN values in keys --> generate a dataframe and use remove!
    # remove values with same temperature
    # then concatenate
    #print(filematrix, names)
    datagroups_dct = {}
    datagroups_x_dct = {} #dictionary of only x axis, ordered
    dg_N = 0

    for i in np.arange(0, len(names), 2, dtype=int):
        # dataset = pd.DataFrame(filematrix[i+1], index=filematrix[i], columns=[names[i+1]])
        dataset = pd.DataFrame(filedf[names[i+1]].values, index=filedf[names[i]].values, columns=[names[i+1]])
        dataset = dataset.dropna()
        if delzero == True:
            dataset = dataset[dataset.values > 0]
        dataset = dataset[dataset.index > 0]
        if len(dataset.values) == 0:
            continue # go to next cycle
        # average duplicate x values
        for xi in list(dataset.index):
            if len(dataset.loc[xi].shape) > 1: # duplicate values present
                # average
                avg_series = dataset.loc[xi].mean()
                avg_df = pd.DataFrame([avg_series.values], index = [xi], columns = avg_series.index)
                # delete row
                dataset = dataset.drop(xi)
                # dataset = dataset[~dataset.index.duplicated(keep=False)]
                # concatenate new value with original
                dataset = pd.concat([dataset, avg_df])
                
        x = list(dataset.index)
        x.sort()
        # print(x, dataset)
        try:
            dg = [key for key, val in datagroups_x_dct.items() if x == val][0]
            # concatenate dataframes
            datagroups_dct[dg] = pd.concat([datagroups_dct[dg], dataset], axis = 1)
        except IndexError:
            dg_N += 1
            dg = 'dg' + str(dg_N)
            datagroups_x_dct[dg] = x
            datagroups_dct[dg] = dataset

    #print(datagroups_dct)
    return datagroups_dct


UNITS = {'temperature': ['K'],
         'length': ['m', 'dm', 'cm', 'mm'],
         'time': ['s', 'us', 'ms', 'ns', 'min'],
         'volume': ['m3', 'dm3', 'cm3', 'mm3', 'L'],
         'pressure': ['atm', 'torr', 'Torr', 'kPa', 'MPa', 'Pa', 'bar', 'mbar'],
         }

def readprofile(filename : str):
    data = {}
    # leggi
    profile_data = pd.read_csv(filename, sep = ';', header = None)
    # prime 2 righe: temperature, pressure con relative unità per initial conditions
    # name1: first initial condition; name2: second initial condition
    dct_keys = ['name', 'value', 'units']
    data['init-cond1'] = dict(zip(dct_keys, [profile_data[0][0]] + profile_data.iloc[0][1].split()))
    data['init-cond2'] = dict(zip(dct_keys, [profile_data[0][1]] + profile_data.iloc[1][1].split()))
    # convert to float
    data['init-cond1']['value'] = float(data['init-cond1']['value'])
    data['init-cond2']['value'] = float(data['init-cond2']['value'])
    # 3a riga: qualcosa tra length e time, con relativa unità
    data['x'] = dict(zip(dct_keys, 
                         [profile_data[0][2]] + 
                         [np.array(profile_data[0][5:].values, dtype=float)] + 
                         [profile_data[1][2].strip()]))
    # 4a riga: qualcosa tra temperature, pressure, volume
    data['y'] = dict(zip(dct_keys, 
                         [profile_data[0][3]] + 
                         [np.array(profile_data[1][5:].values, dtype=float)] + 
                         [profile_data[1][3].strip()]))
    
    # checks: initial conditions - names
    init_cond_list = ['temperature', 'pressure', 'time', 'length']
    if data['init-cond1']['name'] not in init_cond_list or data['init-cond2']['name'] not in init_cond_list:
        raise ValueError('initial conditions should be among {}'.format(' '.join(init_cond_list)))
    # checks: x and y values
    if data['x']['name'] not in ['length', 'time']:
        raise ValueError('x should be length or time')
    if data['y']['name'] not in ['temperature', 'volume', 'pressure']:
        raise ValueError('x should be temperature, volume or pressure')        
    # checks: units
    for key in data.keys():
        if data[key]['units'] not in UNITS[data[key]['name']]:
            print(data[key])
            raise ValueError('units for {} should be among {}'.format(data[key]['name'], UNITS[data[key]['name']]))
        
    return data

OS_PROPERTIES = {
    'InletVelocity' : 'velocity',
    '@Pressure' : 'pressure',
    'Length' : 'length',
    'FuelVelocity' : 'fuel velocity',
    'OxidizerVelocity' : 'oxidizer velocity',    
}
DICT_NAMES = {
    'FuelStream' : [['stringaintrovabile', False], ['Temperature', 'fuel temperature'], 'commonprop'],
    'OxidizerStream' : [['stringaintrovabile', False],['Temperature', 'oxidizer temperature'], 'commonprop'],
    'FixedTemperatureProfile' : [['stringaintrovabile', False],['Profile', 'T profile'], 'character'],
}

def process_osinput(path, osinputname, profiles = False, flameinfo = False):
    """ process OS input file to extract info
    """
    extrainfo = dict(zip(['profileinfo', 'commonprop', 'character'],[{},{},{}]))
    DICT_NAMES_new = DICT_NAMES
    
    with open(os.path.join(path, osinputname)) as f:
        for line in f:
            if profiles == True and 'ListOfProfiles' in line and '//' not in line.split('ListOfProfiles')[0]:
                print('reminder if sth looks weird - ListOfProfiles must be all in the same row')
                extrainfo['profileinfo']['csv_profiles'] = line.split('ListOfProfiles')[1].split(';')[0].strip().split()
                extrainfo['profileinfo']['csv_paths'] = [os.path.join(path, file) for file in extrainfo['profileinfo']['csv_profiles']]
            
            if flameinfo == True:
                for keyprop, prop_tosciexp in OS_PROPERTIES.items():
                    if keyprop in line and '//' not in line.split(keyprop)[0]:
                        extrainfo['commonprop'][prop_tosciexp] = line.split(keyprop)[1].split(';')[0].strip().split() # string includes both value and units
            
            # find keys for fuelstream and oxidizerstream
            # this way of looking for things is stupid - use automech parser in the future
            for key, val in DICT_NAMES_new.items():    
                if key in line and '//' not in line.split(key)[0]:
                    DICT_NAMES_new[key][0][0] = line.split(key)[1].split(';')[0].strip()     
                    
                if val[0][1] == True and val[1][0] in line and '//' not in line.split(val[1][0])[0]:
                    extrainfo[val[2]][val[1][1]] = line.split(val[1][0])[1].split(';')[0].strip().split()
                    DICT_NAMES_new[key][0][1] = False
                    
                if val[0][0] in line:
                    DICT_NAMES_new[key][0][1] = True
    
    with open(os.path.join(path, osinputname)) as f:
        inputstr = f.read()
        
    return inputstr, extrainfo