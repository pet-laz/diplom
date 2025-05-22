with open('bolez2_smclinic.txt', 'r', encoding='utf-8') as f:
    bols = f.read().split('\n')
dict_of_bols = {
    'name': [],
    'simptoms': [],
}
for bol in bols:
    bol = bol.lower()
    name, simptoms = bol.split(' - ')
    dict_of_bols['name'].append(name)
    dict_of_bols['simptoms'].append(simptoms)
dict_of_bols_no_replay = {
    'name': [],
    'simptoms': [],
}
for i in range(len(dict_of_bols['name']) - 1):
    k = True
    for j in range(i + 1, len(dict_of_bols['name']) - 1):
        
        if dict_of_bols['name'][i] == dict_of_bols['name'][j] and not str(dict_of_bols['name'][i]).count('рак') and not str(dict_of_bols['name'][i]).count('перелом'):
            if dict_of_bols['name'][i] in dict_of_bols_no_replay['name']:
                dict_of_bols_no_replay['simptoms'][dict_of_bols_no_replay['name'].index(dict_of_bols['name'][i])] = ( list(set(list(str(dict_of_bols['simptoms'][i] + ', ' + dict_of_bols['simptoms'][j]).split(', ')))) )
            else:
                dict_of_bols_no_replay['name'].append(dict_of_bols['name'][i])
                dict_of_bols_no_replay['simptoms'].append( list(set(list(str(dict_of_bols['simptoms'][i] + ', ' + dict_of_bols['simptoms'][j]).split(', ')))) )
            k = False

    if k:
        if not str(dict_of_bols['name'][i]).count('рак') and not str(dict_of_bols['name'][i]).count('перелом'):
            dict_of_bols_no_replay['name'].append(dict_of_bols['name'][i])
            dict_of_bols_no_replay['simptoms'].append( list(set(list(str(dict_of_bols['simptoms'][i]).split(', ')))) )
# print(dict_of_bols_no_replay['name'][6], '-', dict_of_bols_no_replay['simptoms'][1])
# print((dict_of_bols_no_replay['simptoms'][8]))

# import json
# with open('bolez2_struct.json', 'w', encoding='utf-8') as f:
#     json.dump(dict_of_bols_no_replay, f, ensure_ascii=False)

print(len(dict_of_bols_no_replay['name']))
# for i in range(len(dict_of_bols_no_replay['name']) - 1):
#     if str(dict_of_bols_no_replay['name'][i]).count('рак'): print(1)