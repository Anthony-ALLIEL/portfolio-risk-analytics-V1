from expositions import get_last_prices

def run_stress_tests(portfolio_beta):
    """
    Simule l'impact de véritables crises historiques majeures sur le portefeuille.
    """
    scenarios = {
        "Bulle Internet (2000 - Marché -45%)": -0.45,
        "Crise des Subprimes (2008 - Marché -50%)": -0.50,
        "Krach COVID-19 (2020 - Marché -30%)": -0.30
    }
    
    stress_results = {}
    for name, market_shock in scenarios.items():
        stress_results[name] = portfolio_beta * market_shock
        
    return stress_results


def calculate_liquidity_horizons(portfolio_data, prices_data):
    """
    Calcule le pourcentage du portefeuille global liquidable à 1 jour, 2 jours 
    et 1 semaine (5 jours de trading), en respectant la règle des 10% ADV.
    """
    last_prices = get_last_prices(prices_data)
    
    # 1. Calcul de la valeur monétaire de chaque ligne et de la valeur totale
    positions_values = {}
    total_portfolio_value = 0.0
    for row in portfolio_data:
        ticker = row['asset']
        shares = float(row['shares'])
        price = last_prices.get(ticker, 0.0)
        value = shares * price
        positions_values[ticker] = value
        total_portfolio_value += value

    # Horizons demandés (en jours de trading : 1 semaine = 5 jours ouverts)
    horizons = {
        "1 Jour": 1,
        "2 Jours": 2,
        "1 Semaine": 5
    }
    
    liquidity_by_horizon = {}
    
    # 2. Pour chaque horizon, on calcule la part de valeur totale liquidable
    for horizon_name, num_days in horizons.items():
        liquid_value_at_horizon = 0.0
        
        for row in portfolio_data:
            ticker = row['asset']
            shares = float(row['shares'])
            adv = float(row['adv'])
            price = last_prices.get(ticker, 0.0)
            
            # Quantité d'actions max vendables sur cet horizon
            max_actions_liquidable = num_days * (0.10 * adv)
            
            # On ne peut pas liquider plus d'actions que ce que l'on possède
            actions_effectively_liquidated = min(shares, max_actions_liquidable)
            
            # Valeur financière liquidée pour cet actif
            liquid_value_at_horizon += actions_effectively_liquidated * price
            
        # % du portefeuille total liquidable à cet horizon
        pct_liquidable = (liquid_value_at_horizon / total_portfolio_value) * 100
        liquidity_by_horizon[horizon_name] = pct_liquidable
        
    return liquidity_by_horizon