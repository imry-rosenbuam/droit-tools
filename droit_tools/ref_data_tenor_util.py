from typing import Optional, Dict, List

TENOR_MIN = '0D'

maturity_buckets = {
    "MetalCommodityFutureOrForward": {"PRME": ['3m', '1y', '2y'], "NPRM": ['1y', '2y']},
    "MetalCommodityOption": {"PRME": ['3m', '1y', '2y'], "NPRM": ['1y', '2y']},
    "MetalCommoditySwap": {"PRME": ['3m', '1y', '2y'], "NPRM": ['1y', '2y']},
    "EnergyCommodityFutureOrForward": {'COAL': ['6m', '1y', '2y'],
                                       'OILP': ['4m', '8m', '1y', '2y'],
                                       'ELEC': ['1m', '1y', '2y'],
                                       'NGAS': ['1m', '1y', '2y']},
    "EnergyCommodityOption": {'COAL': ['6m', '1y', '2y'],
                              'OILP': ['4m', '8m', '1y', '2y'],
                              'ELEC': ['1m', '1y', '2y'],
                              'NGAS': ['1m', '1y', '2y']},
    "EnergyCommoditySwap": {'COAL': ['6m', '1y', '2y'],
                            'OILP': ['4m', '8m', '1y', '2y'],
                            'ELEC': ['1m', '1y', '2y'],
                            'NGAS': ['1m', '1y', '2y']},
    "AgriculturalCommodityFutureOrForward": {'DEFAULT': ['3m', '6m', '1y', '2y']},
    "AgriculturalCommodityOption": {'DEFAULT': ['3m', '6m', '1y', '2y']},
    "AgriculturalCommoditySwap": {'DEFAULT': ['3m', '6m', '1y', '2y']},
    "BondFutureOrForward": {'DEFAULT': ['3m', '6m', '1y', '2y']},
    "FixedFloatSingleCurrency": {'DEFAULT': ['1m', '3m', '6m', '1y', '2y', '3y']},
    "InflationSingleCurrency": {'DEFAULT': ['1m', '3m', '6m', '1y', '2y', '3y']},
    "OISSingleCurrency": {'DEFAULT': ['1m', '3m', '6m', '1y', '2y', '3y']}
}

terms = {
    'ST': 'Short term',
    'MT': 'Medium term',
    'LT': 'Long term',
    'ULT': 'Ultra long term',
}


def parse_term(input_str: str) -> str:
    return terms.get(input_str)


# translate tenor to the monthly values in order to compare
def tenor_parser(tenor: str) -> int:
    number = list(filter(lambda x: x.isnumeric(), tenor))
    number = int(''.join(number))
    scale = list(filter(lambda x: x.isalpha(), tenor))
    if len(scale) != 1 or scale[0].upper() not in ['M', 'Y']:
        raise Exception("wrong tenor specification")
    scale = 1 if scale[0] == 'Y' else 12
    return scale * number


# assumption is that last value in the segmentation list is that it will be in years and every bucket after
# increase in a year per bucket
def tenor_bucket_parser(tenor_code: str, sub_asset: str, extra: str = None) -> list:
    try:
        bucket_dict: Dict[str, List[str]] = maturity_buckets.get(sub_asset)

        # get the list of Tenors from the dictionary
        if len(bucket_dict) == 1 or extra is None:
            bucket_list = list(bucket_dict.values())[0].copy()
        else:
            if extra in list(bucket_dict.keys()):
                bucket_list = list(bucket_dict.get(extra)).copy()
            else:
                raise Exception('invalid data enters for Tenor parser')
                bucket_list = list(bucket_dict.values()).copy()

        bucket = int(tenor_code)
        tenor_max = None
        tenor_min = None

        if sub_asset is 'FixedFloatSingleCurrency':
            xx = 1
        if bucket <= len(bucket_list):
            tenor_max = bucket_list[bucket - 1]
            tenor_min = bucket_list[bucket - 2] if bucket - 1 else TENOR_MIN
        else:
            tenor_min = bucket - len(bucket_list) - 1 + int(tenor_parser(bucket_list.pop()) / 12)
            tenor_max = str(tenor_min + 1) + 'Y'
            tenor_min = str(tenor_min) + 'Y'

        return [x.upper() for x in [tenor_min, tenor_max]]
    except:
        print("failed to parse the tenor bucket")
        return []
