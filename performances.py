import csv

def asset_return(prices_list, asset_name):
    """
    Calcule les rendements journaliers d'un actif spécifique (ou du benchmark).
    Prend en entrée :
      - prices_list : la liste des dictionnaires de prix issus du CSV
      - asset_name : le nom de la colonne de l'actif (ex: 'AAPL' ou 'SPY')
    Retourne : une liste de floats (les rendements journaliers de cet actif)
    """
    # Étape A : On extrait la liste des prix de cet actif sous forme de chiffres (floats)
    prices_for_asset = []
    for row in prices_list:
        prices_for_asset.append(float(row[asset_name]))
        
    # Étape B : On applique la formule du rendement journalier : (Pt - Pt-1) / Pt-1
    returns = []
    for i in range(1, len(prices_for_asset)):
        return_as_float = (prices_for_asset[i] - prices_for_asset[i-1]) / prices_for_asset[i-1]
        returns.append(return_as_float)
        
    return returns


def portfolio_return(prices_list, portfolio_composition):
    """
    Calcule les rendements journaliers globaux du portefeuille consolidé.
    Prend en entrée :
      - prices_list : la liste des dictionnaires de prix issus du CSV
      - portfolio_composition : la liste des dictionnaires du portefeuille issus du CSV
    Retourne : une liste de floats (les rendements journaliers du ptf global)
    """
    # Étape A : On calcule l'historique de la valeur monétaire totale du portefeuille jour après jour
    portfolio_prices = []
    for row in prices_list:
        total_value_today = 0.0
        
        for asset_row in portfolio_composition:
            asset_name = asset_row["asset"]
            shares = float(asset_row["shares"])
            
            # On va chercher le prix de l'actif du jour, on multiplie par la quantité et on cumule
            total_value_today += float(row[asset_name]) * shares
            
        portfolio_prices.append(total_value_today)
        
    # Étape B : On applique la formule du rendement journalier sur la valeur globale du portefeuille
    returns = []
    for i in range(1, len(portfolio_prices)):
        return_as_float = (portfolio_prices[i] - portfolio_prices[i-1]) / portfolio_prices[i-1]
        returns.append(return_as_float)
        
    return returns


def portfolio_relative_returns(ptf_returns, bench_returns):
    """
    Calcule les rendements relatifs journaliers (excess returns) du portefeuille par rapport au benchmark.
    Prend en entrée :
      - ptf_returns : la liste des rendements du portefeuille
      - bench_returns : la liste des rendements du benchmark
    Retourne : une liste de floats (les rendements relatifs)
    """
    # Sécurité Risk Management : On valide que les historiques ont la même longueur
    if len(ptf_returns) != len(bench_returns):
        raise ValueError("Les listes de rendements du portefeuille et du benchmark doivent avoir la même longueur.")
        
    returns = []
    # On parcourt chaque journée pour faire la différence arithmétique
    for i in range(len(ptf_returns)):
        return_as_float = ptf_returns[i] - bench_returns[i]
        returns.append(return_as_float)
        
    return returns