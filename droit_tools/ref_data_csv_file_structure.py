csv_file_prefix = "esma_ref_data_"

# associate a class to a file
product_taxonomy = {
    'CommodityDerivative': ['commodity_derivative'],
    'EquityDerivative': ['equity_derivative_isin', 'equity_derivative_stock_index'],
    "InterestRateDerivative": ["interest_rate_derivative"]
}

# associate an asset and sub-asset to a file
subasset_taxonomy = {
    ('Bond', 'ETN'): 'bond_etc_etn',
    ('Bond', 'ETC'): 'bond_etc_etn',
}

standard_output = ["preTradeSSTI", "preTradeLIS",
                   "postTradeSSTI", "postTradeLIS",
                   "liquidMarketForProduct"]
bond_output = ["preTradeSSTI", "preTradeLIS",
               "postTradeSSTI", "postTradeLIS"]

# let us enumerate to which files we will be segregating our records on to
# inputs asset_code is unique key as it will reinterpreted to two as it will also include asset and sub-asset
# keys for inputs or outputs are column name and then esma code for column (name,esma code )
files_to_generate = dict(
    bond_etc_etn=dict(inputs=["esmaAssetClass", "esmaSubAssetClass", "isin"], outputs=standard_output),
    bond_thresholds=dict(inputs=["esmaAssetClass", "esmaSubAssetClass"],
                         outputs=bond_output),
    bond_future=dict(inputs=[], outputs=[], codes=[]),
    cfd_bond_future=dict(inputs=[], outputs=[], codes=[]),
    commodity_derivative=dict(
        inputs=["esmaAssetClass", "esmaSubAssetClass", "metalType", "underlyingMetal", "energyType", "underlyingEnergy",
                "loadType", "deliveryCashSettlementLocation", "agriculturalProduct", "underlyingAgriculturalCommodity",
                "notionalCurrency", "residualTerm@commodity_derivative"], outputs=standard_output),
    cfd_commodity=dict(inputs=[], outputs=[]),
    credit_derivative_non_option=dict(inputs=[], outputs=[]),
    credit_derivative_option=dict(inputs=[], outputs=[]),
    emission_allowance=dict(inputs=[], outputs=[]),
    emission_allowance_derivative=dict(inputs=[], outputs=[]),
    equity_derivative_isin=dict(inputs=["esmaAssetClass", "esmaSubAssetClass", 'underlierIsin@eq_derivative'],
                                outputs=standard_output),
    equity_derivative_stock_index=dict(
        inputs=["esmaAssetClass", "esmaSubAssetClass", 'equityDerivativeUnderlyingInstrument'],
        outputs=standard_output),
    interest_rate_derivative=dict(inputs=["esmaAssetClass", "esmaSubAssetClass", "underlierIsin@ir_derivative",
                                          "currency@ir_derivative", "underlyingInterestRate", "underlyingIRTerm",
                                          "underlyingBondIssuer", "underlyingBondTerm", "residualTerm@ir_derivative"],
                                  outputs=standard_output)
)

# feasible codes, as ESMA do include names with & in the name of some indices, let us remeber what is a feasible code
codes = [
    'DCSL',
    'UIN',
    'UIC',
    'ISIN',
    "SSTI pre-trade",
    "SSTI post-trade",
    "LIS pre-trade",
    "LIS post-trade",
    "Liquidity",
    'BP',
    'SP',
    'FSP',
    'DCSL',
    'CNC',
    'TTMB',
    'SACID',
    'UTYP',
    'CURR1',
    'CURR2',
    'IOUB',
    'TOUB'
]
# column taxonomy
# each column -> name module type operator ( null is equality ) code ( what we are populating from )
# giving opearotr the value tenor will be split unto two columns one with GT and one with MAX
# @ suffix is given to column names that can appear in different tables and thus we need to diffrentiate them
column_taxonomy = {
    "esmaAssetClass": {
        "module": "esma_taxonomy_translation",
        "type": "STRING",
        "default": '',
        'code': 'ASSET'
    },
    "esmaSubAssetClass": {
        "module": "esma_taxonomy_translation",
        "type": "STRING",
        "default": '',
        'code': 'SUBASSET'
    },
    "isin": {
        "module": "trade",
        "type": "STRING",
        "default": 0,
        'code': 'ISIN'
    },
    "preTradeSSTI": {
        "module": "output",
        "type": "INTEGER",
        "default": 0,
        'code': "SSTI pre-trade"
    },
    "postTradeSSTI": {
        "module": "output",
        "type": "INTEGER",
        "default": 0,
        'code': "SSTI post-trade"
    },
    "preTradeLIS": {
        "module": "output",
        "type": "INTEGER",
        "default": 0,
        'code': "LIS pre-trade"
    },
    "postTradeLIS": {
        "module": "output",
        "type": "INTEGER",
        "default": 0,
        'code': "LIS post-trade"
    },
    "liquidMarketForProduct": {
        "module": "output",
        "type": "BOOLEAN",
        "default": 'false',
        'code': 'Liquidity'
    },
    "mifidCommodityType": {
        "module": "trade",
        "type": "STRING",
        "default": 'NA',
        'code': 'BP'
    },
    "mifidEnergyType": {
        "module": "trade",
        "type": "STRING",
        "default": 'NA',
        'code': 'SP',

    },
    "underlyingEnergy": {
        "module": "trade",
        "type": "STRING",
        "default": 'NA',
        'code': 'FSP',
        'depend': {'col': 'energyType',
                   'vals': ['ELEC'],
                   'op': 'not exists',
                   'sub-asset': ['EnergyCommodityFutureOrForward', 'EnergyCommodityOption']}
    },
    "metalType": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': "SP",
        'depend': {'col': 'esmaSubAssetClass',
                   'vals': ['MetalCommodityFutureOrForward', 'MetalCommodityOption'],
                   'op': 'exists'}
    },
    "underlyingMetal": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': "FSP",
        'depend': {'col': 'esmaSubAssetClass',
                   'vals': ['MetalCommodityFutureOrForward', 'MetalCommodityOption'],
                   'op': 'exists'}
    },
    "energyType": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': "SP",
        'depend': {'col': 'esmaSubAssetClass',
                   'vals': ['EnergyCommodityFutureOrForward', 'EnergyCommodityOption'],
                   'op': 'exists'}
    },
    "loadType": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': "FSP",
        'depend': {'col': 'energyType',
                   'vals': ['ELEC'],
                   'op': 'exists'}
    },
    "deliveryCashSettlementLocation": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': "DCSL"
    },
    "agriculturalProduct": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': "SP",
        'depend': {'col': 'esmaSubAssetClass',
                   'vals': ['AgriculturalCommodityFutureOrForward', 'AgriculturalCommodityOption'],
                   'op': 'exists'}
    },
    "underlyingAgriculturalCommodity": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': "FSP",
        'depend': {'col': 'esmaSubAssetClass',
                   'vals': ['AgriculturalCommodityFutureOrForward', 'AgriculturalCommodityOption'],
                   'op': 'exists'}
    },
    "notionalCurrency": {
        "module": "commodity_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': 'CNC'
    },
    "residualTerm@commodity_derivative": {
        "module": "commodity_seg_criteria",
        "type": "TENOR",
        "default": 'NA',
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX,
        'code': 'TTMB'
    },
    "underlyingIndex@credit_derivative": {
        "module": "credit_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': 'TTMB'
    },
    "underlyingReferenceEntity": {
        "module": "credit_seg_criteria",
        "type": "STRING",
        "default": 'NA',
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
        "default": 'NA',
        'code': 'UIN',
        'mandatory': True
    },
    "underlierIsin@ir_derivative": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': 'UIC',
        'extra': ['LIST']
    },
    "underlierIsin@eq_derivative": {
        "module": "trade",
        "type": "STRING",
        "default": 'NA',
        'code': 'UIC',
        'mandatory': True,
        'extra': ['LIST']
    },
    "currency@ir_derivative": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        "code": "CURR1"
    },
    "underlyingInterestRate": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        "code": 'UIR'
    },
    "underlyingIRTerm": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": None,
        'code': 'IRTC'
    },
    "underlyingBondIssuer": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': 'IOUB'
    },
    "underlyingBondTerm": {
        "module": "interest_rate_seg_criteria",
        "type": "STRING",
        "default": 'NA',
        'code': 'TOUB'
    },
    "residualTerm@ir_derivative": {
        "module": "interest_rate_seg_criteria",
        "type": "TENOR",
        "default": None,
        "code": "TTMB",
        "operator": "TENOR",  # tenor will be split unto two columns one with GT and one with MAX
    }
}
