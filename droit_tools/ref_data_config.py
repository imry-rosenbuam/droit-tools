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
    "CFD06": {"SubAsset": "CFDEquityOption", "Asset": "ContractForDifference"},
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
    "COM10": {"SubAsset": "Other Commodity Derivative", "Asset": "CommodityDerivative"},
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
    "EA01": {"SubAsset": "EmissionAllowance-EUA", "Asset": "EmissionAllowance"},
    "EA02": {"SubAsset": "EmissionAllowance-EUAA", "Asset": "EmissionAllowance"},
    "EA03": {"SubAsset": "EmissionAllowance-CER", "Asset": "EmissionAllowance"},
    "EA04": {"SubAsset": "EmissionAllowance-ERU", "Asset": "EmissionAllowance"},
    "EA05": {"SubAsset": "OtherEmissionAllowance", "Asset": "EmissionAllowance"},
    "EQD01": {"SubAsset": "StockIndexOption", "Asset": "EquityDerivative"},
    "EQD02": {"SubAsset": "StockIndexFutureOrForward", "Asset": "EquityDerivative"},
    "EQD03": {"SubAsset": "StockOption", "Asset": "EquityDerivative"},
    "EQD04": {"SubAsset": "StockFutureOrForward", "Asset": "EquityDerivative"},
    "EQD05": {"SubAsset": "StockDividendOption", "Asset": "EquityDerivative"},
    "EQD06": {"SubAsset": "StockDividendFuturesOrForward", "Asset": "EquityDerivative"},
    "EQD07": {"SubAsset": "DividendIndexOption", "Asset": "EquityDerivative"},
    "EQD08": {"SubAsset": "DividendIndexFutureOrForward", "Asset": "EquityDerivative"},
    "EQD09": {"SubAsset": "VolatilityIndexOption", "Asset": "EquityDerivative"},
    "EQD10": {"SubAsset": "VolatilityIndexFutureOrForward", "Asset": "EquityDerivative"},
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
    "IRD01": {"SubAsset": "BondFutureOrForward", "Asset": "InterestRateDerivative"},
    "IRD02": {"SubAsset": "BondOption", "Asset": "InterestRateDerivative"},
    "IRD03": {"SubAsset": "IRFuturesOrFRA", "Asset": "InterestRateDerivative"},
    "IRD04": {"SubAsset": "IROption", "Asset": "InterestRateDerivative"},
    "IRD05": {"SubAsset": "Swaption", "Asset": "InterestRateDerivative"},
    "IRD06": {"SubAsset": "SwapAndFutureOrForwardOnSwap", "Asset": "InterestRateDerivative"},
    "IRD07": {"SubAsset": "OtherInterestRateDerivative", "Asset": "InterestRateDerivative"},
    "SDRV": {"SubAsset": "SecuritisedDerivative", "Asset": "SecuritisedDerivatives"},
    "SFP01": {"SubAsset": "StructuredFinanceProduct", "Asset": "StructuredFinanceProducts"},
    "SFP02": {"SubAsset": "StructuredFinanceProduct", "Asset": "StructuredFinanceProducts"},
}

swap_codes = {
    'XFSC': "FixedFloatSingleCurrency",
    'IFSC': "InflationSingleCurrency",
    'OSSC': "OISSingleCurrency"
}

bond_term_code = {
'ST':	'ShortTerm',
'MT':	'MediumTerm',
'LT':	'LongTerm',
'ULT':	'UltraLongTerm'
}
