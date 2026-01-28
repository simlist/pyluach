from pyluach.names import Parshios, Months, FourParshios, Days

"""
class DaysEnum):
    ROSH_HASHANA = 'ראש השנה'
    YOM_KIPPUR = 'יום כיפור'
    SUCCOS = 'סוכות'
    SHMINI_ATZERES = 'שמיני עצרת'
    SIMCHAS_TORAH = 'שמחת תורה'
    CHANUKA = 'חנוכה'
    TU_BSHVAT = 'ט״ו בשבט'
    PURIM_KATAN = 'פורים קטן'
    PURIM = 'פורים'
    SHUSHAN_PURIM = 'שושן פורים'
    PESACH = 'פסח'
    PESACH_SHENI = 'פסח שני'
    LAG_BAOMER = 'ל״ג בעומר'
    SHAVUOS = 'שבועות'
    TU_BAV = 'ט״ו באב'
    TZOM_GEDALIA = 'צום גדליה'
    TENTH_OF_TEVES = 'י׳ בטבת'
    TAANIS_ESTHER = 'תענית אסתר'
    SEVENTEENTH_OF_TAMUZ = 'י״ז בתמוז'
    NINTH_OF_AV = 'ט׳ באב'
"""


english_ashkenazic = {
    Months.NISSAN: 'Nissan',
    Months.IYAR: 'Iyar',
    Months.SIVAN: 'Sivan',
    Months.TAMMUZ: 'Tammuz',
    Months.AV: 'Av',
    Months.ELUL: 'Elul',
    Months.TISHREI: 'Tishrei',
    Months.CHESHVAN: 'Cheshvan',
    Months.KISLEV: 'Kislev',
    Months.TEVES: 'Teves',
    Months.SHEVAT: 'Shevat',
    Months.ADAR: 'Adar',
    Months.ADAR1: 'Adar 1',
    Months.ADAR2: 'Adar 2',
    Parshios.BEREISHIS: 'Bereishis',
    Parshios.NOACH: 'Noach',
    Parshios.LECH_LECHA: 'Lech Lecha',
    Parshios.VAYEIRA: 'Vayeira',
    Parshios.CHAYEI_SARAH: 'Chayei Sarah',
    Parshios.TOLDOS: 'Toldos',
    Parshios.VAYEITZEI: 'Vayeitzei',
    Parshios.VAYISHLACH: 'Vayishlach',
    Parshios.VAYEISHEV: 'Vayeishev',
    Parshios.MIKEITZ: 'Mikeitz',
    Parshios.VAYIGASH: 'Vayigash',
    Parshios.VAYECHI: 'Vayechi',
    Parshios.SHEMOS: 'Shemos',
    Parshios.VAEIRA: "Va'eira",
    Parshios.BO: 'Bo',
    Parshios.BESHALACH: 'Beshalach',
    Parshios.YISRO: 'Yisro',
    Parshios.MISHPATIM: 'Mishpatim',
    Parshios.TERUMAH: 'Terumah',
    Parshios.TETZAVEH: 'Tetzaveh',
    Parshios.KI_SISA: 'Ki Sisa',
    Parshios.VAYAKHEL: 'Vayakhel',
    Parshios.PEKUDEI: 'Pekudei',
    Parshios.VAYIKRA: 'Vayikra',
    Parshios.TZAV: 'Tzav',
    Parshios.SHEMINI: 'Shemini',
    Parshios.TAZRIA: 'Tazria',
    Parshios.METZORA: 'Metzora',
    Parshios.ACHAREI_MOS: 'Acharei Mos',
    Parshios.KEDOSHIM: 'Kedoshim',
    Parshios.EMOR: 'Emor',
    Parshios.BEHAR: 'Behar',
    Parshios.BECHUKOSAI: 'Bechukosai',
    Parshios.BAMIDBAR: 'Bamidbar',
    Parshios.NASSO: 'Nasso',
    Parshios.BEHAALOSCHA: "Beha'aloscha",
    Parshios.SHELACH: 'Shelach',
    Parshios.KORACH: 'Korach',
    Parshios.CHUKAS: 'Chukas',
    Parshios.BALAK: 'Balak',
    Parshios.PINCHAS: 'Pinchas',
    Parshios.MATTOS: 'Mattos',
    Parshios.MASEI: 'Masei',
    Parshios.DEVARIM: 'Devarim',
    Parshios.VAESCHANAN: "Va'eschanan",
    Parshios.EIKEV: 'Eikev',
    Parshios.REEH: "Re'eh",
    Parshios.SHOFTIM: 'Shoftim',
    Parshios.KI_SEITZEI: 'Ki Seitzei',
    Parshios.KI_SAVO: 'Ki Savo',
    Parshios.NITZAVIM: 'Nitzavim',
    Parshios.VAYEILECH: 'Vayeilech',
    Parshios.HAAZINU: 'Haazinu',
    Parshios.VEZOS_HABERACHA: 'Vezos Haberacha',
    FourParshios.SHEKALIM: 'Shekalim',
    FourParshios.ZACHOR: 'Zachor',
    FourParshios.PARAH: 'Parah',
    FourParshios.HACHODESH: 'Hachodesh',
    Days.ROSH_HASHANA: 'Rosh Hashana',
    Days.YOM_KIPPUR: 'Yom Kippur',
    Days.SUCCOS: 'Succos',
    Days.SHMINI_ATZERES: 'Shmini Atzeres',
    Days.SIMCHAS_TORAH: 'Simchas Torah',
    Days.CHANUKA: 'Chanuka',
    Days.TU_BSHVAT: "Tu B'shvat",
    Days.PURIM_KATAN: 'Purim Katan',
    Days.PURIM: 'Purim',
    Days.SHUSHAN_PURIM: 'Shushan Purim',
    Days.PESACH: 'Pesach',
    Days.PESACH_SHENI: 'Pesach Sheni',
    Days.LAG_BAOMER: "Lag Ba'omer",
    Days.SHAVUOS: 'Shavuos',
    Days.TU_BAV: "Tu B'av",
    Days.TZOM_GEDALIA: 'Tzom Gedalia',
    Days.TENTH_OF_TEVES: '10 of Teves',
    Days.TAANIS_ESTHER: 'Taanis Esther',
    Days.SEVENTEENTH_OF_TAMMUZ: '17 of Tammuz',
    Days.NINTH_OF_AV: '9 of Av'
}
