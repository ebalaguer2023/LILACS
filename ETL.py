import pandas as pd
from sqlalchemy import create_engine

def extract(filepath):
    df = pd.read_csv(filepath)
    return df
    
    
################################################################################

def alternative_extraction(file, sep):

    fin = open(file, "rt",encoding="utf-8")

    separator = sep

    def contarcolumnas(x):
        contarcolumnas=0
        for letra in x:
            if letra == sep:
                contarcolumnas = contarcolumnas+1 
        contarcolumnas = contarcolumnas+1 
        return contarcolumnas

    def obtenervalores(x):
            valor = ''
            cadenaabierta = False
            i = 0
            valores = []
            
            while i < len(x):

                caracter = x[i]
                    
                if caracter == '"' and not cadenaabierta:
                    cadenaabierta = True
                elif caracter == '"' and  cadenaabierta:
                    cadenaabierta = False
                
                if (caracter != sep) | (caracter == sep and cadenaabierta):
                    valor = valor + caracter
                
                if (caracter == sep and not cadenaabierta) | (caracter == '\n'):
                    valor = valor.strip()
                    valores.append(valor)
                    valor = ''
                i += 1
            return valores;


    #########################################################################

    # Leer encabezado para obtener nombres de columnas
    with open(file, "rt", encoding="utf-8") as fin:
        encabezado = fin.readline()
        columnas = obtenervalores(encabezado)
        cantidadcolumnas = contarcolumnas(encabezado)

    listavalores = []


    # Check line by line
    with open(file, "rt", encoding="utf-8") as fin:
        next(fin)  # ignores header
        for linea in fin:
            valores = obtenervalores(linea)
            if len(valores) == cantidadcolumnas:
                listavalores.append(valores)
            else:
                pass  

    df = pd.DataFrame(listavalores, columns=columnas)

    df.drop('', axis=1, inplace=True)

    return df

###############################################################################
    
def load(df):
    
    user = "postgres"
    keyword = "Gomasio2024"
    host = "localhost"
    port = "5432"
    database = "lilacs"
    table = "lilacs"

    engine = create_engine(f"postgresql+psycopg2://{user}:{keyword}@{host}:{port}/{database}")

    df.to_sql(table, engine, if_exists="replace", index=False)

    print(f"✅ DataFrame subido a PostgreSQL en la tabla '{table}'")



#######################################################
def convert(df):
    df['Publication year']=df['Publication year'].replace('', 0)
    df['Publication year']=df['Publication year'].astype(int)

    df['Entry Date']=pd.to_datetime(df['Entry Date'], format='%Y%m%d')
    df['Language']=df['Language'].astype('category')
    df['Database']=df['Database'].astype('category')
    df['Type']=df['Type'].astype('category')
    
    print('\n\n\n')
    print(df.info())
