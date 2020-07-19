import os
import sys
import json
import pandas as pd

default_result_file_name = "20200710_nyar_liquid_results.xlsx"
default_file_name = 'template_nyar.xlsx'
file_name = sys.argv.pop() if len(sys.argv) > 1 else default_result_file_name
path = os.path.join(os.environ['DROIT_REFDATA'], file_name)

json_file_prefix = "esma_ref_data_commodity"

standard_output = [("preTradeSSTI", "SSTI pre-trade"), ("preTradeLIS", "LIS pre-trade"),
                   ("postTradeSSTI", "SSTI post-trade"), ("postTradeLIS", "SSTI post-trade"),
                   ("liquidMarketForProduct", "Liquidity")]
bond_output = [("preTradeSSTI", "SSTI pre-trade"), ("preTradeLIS", "LIS pre-trade"),
               ("postTradeSSTI", "SSTI post-trade"), ("postTradeLIS", "SSTI post-trade")]

# let us enumerate to which files we will be segregating our records on to
# inputs asset_code is unique key as it will reinterpreted to two as it will also include asset and sub-asset
# keys for inputs or outputs are column name and then esma code for column (name,esma code )
files_to_generate = dict(
    # bond_etc_etn=dict(template= '', inputs= [('asset_code', "SACID"), ("isin", 'ISIN')], outputs= standard_output),
    bond_thresholds=dict(template='esma_ref_data_bond_thresholds.droit.1.0.json', inputs=[('asset_code', "SACID")], outputs=bond_output),
    # bond_future=dict(template='', inputs=[], outputs=[], codes=[]),
    # cfd_bond_future=dict(template='', inputs=[], outputs=[], codes=[]),
    # commodity_derviative=dict(template="", inputs=[], outputs=[], codes=[]),
    # cfd_commodity=dict(template='', inputs=[], outputs=[], codes=[]),
    # credit_derivative_non_option=dict(template="", inputs=[], outputs=[], codes=[]),
    # credit_derivative_option=dict(template="", inputs=[], outputs=[], codes=[]),
    # emission_allowance=dict(template="", inputs=[], outputs=[], codes=[]),
    # emission_allowance_derivative=dict(template="", inputs=[], outputs=[], codes=[]),
    # equity_derivative=dict(template="", inputs=[], outputs=[], codes=[]),
    # equity_derivative_stock_index=dict(template="", inputs=[], outputs=[], codes=[]),
    # interest_rate_derivative=dict(template="", inputs=[], outputs=[], codes=[])
)

# associate an asset to a class
product_taxonomy = {
    ('Bond', 'CorporateBond'): 'bond_etc_etn',
    ('Bond', 'ConvertibleBond'): 'bond_etc_etn',
    ('Bond', 'ConvertibleBond'): 'bond_etc_etn',
    ('Bond', 'CoveredBond'): 'bond_etc_etn',
    ('Bond', 'SovereignBond'): 'bond_etc_etn',
    ('Bond', 'OtherBond'): 'bond_etc_etn',
}

# column taxonomy
# each column -> name module type operator ( null is equality )
# giving opearotr the value tenor will be split unto two columns one with GT and one with MAX
# @ suffix is given to column names that can appear in different tables and thus we need to diffrentiate them
column_taxonomy = {
    "esmaAssetClass": {
        "module": "esma_taxonomy_translation",
        "type": "STRING",
        "default": None
    },
    "esmaSubAssetClass": {
        "module": "esma_taxonomy_translation",
        "type": "STRING",
        "default": None
    },
    "isin": {
        "module": "trade",
        "type": "STRING",
        "default": None
    },
    "preTradeSSTI": {
        "module": "output",
        "type": "INTEGER",
        "default": None
    },
    "postTradeSSTI": {
        "module": "output",
        "type": "INTEGER",
        "default": None
    },
    "postTradeLIS": {
        "module": "output",
        "type": "INTEGER",
        "default": None
    },
    "liquidMarketForProduct": {
        "module": "output",
        "type": "BOOLEAN",
        "default": None
    },
    "mifidCommodityType": {
        "module": "trade",
        "type": "STRING",
        "default": None
    },
    "mifidEnergyType": {
        "module": "trade",
        "type": "STRING",
        "default": None
    },
    "underlyingEnergy": {
        "module": "trade",
        "type": "STRING",
        "default": None
    },
    "metalType": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "underlyingMetal": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "energyType": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "loadType": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "deliveryCashSettlementLocation": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "agriculturalProduct": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "underlyingAgriculturalCommodity": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "notionalCurrency": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "residualTerm@commodity_derivative": {
        "module": "commodity_seg_criteria",
        "type": "TENOR",
        "default": None,
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX
    },
    "underlyingIndex@credit_derivative": {
        "module": "credit_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "underlyingReferenceEntity": {
        "module": "credit_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "underlyingReferenceEntityType": {
        "module": "credit_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "currency@credit_derivative": {
        "module": "credit_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "residualTerm@credit_derivative": {
        "module": "credit_seg_criteria",
        "type": "TENOR",
        "default": None,
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX
    },
    "swaption_swap_residualterm": {
        "module": "trade",
        "type": "TENOR",
        "default": None,
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX
    },
    "swaption_residualterm": {
        "module": "trade",
        "type": "TENOR",
        "default": None,
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX
    },
    "equityDerivativeUnderlyingInstrument": {
        "module": "trade",
        "type": "STRING",
        "default": None,
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX
    },
    "underlierIsin": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "currency@ir_derivative": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "underlyingInterestRate": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": None
    },
    "underlyingIRTerm	": {
        "module": "interest_rate_seg_criteria",
        "type": "TENOR",
        "default": None
    },
    "residualTerm@ir_derivative": {
        "module": "credit_seg_criteria",
        "type": "TENOR",
        "default": None,
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX
    },
}

# Parse product codes
product_codes = {
    "BOND1": {"SubAsset": "SovereignBond", "Asset": "Bond"},
    "BOND2": {"SubAsset": "OtherPublicBond", "Asset": "Bond"},
    "BOND3": {"SubAsset": "ConvertibleBond", "Asset": "Bond"},
    "BOND4": {"SubAsset": "CoveredBond", "Asset": "Bond"},
    "BOND5": {"SubAsset": "CorporateBond", "Asset": "Bond"},
    "BOND6": {"SubAsset": "OtherBond", "Asset": "Bond"},
    "C1001": {"SubAsset": "FreightDerivatives", "Asset": "C10Derivative"},
    "C1002": {"SubAsset": "OtherC10Derivatives", "Asset": "C10Derivative"},
    "CFD01": {"SubAsset": "CurrencyCFDs", "Asset": "ContractForDifference"},
    "CFD02": {"SubAsset": "CommodityCFDs", "Asset": "ContractForDifference"},
    "CFD03": {"SubAsset": "EquityCFD", "Asset": "ContractForDifference"},
    "CFD04": {"SubAsset": "BondCFD", "Asset": "ContractForDifference"},
    "CFD05": {"SubAsset": "CFDEquityFutureOrForward", "Asset": "ContractForDifference"},
    "CFD06": {"SubAsset": "CFDsEquityOption", "Asset": "ContractForDifference"},
    "CFD07": {"SubAsset": "OtherCFD", "Asset": "ContractForDifference"},
    "COM01": {"SubAsset": "MetalCommodityFutureOrForward", "Asset": "CommodityDerivative"},
    "COM02": {"SubAsset": "MetalCommodityOption", "Asset": "CommodityDerivative"},
    "COM03": {"SubAsset": "MetalCommoditySwap", "Asset": "CommodityDerivative"},
    "COM04": {"SubAsset": "EnergyCommodityFutureOrForward", "Asset": "CommodityDerivative"},
    "COM05": {"SubAsset": "EnergyCommodityOption", "Asset": "CommodityDerivative"},
    "COM06": {"SubAsset": "EnergyCommoditySwap", "Asset": "CommodityDerivative"},
    "COM07": {"SubAsset": "AgriculturalCommodityFutureOrForward", "Asset": "CommodityDerivative"},
    "COM08": {"SubAsset": "AgriculturalCommodityOption", "Asset": "CommodityDerivative"},
    "COM09": {"SubAsset": "AgriculturalCommoditySwap", "Asset": "CommodityDerivative"},
    "COM10": {"SubAsset": "Other Commodity Derivatives", "Asset": "CommodityDerivative"},
    "CRE01": {"SubAsset": "IndexCDS", "Asset": "CreditDerivative"},
    "CRE02": {"SubAsset": "SingleNameCDS", "Asset": "CreditDerivative"},
    "CRE03": {"SubAsset": "CDSIndexOption", "Asset": "CreditDerivative"},
    "CRE04": {"SubAsset": "SingleNameCDSOption", "Asset": "CreditDerivative"},
    "CRE05": {"SubAsset": "OtherCreditDerivative", "Asset": "EmissionAllowanceDerivative"},
    "DEA01": {"SubAsset": "DerivativeEmissionAllowance-EUA", "Asset": "EmissionAllowanceDerivative"},
    "DEA02": {"SubAsset": "DerivativeEmissionAllowance-EUAA", "Asset": "EmissionAllowanceDerivative"},
    "DEA03": {"SubAsset": "DerivativeEmissionAllowance-CER", "Asset": "EmissionAllowanceDerivative"},
    "DEA04": {"SubAsset": "DerivativeEmissionAllowance-ERU", "Asset": "EmissionAllowanceDerivative"},
    "DEA05": {"SubAsset": "OtherDerivativeEmissionAllowance", "Asset": "EmissionAllowanceDerivative"},
    "EA01": {"SubAsset": "EmissionAllowances-EUA", "Asset": "EmissionAllowance"},
    "EA02": {"SubAsset": "EmissionAllowances-EUAA", "Asset": "EmissionAllowance"},
    "EA03": {"SubAsset": "EmissionAllowances-CER", "Asset": "EmissionAllowance"},
    "EA04": {"SubAsset": "EmissionAllowances-ERU", "Asset": "EmissionAllowance"},
    "EA05": {"SubAsset": "OtherEmissionAllowance", "Asset": "EmissionAllowance"},
    "EQD01": {"SubAsset": "StockIndexOptions", "Asset": "EquityDerivative"},
    "EQD02": {"SubAsset": "StockIndexFuturesOrForwards", "Asset": "EquityDerivative"},
    "EQD03": {"SubAsset": "StockOptions", "Asset": "EquityDerivative"},
    "EQD04": {"SubAsset": "StockFuturesOrForward", "Asset": "EquityDerivative"},
    "EQD05": {"SubAsset": "StockDividendOption", "Asset": "EquityDerivative"},
    "EQD06": {"SubAsset": "StockDividendFuturesOrForward", "Asset": "EquityDerivative"},
    "EQD07": {"SubAsset": "DividendIndexOption", "Asset": "EquityDerivative"},
    "EQD08": {"SubAsset": "DividendIndexFutureOrForward", "Asset": "EquityDerivative"},
    "EQD09": {"SubAsset": "VolatilityIndexOption", "Asset": "EquityDerivative"},
    "EQD10": {"SubAsset": "VolatilityIndexFuturesOrForwards", "Asset": "EquityDerivative"},
    "EQD11": {"SubAsset": "ETFOption", "Asset": "EquityDerivative"},
    "EQD12": {"SubAsset": "ETFFuturesOrForward", "Asset": "EquityDerivative"},
    "EQD13": {"SubAsset": "Swap", "Asset": "EquityDerivative"},
    "EQD14": {"SubAsset": "PortfolioSwap", "Asset": "EquityDerivative"},
    "EQD15": {"SubAsset": "OtherEquityDerivative", "Asset": "EquityDerivative"},
    "ETC": {"SubAsset": "ETC", "Asset": "Bond"},
    "ETN": {"SubAsset": "ETN", "Asset": "Bond"},
    "FEX01": {"SubAsset": "NonDeliverableForward", "Asset": " ForeignExchangeDerivatives"},
    "FEX02": {"SubAsset": "DeliverableForward", "Asset": " ForeignExchangeDerivatives"},
    "FEX03": {"SubAsset": "NonDeliverableFXOption", "Asset": " ForeignExchangeDerivatives"},
    "FEX04": {"SubAsset": "DeliverableFXOption", "Asset": " ForeignExchangeDerivatives"},
    "FEX05": {"SubAsset": "NonDeliverableFXSwap", "Asset": " ForeignExchangeDerivatives"},
    "FEX06": {"SubAsset": "DeliverableFXSwap", "Asset": " ForeignExchangeDerivatives"},
    "FEX07": {"SubAsset": "FXFuture", "Asset": " ForeignExchangeDerivatives"},
    "FEX08": {"SubAsset": "OtherForeignExchangeDerivative", "Asset": " ForeignExchangeDerivatives"},
    "IRD01": {"SubAsset": "BondFuturesOrForward", "Asset": "InterestRateDerivative"},
    "IRD02": {"SubAsset": "BondOption", "Asset": "InterestRateDerivative"},
    "IRD03": {"SubAsset": "IRFuturesOrFRA", "Asset": "InterestRateDerivative"},
    "IRD04": {"SubAsset": "IROption", "Asset": "InterestRateDerivative"},
    "IRD05": {"SubAsset": "Swaption", "Asset": "InterestRateDerivative"},
    "IRD06": {"SubAsset": "SwapsAndFuturesOrForwardsOnSwap", "Asset": "InterestRateDerivative"},
    "IRD07": {"SubAsset": "OtherInterestRateDerivative", "Asset": "InterestRateDerivative"},
    "SDRV": {"SubAsset": "SecuritisedDerivative", "Asset": "SecuritisedDerivatives"},
    "SFP01": {"SubAsset": "StructuredFinanceProduct", "Asset": "StructuredFinanceProducts"},
    "SFP02": {"SubAsset": "StructuredFinanceProduct", "Asset": "StructuredFinanceProducts"},
}

def add_input_row(item:dict, row_dict:dict):
    pass


def  add_output_row(item:dict,row_dict:dict):
    pass



def parse_row(row: dict, data_map: dict) -> dict:
    # asset_tuple = product_codes.get()
    row_dict = dict([x.split('=') for x in row["Sub-class identification"].split('&')])
    row_dict.update(row)
    asset_tuple = product_codes.get(row_dict.get('SACID'))
    file_to_update = product_taxonomy.get((asset_tuple.get('Asset'),asset_tuple.get('asset_tuple.SubAsset')))
    file_metadata = files_to_generate.get(file_to_update)
    data = dict()
    inputs = file_metadata['inputs']
    for item in inputs:
            add_input_row(item, row_dict)
    outputs = file_metadata['inputs']
    for item in outputs:
            add_output_row(item, row_dict)
    pass


if __name__ == "__main__":

    data_map = dict()

    df_note = pd.read_excel(path, 'Explanatory note')
    df_results = pd.read_excel(path, 'Liquidity LIS SSTI results')

    columns = {}

    for index, row in df_results.iterrows():
        if index:
           # parse_row(dict(row), data_map)
            pass
        pass

    path_to_json = os.environ['DROIT_REFDATA']
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print(json_files)  # for me this prints ['foo.json']

x = 1
