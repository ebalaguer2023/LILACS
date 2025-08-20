import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


user = "postgres"
keyword = "Gomasio2024"
host = "localhost"
port = "5432"
database = "lilacs"
table = "lilacs"

engine = create_engine(f"postgresql+psycopg2://{user}:{keyword}@{host}:{port}/{database}")
# Reading from a SQL query
query = 'SELECT "ID", "Authors", "Descriptor(s)", "Keyword(s)" FROM lilacs'
df = pd.read_sql(query, con=engine)

df = df[df['Keyword(s)'].str.contains('comunica', case=False) | df['Descriptor(s)'].str.contains('comunica',case=False) ]

def procesar_columna(df, col_name, alias, top_n=20):
    """
    Procesa una columna (Descriptor(s) o Keyword(s)) y genera gráfico ordenado
    sin incluir valores vacíos.
    """
    # Separar los valores por punto y coma
    df[col_name] = df[col_name].fillna('').str.split(';')

    # Crear nuevo dataframe con la columna expandida
    data = {'ID': df['ID'], alias: df[col_name]}
    dfk = pd.DataFrame(data)
    df_exploded = dfk.explode(alias).reset_index(drop=True)
    df_exploded[alias] = df_exploded[alias].str.strip()
    df_exploded[alias] = df_exploded[alias].str.upper()
    # Filtrar vacíos
    df_exploded = df_exploded[df_exploded[alias].str.strip() != '']

    # Contar frecuencias en orden descendente
    conteo = df_exploded[alias].value_counts().head(top_n)

    # Graficar
    fig, ax = plt.subplots()
    conteo.plot(kind='barh', ax=ax)
    ax.invert_yaxis()  # Para que el más frecuente quede arriba
    ax.tick_params(axis='y', labelsize=8)  # fuente más pequeña
    ax.set_title(f"Top {top_n} de {alias}")
    plt.tight_layout()
    plt.show()

# Procesar Descriptores
procesar_columna(df, "Descriptor(s)", "descriptor")

# Procesar Keywords
procesar_columna(df, "Keyword(s)", "keyword")

