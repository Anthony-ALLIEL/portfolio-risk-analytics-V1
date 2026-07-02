import csv
import performances
import risque_absolu
import risque_relatif
import ratios
import expositions
import contributions
import stress_liquidite

def main():
    # ==========================================
    # 1. IMPORTATION DES DONNÉES CSV
    # ==========================================
    portfolio_data = []
    with open("portfolio.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            portfolio_data.append(row)

    prices_data = []
    with open("prices.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            prices_data.append(row)

    # ==========================================
    # 2. CALCULS INTERMÉDIAIRES ET SÉRIES
    # ==========================================
    ptf_ret = performances.portfolio_return(prices_data, portfolio_data)
    bench_ret = performances.asset_return(prices_data, "SPY")
    relative_ret = performances.portfolio_relative_returns(ptf_ret, bench_ret)

    # ==========================================
    # 3. EXÉCUTION DE TOUS LES MODULES (A à G)
    # ==========================================
    # Module B
    ptf_vol_daily = risque_absolu.daily_volatility(ptf_ret)
    ptf_vol_ann = risque_absolu.annualized_volatility(ptf_ret)
    ptf_var_95 = risque_absolu.historical_var(ptf_ret, confidence=0.95)

    # Module C
    ptf_te = risque_relatif.tracking_error(relative_ret)
    ptf_beta = risque_relatif.portfolio_beta(ptf_ret, bench_ret)

    # Module D
    ptf_sharpe = ratios.sharpe_ratio(ptf_ret, risk_free_rate=0.03)
    ptf_ir = ratios.information_ratio(ptf_ret, bench_ret)

    # Module E
    sector_expos = expositions.calculate_expositions(portfolio_data, prices_data, "sector")
    country_expos = expositions.calculate_expositions(portfolio_data, prices_data, "country")
    top_positions = expositions.get_top_positions(portfolio_data, prices_data, n=10)

    # Module F
    perf_contribs = contributions.calculate_perf_contributions(portfolio_data, prices_data)
    risk_contribs = contributions.calculate_risk_contributions(portfolio_data, prices_data, ptf_ret)

    # Module G
    stress_scenarios = stress_liquidite.run_stress_tests(ptf_beta)
    liquidity_horizons = stress_liquidite.calculate_liquidity_horizons(portfolio_data, prices_data)

    # ==========================================
    # 4. AFFICHAGE DU RAPPORT CONSOLIDÉ FINAL
    # ==========================================
    print("\n" + "="*65)
    print("      RAPPORT DE RISK MANAGEMENT - Revue de Portefeuilles      ")
    print("="*65)
    
    # 📈 MODULE A
    print("\n📈 [MODULE A] PERFORMANCES JOURNALIÈRES (3 derniers jours)")
    print(f"  Portefeuille : { [f'{r*100:.2f}%' for r in ptf_ret[-3:]] }")
    print(f"  Benchmark    : { [f'{r*100:.2f}%' for r in bench_ret[-3:]] }")
    print(f"  Relatifs     : { [f'{r*100:.2f}%' for r in relative_ret[-3:]] }")
    
    # 🛡️ MODULE B
    print("\n🛡️ [MODULE B] RISQUE ABSOLU DU PORTEFEUILLE")
    print(f"  Volatilité Journalière : {ptf_vol_daily * 100:.2f}%")
    print(f"  Volatilité Annualisée  : {ptf_vol_ann * 100:.2f}%")
    print(f"  VaR Historique (95%)   : {ptf_var_95 * 100:.2f}%")
    
    # 📊 MODULE C
    print("\n📊 [MODULE C] RISQUE RELATIF VS BENCHMARK")
    print(f"  Tracking Error (Ann.)  : {ptf_te * 100:.2f}%")
    print(f"  Beta du Portefeuille   : {ptf_beta:.2f}")
    
    # 🏆 MODULE D
    print("\n🏆 [MODULE D] RATIOS DE PERFORMANCE (QUALITÉ DE GESTION)")
    print(f"  Ratio de Sharpe (Rf=3%): {ptf_sharpe:.2f}")
    print(f"  Ratio d'Information    : {ptf_ir:.2f}")
    
    # 🌍 MODULE E
    print("\n🌍 [MODULE E] CARTOGRAPHIE DES EXPOSITIONS (ALLOCATION)")
    print("  Répartition Sectorielle :")
    for sec, weight in sector_expos.items():
        print(f"    - {sec:<12} : {weight*100:.2f}%")
    print("  Répartition Géographique :")
    for country, weight in country_expos.items():
        print(f"    - {country:<12} : {weight*100:.2f}%")
        
    # 🧮 MODULE F
    print("\n🧮 [MODULE F] CONTRIBUTIONS SOUSTREITRES (EULER ALLOCATION)")
    print("  Détail par actif :")
    for asset, weight in top_positions:
        p_contrib = perf_contribs.get(asset, 0.0)
        r_contrib_raw = risk_contribs.get(asset, 0.0)
        # Part du risque en % (MCTR normalisé par la volatilité quotidienne globale)
        r_contrib_pct = (r_contrib_raw / ptf_vol_daily) * 100 if ptf_vol_daily > 0 else 0.0
        print(f"    - {asset:<4} (Poids: {weight*100:5.2f}%) : Perf = {p_contrib*100:+6.2f}% | Part du Risque = {r_contrib_pct:6.2f}%")
        
    # 💥 MODULE G
    print("\n💥 [MODULE G] STRESS TESTING HISTORIQUE & LIQUIDITÉ MULTI-HORIZONS")
    print("  Scénarios de Crises Historiques (Impact estimé via Beta) :")
    for scenario_name, impact in stress_scenarios.items():
        print(f"    - {scenario_name:<42} : {impact*100:+.2f}% de la valeur du PTF")
        
    print("  Profil de Liquidité Réglementaire (% du PTF total liquidable à 10% ADV) :")
    for horizon, pct in liquidity_horizons.items():
        print(f"    - À {horizon:<10} : {pct:.2f}% du portefeuille liquide")
        
    print("\n" + "="*65 + "\n")

if __name__ == "__main__":
    main()