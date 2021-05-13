import os
import sys
import csv
import pandas as pd
import xlrd
import droit_tools.ref_data_csv_file_structure as file_structure
import droit_tools.ref_data_config as rd_config
import droit_tools.ref_data_tenor_util as tenor_util

default_result_file_name = "20210430_nyar_liquid_results.xlsx"
default_file_name = 'template_nyar.xlsx'
file_name = sys.argv.pop() if len(sys.argv) > 1 else default_result_file_name
path = os.path.join(os.environ['DROIT_REFDATA'], file_name)


def update_header_columns(source: str, attribute: str, type_: str, operator: str, mode: str, sources: list,
                          types: list, operators: list, modes: list) -> None:
    sources.append(source + '.' + attribute)
    types.append(type_)
    operators.append(operator)
    modes.append(mode)


def populate_header(data_map, file_to_update, file_metadata: dict) -> None:
    sources = list()
    types = list()
    operators = list()
    modes = list()
    data = data_map.get(file_to_update, dict())
    inputs = file_metadata['inputs']
    for item in inputs:
        column = file_structure.column_taxonomy.get(item)
        if item.find('@') >-1:
            xxx=1
        column_name = item.split('@')[0]
        if column['type'] == 'TENOR' and column_name == 'residualTerm':  # tenor has a different behaviour and as such we are making a hack to accommodate
            update_header_columns(column['module'], column_name, column['type'], 'GT', 'INPUT', sources,
                                  types, operators, modes)
            # add the second column
            update_header_columns(column['module'], column_name, column['type'], 'MAX', 'INPUT', sources,
                                  types, operators, modes)

        else:
            column_name = item.split('@')[0]
            update_header_columns(column['module'], column_name, column['type'], 'EQ', 'INPUT', sources,
                                  types, operators, modes)

    outputs = file_metadata['outputs']
    for item in outputs:
        column = file_structure.column_taxonomy.get(item)
        column_name = item.split('@')[0]
        update_header_columns(column['module'], column_name, column['type'], '', 'OUTPUT', sources,
                              types, operators, modes)

    header = [sources, types, operators, modes]
    data["header"] = header
    data_map[file_to_update] = data


def add_input_to_row(item: str, row: list, row_dict: dict, asset_tuple: tuple) -> bool:
    taxonomy = file_structure.column_taxonomy.get(item)

    mandatory = taxonomy.get('mandatory', False)
    default = None if mandatory else taxonomy['default']

    if taxonomy.get('type') == 'TENOR' and item.find('residualTerm') > -1:
        tenor_buck = row_dict.get(taxonomy['code'])
        extra_info = row_dict.get('SP')
        buckets = tenor_util.tenor_bucket_parser(tenor_buck, asset_tuple.get('SubAsset'), extra=extra_info)
        if len(buckets) != 2:
            raise Exception("Got back a malformed tenor bucket")
        for i in range(len(buckets)):
            row.append(buckets[i])

    elif taxonomy.get('depend', False):
        depend_dict = taxonomy.get('depend')
        colum_depend = file_structure.column_taxonomy.get(depend_dict['col'])
        val_depend = row_dict.get(colum_depend['code'])

        if val_depend not in depend_dict['vals'] and depend_dict.get('op') == 'not exists':
            if asset_tuple.get('SubAsset') in depend_dict.get('sub-asset', []):
                val = row_dict.get(taxonomy["code"], default)
            else:
                val = default
        elif val_depend in depend_dict['vals'] and depend_dict.get('op') == 'exists':
            val = row_dict.get(taxonomy["code"], default)
        else:
            val = default

        if mandatory and val == None:
            return True
        else:
            row.append(val)
    else:
        val = row_dict.get(taxonomy["code"], default)
        if mandatory:
            x = 1
        if item.find('underlyingBondTerm') > -1 and val != 'NA':
            val = rd_config.bond_term_code[val].upper()

        if taxonomy.get('type') == 'BOOLEAN':

            if val in ['T']:
                val = 'true'
            else:
                val = 'false'
        if 'LIST' in taxonomy.get('extra', []) and val is not None:
            val = '["' + val + '"]'

        if mandatory and val is None:
            return True
        else:
            row.append(val)

    return False


def extract_code_val(code: str, row_string: str) -> str:
    split_val = row_string.split(code + '=')[1]

    if '=' in split_val:
        split_val = split_val.split('=')[0]
        last_char_index = split_val.rfind("&")
        split_val = split_val[:last_char_index]

    if split_val == '':
        split_val = None

    if split_val is not None:
        return split_val.strip()
    else:
        return split_val


def product_codes_parser(id_code: str, extra: dict) -> dict:
    val = rd_config.product_codes.get(id_code)

    if id_code == 'IRD06':
        product_type = rd_config.swap_codes.get(extra.get('UTYP'))
        if product_type is None:
            raise Exception('Unrecognised Swap Code')
        val['SubAsset'] = product_type

    return val


def parse_row(row_input: dict, data_map: dict) -> None:
    # asset_tuple = product_codes.get()
    row_dict = dict()
    row_sub_class = row_input["Sub-class identification"]
    for code in file_structure.codes:
        prefix = '' if code == 'SACID' else '&'
        if (prefix + code + '=') in row_sub_class:
            val = extract_code_val(prefix + code, row_sub_class)
            if val is not None:
                row_dict[code] = extract_code_val(prefix + code, row_sub_class)

    row_dict.update(row_input)

    asset_tuple = product_codes_parser(row_dict.get('SACID'), row_dict)
    row_dict['ASSET'] = asset_tuple.get('Asset')
    row_dict['SUBASSET'] = asset_tuple.get('SubAsset')

    files_to_update = file_structure.subasset_taxonomy.get(
        (asset_tuple.get('Asset'), asset_tuple.get('SubAsset'))) or \
                      file_structure.product_taxonomy.get(asset_tuple.get('Asset'))

    if not files_to_update:
        return None
    for file_to_update in files_to_update:
        file_metadata = file_structure.files_to_generate.get(file_to_update)
        if not data_map.get(file_to_update):
            populate_header(data_map, file_to_update, file_metadata)

        row_elem = list()
        inputs = file_metadata['inputs']
        do_not_append = False
        for item in inputs:
            do_not_append = add_input_to_row(item, row_elem, row_dict, asset_tuple) or do_not_append

        outputs = file_metadata['outputs']
        for item in outputs:
            do_not_append = add_input_to_row(item, row_elem, row_dict, asset_tuple) or do_not_append

        # after checking that all mandatory elements are there should we append the row we created
        if not do_not_append:
            data = data_map.get(file_to_update)
            # can be done with defaultdict instead
            data_rows = data.get('data', list())

            data_rows.append(row_elem)
            data['data'] = data_rows
            data_map[file_to_update] = data

    return None


def create_csv_file(file_name: str, data: list) -> None:
    with open(os.path.join(os.environ['DROIT_REFDATA'], file_name + '.csv'), 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerows(data['header'])
        writer.writerows(data['data'])


if __name__ == "__main__":

    data_map = dict()

    df_note = pd.read_excel(path, 'Explanatory note')
    df_results = pd.read_excel(path, 'Liquidity LIS SSTI results')

    for index, row in df_results.iterrows():
        if index:
            parse_row(dict(row), data_map)

    for key, value in data_map.items():
        create_csv_file(key, value)
