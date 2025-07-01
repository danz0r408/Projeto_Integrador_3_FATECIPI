import pandas as pd
import os
from sqlalchemy import create_engine, String, Float
from PIL import Image

# Configurações do banco de dados PostgreSQL
DB_USER = 'postgres'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'PI'
DIRETORIO_DADOS = 'C:/Users/gu-gu/OneDrive/Desktop/Big Data/3 Semestre/PI 3/archive (1)/FINAL FOOD DATASET'  # Pasta com CSVs e PNGs

# Criar conexão com o PostgreSQL
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def processar_arquivos():
    """Processa todos os CSVs e PNGs na pasta."""
    dataframes_csv = []
    dados_png = []

    for arquivo in os.listdir(DIRETORIO_DADOS):
        caminho_completo = os.path.join(DIRETORIO_DADOS, arquivo)
        
        # Processar CSVs
        if arquivo.endswith('.csv'):
            try:
                df = pd.read_csv(caminho_completo)
                dataframes_csv.append(df)
                print(f"CSV processado: {arquivo}")
            except Exception as e:
                print(f"Erro no CSV {arquivo}: {str(e)}")
        
        # Processar PNGs (opcional)
        elif arquivo.endswith('.png'):
            try:
                img = Image.open(caminho_completo)
                # Exemplo: salvar metadados da imagem em um log
                print(f"PNG processado: {arquivo} (Tamanho: {img.size})")
            except Exception as e:
                print(f"Erro no PNG {arquivo}: {str(e)}")

    # Combinar CSVs (se houver)
    if dataframes_csv:
        return pd.concat(dataframes_csv, ignore_index=True)
    else:
        raise ValueError("Nenhum CSV válido encontrado na pasta.")

def transformar_dados(df):
    """Transforma os dados combinados."""
    # Converter colunas numéricas
    numeric_cols = [
        'Caloric Value', 'Fat', 'Saturated Fats', 'Monounsaturated Fats',
        'Polyunsaturated Fats', 'Carbohydrates', 'Sugars', 'Protein', 'Dietary Fiber',
        'Cholesterol', 'Sodium', 'Water', 'Vitamin A', 'Vitamin B1', 'Vitamin B11',
        'Vitamin B12', 'Vitamin B2', 'Vitamin B3', 'Vitamin B5', 'Vitamin B6', 'Vitamin C',
        'Vitamin D', 'Vitamin E', 'Vitamin K', 'Calcium', 'Copper', 'Iron', 'Magnesium',
        'Manganese', 'Phosphorus', 'Potassium', 'Selenium', 'Zinc', 'Nutrition Density'
    ]
    
    for col in numeric_cols:
        # Converter para numérico e forçar valores inválidos a se tornarem NaN
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Preencher valores ausentes com 0 ou outros valores padrão
    df.fillna({
        'Sugars': 0,
        'Cholesterol': 0,
        'Sodium': 0,
        'Caloric Value': 0,  # Garantir que Caloric Value não tenha NaN
    }, inplace=True)
    
    # Adicionar Health Score (exemplo)
    df['Health_Score'] = (
        (df['Protein'] * 2) +
        (df['Dietary Fiber'] * 1.5) - 
        (df['Saturated Fats'] * 0.5) - 
        (df['Sugars'] * 0.3)
    )
    # Limpar valores de colunas específicas para garantir que são numéricos
    df['Caloric Value'] = pd.to_numeric(df['Caloric Value'], errors='coerce')
     
    return df

def carregar_dados(df):
    """Carrega dados no PostgreSQL."""
    df.to_sql(
        name='alimentos_nutricao',
        con=engine,
        if_exists='replace',
        index=False,
        dtype={col: Float for col in df.columns if col != 'food'} | {'food': String(255)}
    )
    print("Dados carregados no PostgreSQL!")

def main():
    """Executa o pipeline completo."""
    try:
        print("Processando arquivos...")
        df = processar_arquivos()
        
        print("Transformando dados...")
        df_transformado = transformar_dados(df)
        
        print("Carregando no PostgreSQL...")
        carregar_dados(df_transformado)
        
        print("Concluído com sucesso!")
    
    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    main()