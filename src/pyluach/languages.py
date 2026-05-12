"""The languages module contains the translations for the months, parshios, and holidays."""
from pyluach.values import Parshios, Months, FourParshios, Days


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


def _get_translation(val, hebrew, language):
    """Return the translation for the given value.
    Parameters
    ----------
    val : Enum
        The value to translate.
    hebrew : bool
        Whether to return name of the value in Hebrew. This takes
        precedence over the language parameter.
    language : dict
        A dict mapping the value (from the values module) to the the desired
        translation. If not given or if the dict doesn't contain the value,
        the English Ashkenazic translation will be used.

    Returns
    -------
    str
        The translation of the value.
    """
    if hebrew:
        return val.value
    if not language:
        language = english_ashkenazic
    return language.get(val, english_ashkenazic[val])
