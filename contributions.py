from risque_relatif import portfolio_covariance
from risque_absolu import daily_volatility
from expositions import get_last_prices

def calculate_perf_contributions(portfolio_data, prices_data):
    """
    Calcule la contribution de chaque actif à la performance totale.
    """
    last_prices = get_last_prices(prices_data)
    
    # 1. Calculer les poids (comme dans le module E)
    positions_values = {}
    total_value = 0.0
    for row in portfolio_data:
        ticker = row['asset']
        shares = float(row['shares'])
        positions_values[ticker] = shares * last_prices.get(ticker, 0.0)
        total_value += positions_values[ticker]
        
    contributions_perf = {}
    
    # 2. Pour chaque actif, calculer : Poids * Rendement Global de l'actif
    for row in portfolio_data:
        ticker = row['asset']
        weight = positions_values[ticker] / total_value
        
        # Rendement global de l'actif entre le premier et le dernier jour du CSV
        initial_price = float(prices_data[0][ticker])
        final_price = float(prices_data[-1][ticker])
        asset_return = (final_price - initial_price) / initial_price
        
        # Calculer la contribution et stockez-la dans contributions_perf
        contributions_perf[ticker] = weight * asset_return
        
    return contributions_perf


def calculate_risk_contributions(portfolio_data, prices_data, ptf_returns):
    """
    Calcule la contribution de chaque actif à la volatilité journalière du portefeuille.
    """
    last_prices = get_last_prices(prices_data)
    
    # (Calcul des poids identique...)
    positions_values = {}
    total_value = 0.0
    for row in portfolio_data:
        ticker = row['asset']
        positions_values[ticker] = float(row['shares']) * last_prices.get(ticker, 0.0)
        total_value += positions_values[ticker]
        
    ptf_vol_daily = daily_volatility(ptf_returns)
    contributions_risk = {}
    
    for row in portfolio_data:
        ticker = row['asset']
        weight = positions_values[ticker] / total_value
        
        # 1. Extraire l'historique des rendements de CET actif (Module A)
        asset_returns = []
        for i in range(1, len(prices_data)):
            prev_p = float(prices_data[i-1][ticker])
            cur_p = float(prices_data[i][ticker])
            asset_returns.append((cur_p - prev_p) / prev_p)
            
        # 2. Calculer la covariance entre les rendements de l'actif et ceux du ptf
        cov_asset_ptf = portfolio_covariance(asset_returns, ptf_returns)
        
        # 3. Formule : (Poids * Cov) / Vol_Quotidienne_Ptf
        contributions_risk[ticker] = (weight * cov_asset_ptf) / ptf_vol_daily
        
    return contributions_risk