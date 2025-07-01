# -*- coding: utf-8 -*-
"""
Análise Estatística de Dados Nutricionais

Este script realiza uma série de análises em um dataset de alimentos,
gerando gráficos e arquivos com os resultados.

Para funcionar, este script precisa do arquivo 'data-1745622189613.csv'
na mesma pasta onde ele for executado.

As análises incluem:
1. Distribuição e Variabilidade Calórica por Grupo de Alimentos (Boxplot + ANOVA).
2. Correlação entre Macronutrientes e Calorias (Heatmap).
3. Impacto da Relação Proteína/Gordura na Nutrição (Barplot).
4. Correlação de Micronutrientes com um "Health Score" (Barplot).
5. Clusterização de Alimentos por Perfil Nutricional (K-Means + PCA).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import os

# --- CONFIGURAÇÕES GERAIS ---

# Estilo dos gráficos
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (14, 9)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12

# Diretório para salvar os gráficos e resultados
# Cria a pasta 'analises_nutricionais_output' no mesmo local do script
output_dir = 'analises_nutricionais_output'
os.makedirs(output_dir, exist_ok=True)

# --- CARREGAMENTO E LIMPEZA INICIAL DOS DADOS ---

# Carregar os dados a partir do CSV local
try:
    df = pd.read_csv('data-1745622189613.csv')
except FileNotFoundError:
    print("Erro: Arquivo 'data-1745622189613.csv' não encontrado.")
    print("Por favor, certifique-se de que o arquivo CSV está na mesma pasta que este script.")
    exit()

# Preencher valores nulos nos macronutrientes com 0 para evitar erros de cálculo
macros = ['Caloric Value', 'Fat', 'Protein', 'Carbohydrates', 'Sugars']
df[macros] = df[macros].fillna(0)

print("Dataset carregado com sucesso.")
print(f"Número de linhas: {df.shape[0]}")
print(f"Número de colunas: {df.shape[1]}")

# --- ANÁLISE 1: DISTRIBUIÇÃO CALÓRICA POR GRUPO DE ALIMENTOS ---

print("\nIniciando Análise 1: Distribuição Calórica por Grupo...")

# Categorizar alimentos baseado em palavras-chave nos nomes
df['category'] = 'Outros'
categorias = {
    'cheese': 'Queijos',
    'butter': 'Gorduras',
    'jam': 'Doces',
    'honey': 'Doces',
    'peanut': 'Pastas',
    'spread': 'Pastas'
}

for palavra, categoria in categorias.items():
    df.loc[df['food'].str.contains(palavra, case=False, na=False), 'category'] = categoria

# Boxplot das calorias por categoria
plt.figure(figsize=(14, 9))
sns.boxplot(data=df, x='category', y='Caloric Value', palette='pastel')
plt.title('Distribuição de Calorias por Categoria de Alimento')
plt.ylabel('Valor Calórico (kcal)')
plt.xlabel('Categoria')
plt.tight_layout()
plt.savefig(f"{output_dir}/boxplot_calorias_por_categoria.png")
plt.close()

# Análise de Variância (ANOVA)
categorias_validas = df['category'].unique()
grupos_caloricos = [df[df['category'] == cat]['Caloric Value'] for cat in categorias_validas]
f_val, p_val = stats.f_oneway(*grupos_caloricos)

with open(f"{output_dir}/resultado_anova_calorias.txt", "w") as f:
    f.write("Resultado da Análise de Variância (ANOVA) para Calorias por Categoria\n")
    f.write("="*70 + "\n")
    f.write(f"Valor-F: {f_val:.4f}\n")
    f.write(f"Valor-p: {p_val:.4f}\n")
    if p_val < 0.05:
        f.write("\nConclusão: Como o valor-p é menor que 0.05, rejeitamos a hipótese nula. Existem diferenças estatisticamente significativas nos valores calóricos entre as categorias de alimentos.")
    else:
        f.write("\nConclusão: Como o valor-p não é menor que 0.05, não podemos rejeitar a hipótese nula. Não há evidências de diferenças estatisticamente significativas nos valores calóricos entre as categorias.")

print("Análise 1 concluída. Gráfico e resultado da ANOVA salvos.")

# --- ANÁLISE 2: CORRELAÇÃO ENTRE MACRONUTRIENTES E CALORIAS ---

print("\nIniciando Análise 2: Correlação de Macronutrientes...")

# Selecionar colunas relevantes
cols_corr = ['Caloric Value', 'Fat', 'Protein', 'Carbohydrates', 'Sugars']
matriz_corr = df[cols_corr].corr()

# Heatmap da correlação
plt.figure(figsize=(10, 8))
sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Mapa de Calor da Correlação entre Macronutrientes e Calorias')
plt.tight_layout()
plt.savefig(f"{output_dir}/heatmap_correlacao_macronutrientes.png")
plt.close()

print("Análise 2 concluída. Heatmap de correlação salvo.")

# --- ANÁLISE 3: IMPACTO DA RELAÇÃO PROTEÍNA/GORDURA (PF RATIO) ---

print("\nIniciando Análise 3: Relação Proteína/Gordura...")

# Calcular PF Ratio (adicionando epsilon para evitar divisão por zero)
epsilon = 0.01
df['PF_ratio'] = df['Protein'] / (df['Fat'] + epsilon)
df['PF_quartil'] = pd.qcut(df['PF_ratio'], 4, labels=['Q1 (Baixo)', 'Q2', 'Q3', 'Q4 (Alto)'], duplicates='drop')

# Médias de nutrientes por quartil do PF_ratio
nutri_por_quartil_pf = df.groupby('PF_quartil')[['Caloric Value', 'Fat', 'Protein', 'Carbohydrates']].mean()

# Barplot
nutri_por_quartil_pf.plot(kind='bar', figsize=(14, 9), colormap='viridis')
plt.title('Média de Nutrientes por Quartil da Relação Proteína/Gordura (PF Ratio)')
plt.ylabel('Valor Médio')
plt.xlabel('Quartil da Relação Proteína/Gordura')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{output_dir}/barplot_nutricao_por_quartil_pf.png")
plt.close()

print("Análise 3 concluída. Gráfico de barras por quartil salvo.")

# --- ANÁLISE 4: CORRELAÇÃO DE MICRONUTRIENTES COM "HEALTH SCORE" ---

print("\nIniciando Análise 4: Health Score e Micronutrientes...")

# Definir colunas de micronutrientes
micronutrientes = ['Phosphorus', 'Potassium', 'Sodium', 'Vitamin B1', 'Vitamin B2', 'Vitamin B6']
df[micronutrientes] = df[micronutrientes].fillna(0)

# Criar um "Health Score" simples (Proteínas + Micronutrientes) / (Açúcares + Gordura)
df['Health_Score'] = (df['Protein'] + df[micronutrientes].sum(axis=1)) / (df['Sugars'] + df['Fat'] + epsilon)
df['Health_Score'] = df['Health_Score'].replace([np.inf, -np.inf], np.nan).fillna(0)

# Calcular correlação com o Health Score
corr_health_score = df[micronutrientes + ['Health_Score']].corr()['Health_Score'].drop('Health_Score')

# Barplot das correlações
plt.figure(figsize=(12, 8))
corr_health_score.sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title('Correlação entre Micronutrientes e o "Health Score"')
plt.ylabel('Coeficiente de Correlação de Pearson')
plt.xlabel('Micronutriente')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f"{output_dir}/barplot_correlacoes_micronutrientes.png")
plt.close()

print("Análise 4 concluída. Gráfico de correlação com Health Score salvo.")


# --- ANÁLISE 5: CLUSTERIZAÇÃO DE ALIMENTOS (K-MEANS) ---

print("\nIniciando Análise 5: Clusterização de Alimentos...")

# Variáveis para clusterização
vars_cluster = ['Caloric Value', 'Fat', 'Protein', 'Carbohydrates', 'Sugars']
df_cluster = df[vars_cluster].dropna()

# Padronização dos dados
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_cluster)

# Aplicar K-Means com n_clusters=3 (como no relatório)
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
clusters = kmeans.fit_predict(df_scaled)
df['Cluster'] = pd.Series(clusters, index=df_cluster.index)

# Aplicar PCA para visualização em 2D
pca = PCA(n_components=2)
pca_result = pca.fit_transform(df_scaled)
df_pca = pd.DataFrame(data=pca_result, columns=['PC1', 'PC2'])
df_pca['Cluster'] = clusters

# Gráfico de dispersão dos clusters (PCA)
plt.figure(figsize=(14, 9))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c'] # Azul, Laranja, Verde
for i in range(n_clusters):
    plt.scatter(
        df_pca[df_pca['Cluster'] == i]['PC1'],
        df_pca[df_pca['Cluster'] == i]['PC2'],
        s=60, c=colors[i], label=f'Cluster {i}', alpha=0.7
    )
plt.title('Visualização dos Clusters Nutricionais (via PCA)')
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{output_dir}/clusters_pca.png")
plt.close()

# Salvar estatísticas por cluster
stats_por_cluster = df.groupby('Cluster')[vars_cluster].mean()
stats_por_cluster.to_csv(f"{output_dir}/stats_por_cluster.csv")

print("Análise 5 concluída. Gráfico de clusters e estatísticas salvos.")
print("\n--- Todas as análises foram concluídas com sucesso! ---")
print(f"Verifique a pasta '{output_dir}' para os resultados.")