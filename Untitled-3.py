def transformar_dados(df):
    """Transforma os dados combinados."""
    # Converter colunas numéricas
    numeric_cols = [
        'Caloric Value', 'Fat', 'Saturated Fats', 'Monounsaturated Fats',
        'Polyunsaturated Fats', 'Carbohydrates', 'Sugars', 'Protein', 'Dietary Fiber',
        'Cholesterol', 'Sodium', 'Water', 'Vitamin A', 'Vitamin B1', 'Vitamin B11',
        'Vitamin B12', 'Vitamin B2', 'Vitamin B3', 'Vitamin B5', 'Vitamin B6',
        'Vitamin C', 'Vitamin D', 'Vitamin E', 'Vitamin K', 'Calcium', 'Copper',
        'Iron', 'Magnesium', 'Manganese', 'Phosphorus', 'Potassium', 'Selenium',
        'Zinc', 'Nutrition Density'
    ]
    
    # Garantir que as colunas sejam convertidas para números, substituindo erros por NaN
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Preencher valores ausentes
    df.fillna({
        'Sugars': 0,
        'Cholesterol': 0,
        'Sodium': 0
    }, inplace=True)
    
    # Adicionar Health Score
    df['Health_Score'] = (
        (df['Protein'] * 2) +
        (df['Dietary Fiber'] * 1.5) - 
        (df['Saturated Fats'] * 0.5) - 
        (df['Sugars'] * 0.3)
    )
    
    # Limpar valores de colunas específicas para garantir que são numéricos
    df['Caloric Value'] = pd.to_numeric(df['Caloric Value'], errors='coerce')
    
    return df