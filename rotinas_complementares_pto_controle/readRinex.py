import os

def get_rinex_data(pasta, nome):
    rinex_info = {}
    with open(os.path.join(pasta, nome)) as rinex_file:
        lines = rinex_file.readlines()
        for line in lines:
            key = line[60:].strip()
            if key == 'END OF HEADER':
                break
            value = list(filter(None, line[:60].strip().split(' ')))
            if key == 'MARKER NAME':
                rinex_info['cod_ponto_1'] = value[0]
            elif key == 'MARKER NUMBER':
                rinex_info['cod_ponto_2'] = value[0]
            elif key == 'REC # / TYPE / VERS':
                rinex_info['nr_serie_receptor'] = value[0]
                rinex_info['modelo_receptor'] = value[1]
            elif key == 'ANT # / TYPE':
                rinex_info['nr_serie_antena'] = value[0]
                rinex_info['modelo_antena'] = value[1]
            elif key == 'ANTENNA: DELTA H/E/N':
                rinex_info['altura_antena'] = value[0]
            elif key == 'TIME OF FIRST OBS':
                rinex_info['data_rastreio_1'] = '{0}-{1}-{2}'.format(
                    value[0],
                    value[1].zfill(2),
                    value[2].zfill(2)
                )
                rinex_info['hora_inicio_rastreio'] = '{0}:{1}'.format(
                    value[3],
                    value[4].zfill(2)
                )
            elif key == 'TIME OF LAST OBS':
                rinex_info['data_rastreio_2'] = '{0}-{1}-{2}'.format(
                    value[0],
                    value[1].zfill(2),
                    value[2].zfill(2)
                )
                rinex_info['hora_fim_rastreio'] = '{0}:{1}'.format(
                    value[3],
                    value[4].zfill(2)
                )
        print(rinex_info)
            
            
            
        
        #rinex_info["cod_ponto_1"] = lines[3].split(' ')[0]
#        rinex_info["cod_ponto_2"] = lines[4].split(' ')[0]
#        rinex_info["nr_serie_receptor"] = lines[6].split(' ')[0]
#        rinex_info["modelo_receptor"] = [
#            x for x in lines[6].split('  ') if x][1].strip()
#        rinex_info["nr_serie_antena"] = lines[7].split(' ')[0].strip()
#        if "NONE" in lines[7]:
#            rinex_info["modelo_none"] = True
#        else:
#            rinex_info["modelo_none"] = False
#        rinex_info["modelo_antena"] = [
#            x for x in lines[7].split('  ') if x][1].strip()
#        rinex_info["altura_antena"] = lines[9].strip().split(' ')[0]
#        aux_inicio = [x for x in lines[12].strip().split(' ') if x]
#        rinex_info["data_rastreio_1"] = "{0}-{1}-{2}".format(
#            aux_inicio[0], aux_inicio[1].zfill(2), aux_inicio[2].zfill(2))
#        rinex_info["hora_inicio_rastreio"] = "{0}:{1}".format(
#            aux_inicio[3], aux_inicio[4])
#        aux_fim = [x for x in lines[13].strip().split(' ') if x]
#        rinex_info["data_rastreio_2"] = "{0}-{1}-{2}".format(
#            aux_fim[0], aux_fim[1].zfill(2), aux_fim[2].zfill(2))
#        rinex_info["hora_fim_rastreio"] = "{0}:{1}".format(
#            aux_fim[3], aux_fim[4])

    return rinex_info
    
get_rinex_data(
'C:\\Users\\marcel\\Desktop\\TOPCON\\0703\\paulo_2022-07-03\\RS-HV-201\\2_RINEX',
'RS-HV-201.22o'
)