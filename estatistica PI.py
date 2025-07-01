
import pandas as pd
from scipy.stats import pearsonr

# 1. Carregar os dados a partir de um CSV
df = pd.read_csv('d:/fatec/Projeto Integrador/data-1745622189613.csv')  # Substitua pelo nome correto do arquivo

# 2. Densidade Calórica Estimada (sem uso de média)
df['Peso_estimado'] = df[['Fat', 'Protein', 'Carbohydrates']].sum(axis=1)
df['Densidade_Calorica'] = df['Caloric Value'] / df['Peso_estimado']
densidade_calorica_top = df[['food', 'Densidade_Calorica']].dropna().sort_values(by='Densidade_Calorica', ascending=False).head(10)

# 3. Relação Proteína / Gordura ajustada
epsilon = 0.01
df['PF_ratio'] = df['Protein'] / (df['Fat'] + epsilon)
pf_ranking = df[['food', 'PF_ratio']].dropna().sort_values(by='PF_ratio', ascending=False).head(10)

# 4. Correlação açúcar vs calorias
sugar = df['Sugars'].fillna(0)
calories = df['Caloric Value'].fillna(0)
correl_sugar_cal, pval_sugar_cal = pearsonr(sugar, calories)

# 5. Dietas low-carb (ranking direto e proporção)
df['Carb_ratio'] = df['Carbohydrates'] / (df['Fat'] + df['Protein'] + df['Carbohydrates'])
lowcarb_direct = df[['food', 'Carbohydrates']].dropna().sort_values(by='Carbohydrates').head(10)
lowcarb_ratio = df[['food', 'Carb_ratio']].dropna().sort_values(by='Carb_ratio').head(10)

# 6. Ranking combinado (se existir coluna 'category')
if 'category' in df.columns:
    df['rank_density'] = df['Densidade_Calorica'].rank(ascending=False)
    df['rank_pf'] = df['PF_ratio'].rank(ascending=False)
    df['rank_carb'] = df['Carb_ratio'].rank(ascending=True)
    df['score_total'] = df[['rank_density', 'rank_pf', 'rank_carb']].sum(axis=1)
    best_category_items = df[['food', 'category', 'score_total']].dropna().sort_values('score_total').head(10)
else:
    best_category_items = None

# 7. Exibição dos resultados (ou salvar/exportar)
print("Top 10 Alimentos com Maior Densidade Calórica:")
print(densidade_calorica_top)

print("\nTop 10 Alimentos com Melhor Relação Proteína/Gordura:")
print(pf_ranking)

print("\nTop 10 Alimentos Low-Carb (Carboidrato Absoluto):")
print(lowcarb_direct)

print("\nTop 10 Alimentos Low-Carb (Proporção de Carboidrato):")
print(lowcarb_ratio)

if best_category_items is not None:
    print("\nTop 10 Alimentos com Melhor Score Combinado por Categoria:")
    print(best_category_items)

# 8. Exibir a correlação açúcar vs calorias
print(f"\nCorrelação entre açúcar e calorias: {correl_sugar_cal:.3f} (p-valor: {pval_sugar_cal:.3f})")