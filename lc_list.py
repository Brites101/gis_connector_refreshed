def lc_list():
    lcs = [
    {'id': 1606, 'name': "BRAZIL", 'sigla': 'BAZI', 'cluster': 0},    
    # Cluster 1 - 8 CLs
    {'id': 436, 'name': "ESPM", 'sigla': 'ES', 'cluster': 1},
    {'id': 1300, 'name': "Brasília", 'sigla': 'BS','cluster': 1},
    {'id': 1178, 'name': "Curitiba", 'sigla': 'CT','cluster': 1},
    {'id': 1121, 'name': "Salvador", 'sigla': 'SS','cluster': 1},
    {'id': 909, 'name': "Vitória", 'sigla': 'VT','cluster': 1},
    {'id': 854, 'name': "Porto Alegre", 'sigla': 'PA','cluster': 1},
    {'id': 1248, 'name': "Belo Horizonte", 'sigla': 'BH','cluster': 1},
    {'id': 2151, 'name': "Natal", 'sigla': 'NA','cluster': 1},
    # Cluster 2 - 11 CLs
    {'id': 777, 'name': "Rio De Janeiro", 'sigla': 'RJ', 'cluster': 2},
    {'id': 943, 'name': "Getúlio Vargas", 'sigla': 'GV', 'cluster': 2},
    {'id': 2061, 'name': "Limeira", 'sigla': 'LM', 'cluster': 2},
    {'id': 1666, 'name': "Joao Pessoa", 'sigla': 'JP','cluster': 2},
    {'id': 958, 'name': "Santa Maria", 'sigla': 'SM','cluster': 2},
    {'id': 723, 'name': "Maringá", 'sigla': 'MA','cluster': 2},
    {'id': 435, 'name': "Sao Carlos", 'sigla': 'SC','cluster': 2},
    {'id': 233, 'name': "Insper", 'sigla': 'IN','cluster': 2},
    {'id': 287, 'name': "Uberlândia", 'sigla': 'UB','cluster': 2},
    {'id': 286, 'name': "Fortaleza", 'sigla': 'FO','cluster': 2},
    {'id': 988, 'name': "Florianópolis", 'sigla': 'FL','cluster': 2},
    # Cluster 3 - 12 CLs
    {'id': 1003, 'name': "USP", 'sigla': 'US', 'cluster': 3},
    {'id': 2152, 'name': "Mackenzie", 'sigla': 'MK', 'cluster': 3},
    {'id': 2155, 'name': "Blumenau", 'sigla': 'BM', 'cluster': 3},
    {'id': 2149, 'name': "Maceio", 'sigla': 'MZ', 'cluster': 3},
    {'id': 2148, 'name': "Viçosa", 'sigla': 'VC', 'cluster': 3},
    {'id': 2098, 'name': "Teresina", 'sigla': 'TE', 'cluster': 3},
    {'id': 1368, 'name': "Vale Do Paraíba", 'sigla': 'VP','cluster': 3},
    {'id': 541, 'name': "Recife", 'sigla': 'RC','cluster': 3},
    {'id': 283, 'name': "Chapeco", 'sigla': 'CH','cluster': 3},
    {'id': 232, 'name': "Joinville", 'sigla': 'JV','cluster': 3},
    {'id': 230, 'name': "Sorocaba", 'sigla': 'SO','cluster': 3},
    {'id': 32, 'name': "Bauru", 'sigla': 'BA','cluster': 3},
    # Cluster 4 - 10 CLs
    {'id': 2150, 'name': "Cuiaba", 'sigla': 'CB', 'cluster': 4},
    {'id': 1816, 'name': "Santos", 'sigla': 'SA', 'cluster': 4},
    {'id': 1766, 'name': "Campo Grande", 'sigla': 'CG', 'cluster': 4},
    {'id': 1649, 'name': "Vale Do Sao Francisco", 'sigla': 'SF','cluster': 4},
    {'id': 479, 'name': "Itajuba", 'sigla': 'IJ','cluster': 4},
    {'id': 467, 'name': "Ribeirao Preto", 'sigla': 'RP','cluster': 4},
    {'id': 289, 'name': "Volta Redonda", 'sigla': 'VR','cluster': 4},
    {'id': 148, 'name': "Pelotas", 'sigla': 'PE','cluster': 4},
    {'id': 100, 'name': "Aracaju", 'sigla': 'AJ','cluster': 4},
    {'id': 1647, 'name': "ABC", 'sigla': 'AB','cluster': 4},
    # Cluster 5 - 9 CLs
    {'id': 2344, 'name': "São Luis", 'sigla': 'SL', 'cluster': 5},
    {'id': 2343, 'name': "Palmas", 'sigla': 'PW','cluster': 5},
    {'id': 1731, 'name': "Balneario Camboriu", 'sigla': 'BC', 'cluster': 5},    
    {'id': 437, 'name': "Londrina", 'sigla': 'LD','cluster': 5},
    {'id': 434, 'name': "Goiania", 'sigla': 'GO','cluster': 5},
    {'id': 231, 'name': "Manaus", 'sigla': 'MN','cluster': 5},
    {'id': 284, 'name': "Franca", 'sigla': 'FR','cluster': 5}, 
    {'id': 12, 'name': "Belém", 'sigla': 'BL','cluster': 5},
    {'id': 2147, 'name': "São José do Rio Preto", 'sigla': 'SJ','cluster': 5},
    # CLs Fechados - 3 CLs
    {'id': 2153, 'name': "Campina Grande - fechado", 'sigla': 'CP','cluster': 0},
    {'id': 146, 'name': "Santarém - Fechado", 'sigla': 'SR','cluster': 0},
    {'id': 288, 'name': "PUC - Fechado", 'sigla': 'PC','cluster': 0}]

    return lcs
