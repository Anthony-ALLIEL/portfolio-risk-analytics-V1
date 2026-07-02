def daily_volatility(returns_list):
    """
    Calcule la volatilité journalière (écart-type) d'une série de rendements.
    """
    if len(returns_list) < 2:
        raise ValueError("La liste doit contenir au moins 2 rendements.")
        
    moyenne = sum(returns_list) / len(returns_list)

    somme_excess = 0
    for r in returns_list:
        somme_excess += (r - moyenne) ** 2
        
    ecart_type = (somme_excess / len(returns_list)) ** 0.5
    return ecart_type


def annualized_volatility(returns_list):
    """
    Annualise la volatilité journalière (base 252 jours).
    """
    return daily_volatility(returns_list) * (252) ** 0.5


def historical_var(returns_list, confidence=0.95):
    """
    Calcule la Value at Risk (VaR) Historique au niveau de confiance spécifié.
    Retourne le rendement critique (négatif) marquant le début de la zone de perte extrême.
    """
    if not returns_list:
        raise ValueError("La liste de rendements ne peut pas être vide.")
        
    # Étape 1 : Tri par ordre croissant (du pire au meilleur rendement)
    sorted_list = sorted(returns_list)
    
    # Étape 2 : Calcul de l'index de coupure selon le niveau de confiance
    i = int(len(sorted_list) * (1 - confidence))
    
    # Étape 3 : Extraction de la VaR
    return sorted_list[i]

