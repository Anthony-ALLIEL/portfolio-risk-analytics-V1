# On importe daily_volatility pour le Beta et annualized_volatility pour la TE
from risque_absolu import daily_volatility, annualized_volatility

def tracking_error(relative_returns_list):
    """
    Calcule la Tracking Error annualisée.
    """
    return annualized_volatility(relative_returns_list)
    
def portfolio_covariance(list_a, list_b):
    """
    Calcule la covariance historique entre deux séries de rendements.
    """
    moyenne_a = sum(list_a) / len(list_a)
    moyenne_b = sum(list_b) / len(list_b)

    somme_prod_list = 0
    for i in range(len(list_a)):
        somme_prod_list += (list_a[i] - moyenne_a) * (list_b[i] - moyenne_b)
        
    covariance = somme_prod_list / len(list_a)
    return covariance

def portfolio_beta(ptf_returns, bench_returns):
    """
    Calcule le Beta du portefeuille par rapport au benchmark.
    """
    # Utilisation obligatoire de la volatilité JOURNALIÈRE élevée au carré
    variance_bench = daily_volatility(bench_returns) ** 2
    return portfolio_covariance(ptf_returns, bench_returns) / variance_bench