import json

GSE_LIB={}
with open('GSCLib_3.0.lib', 'r') as gsc_file: #open the file 
    lines = ' '.join(gsc_file.readlines()[103:]).replace('\n','').split('* Design :')[1:]
    for line in lines: # cell information
        cell_info = line.split('pin(')[0].split('*')
        cell_name = cell_info[0].strip()
        area = float(cell_info[3].split(';')[0].split(':')[-1].strip())
        cell_leakage_power = float(cell_info[3].split(';')[1].split(':')[-1].strip())
        GSE_LIB[cell_name]={}
        GSE_LIB[cell_name]['area']=area
        GSE_LIB[cell_name]['cell_leakage_power']=cell_leakage_power
        GSE_LIB[cell_name]['pins']={}
        pin_list = line.split('pin(')[1:]
        for pin in pin_list:
            pin_name=pin.split(')')[0]
            GSE_LIB[cell_name]['pins'][pin_name]={}
            GSE_LIB[cell_name]['pins'][pin_name]['direction']= pin.split(';')[0].split(':')[-1].strip()
            GSE_LIB[cell_name]['pins'][pin_name]['capacitance']= float(pin.split(';')[1].split(':')[-1].strip())
            GSE_LIB[cell_name]['pins'][pin_name]['rise_capacitance'] = float(pin.split(';')[2].split(':')[-1].strip())
            GSE_LIB[cell_name]['pins'][pin_name]['fall_capacitance'] = float(pin.split(';')[3].split(':')[-1].strip())
            if GSE_LIB[cell_name]['pins'][pin_name]['direction']=="output":
                GSE_LIB[cell_name]['pins'][pin_name]['max_capacitance'] = float(pin.split(';')[4].split(':')[-1].strip())
                