import time_conversion

"""This module has functions to find the weekly parasha for a given Shabbos.
The algorithm comes from Dr. Irv Bromberg, University of Toronto at 
http://individual.utoronto.ca/kalendis/hebrew/parshah.htm
"""  

parshios = (
            'Beraishis', 'Noach', "Lech L'cha", 'Vayera', 'Chayei Sarah',
            'Toldos', 'Vayetzei', 'Vayishlach', 'Vayeshev', 'Miketz',
            'Vayigash', 'Vayechi', 'Shemos',  "Va'era", 'Bo', 'Beshalach',
            'Yisro',  'Mishpatim', 'Teruma', 'Tetzave', 'Ki Sisa', 'Vayakhel',
            'Pekudei', 'Vayikra', 'Tzav','Shemini', 'Tazria', 'Metzora',
            'Acharei Mos','Kedoshim', 'Emor', "Behar", 'Bechukosai', 'Bamidbar',
            'Naso',"Baha'aloscha", "Shelach", 'Korach', 'Chukas', 'Balak',
            'Pinchas','Matos', "Ma'sei", 'Devarim', "Va'eschanan", 'Eikev',
            "R'ey", 'Shoftim', 'Ki Setzei', 'Ki Savo', 'Netzavim', 'Vayelech',
            'Haazinu', "Vezos Habrocho")