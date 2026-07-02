from risque_relatif import tracking_error
from risque_absolu import annualized_volatility
from performances import portfolio_relative_returns

def sharpe_ratio(ptf_returns, risk_free_rate=0.03):
    """
    Calcule le Ratio de Sharpe (Rendement Ptf Ann. - Taux sans risque) / Vol Ptf Ann.
    """
    moyenne_return = (1 + (sum(ptf_returns) / len(ptf_returns))) ** 252 - 1
    return (moyenne_return - risk_free_rate) / annualized_volatility(ptf_returns)


def information_ratio(ptf_returns, bench_returns):
    """
    Calcule le Ratio d'Information (Rendement Ptf Ann. - Rendement Bench Ann.) / TE Ann.
    """
    # 1. Calcul des rendements annualisés des deux côtés
    ptf_ann_return = (1+(sum(ptf_returns) / len(ptf_returns))) ** 252 - 1
    bench_ann_return = (1+(sum(bench_returns) / len(bench_returns))) ** 252 - 1
    
    # 2. Calcul de la surperformance
    excess_return = ptf_ann_return - bench_ann_return
    
    # 3. Calcul des rendements relatifs via votre fonction importée du Module A
    rel_returns = portfolio_relative_returns(ptf_returns, bench_returns)
    
    # 4. Ratio d'Information = Surperformance / Tracking Error
    return excess_return / tracking_error(rel_returns)