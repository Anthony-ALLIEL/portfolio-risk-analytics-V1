def get_last_prices(prices_data):
    """
    Extrait le dernier prix connu pour chaque actif à partir de la structure horizontale de prices_data.
    Retourne un dictionnaire : { 'AAPL': 190.0, 'MSFT': 433.0, ... }
    """
    # On récupère la toute dernière ligne de l'historique (les prix les plus récents)
    last_row = prices_data[-1]
    
    last_prices = {}
    # On parcourt chaque colonne de cette ligne
    for key, value in last_row.items():
        if key != 'date':  # On ignore la colonne de la date
            last_prices[key] = float(value)
            
    return last_prices


def calculate_expositions(portfolio_data, prices_data, axis):
    """
    Calcule l'exposition du portefeuille (en %) selon l'axe choisi ('sector' ou 'country').
    """
    last_prices = get_last_prices(prices_data)
    
    positions_values = {}
    total_portfolio_value = 0.0
    
    for row in portfolio_data:
        ticker = row['asset']
        shares = float(row['shares'])
        price = last_prices.get(ticker, 0.0)
        
        value = shares * price
        positions_values[ticker] = value
        total_portfolio_value += value

    expos = {}
    for row in portfolio_data:
        ticker = row['asset']
        key = row[axis]
        
        asset_weight = positions_values[ticker] / total_portfolio_value
        
        if key in expos:
            expos[key] += asset_weight
        else:
            expos[key] = asset_weight

    return expos


def get_top_positions(portfolio_data, prices_data, n=10):
    """
    Retourne les n plus grosses positions du portefeuille triées par poids décroissant.
    """
    last_prices = get_last_prices(prices_data)
    
    positions_values = {}
    total_portfolio_value = 0.0
    
    for row in portfolio_data:
        ticker = row['asset']
        shares = float(row['shares'])
        price = last_prices.get(ticker, 0.0)
        
        value = shares * price
        positions_values[ticker] = value
        total_portfolio_value += value
        
    raw_positions = []
    for row in portfolio_data:
        ticker = row['asset']
        asset_weight = positions_values[ticker] / total_portfolio_value
        raw_positions.append((ticker, asset_weight))
        
    sorted_positions = sorted(raw_positions, key=lambda x: x[1], reverse=True)
    return sorted_positions[:n]