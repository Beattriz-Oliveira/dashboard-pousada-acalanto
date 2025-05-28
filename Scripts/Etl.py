import mysql.connector
import re

# Conexão com o Banco de Dados
bd = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='1452',
    database='Acalanto'
)

def padronizar_telefone(telefone):
    numeros = re.sub(r"\D", "", telefone)  
    if numeros.startswith("55"):
        numeros = numeros[2:]
    if len(numeros) == 11:
        return f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}"
    elif len(numeros) == 10:
        return f"({numeros[:2]}) {numeros[2:6]}-{numeros[6:]}"
    return telefone

def etl():
    try:
        cursor = bd.cursor()

        cursor.execute('select id_cliente, telefone from Cliente')
        clientes = cursor.fetchall()
        print(f"Clientes extraídos: {clientes}")  

        dados_transformados = [
            (padronizar_telefone(telefone), id_cliente) for id_cliente, telefone in clientes
        ]
        print(f"Dados transformados: {dados_transformados}") 

        for telefone_padronizado, id_cliente in dados_transformados:
            print(f"Atualizando id_cliente={id_cliente} para telefone={telefone_padronizado}")  
            cursor.execute(
                'update Cliente set telefone = %s where id_cliente = %s',
                (telefone_padronizado, id_cliente)
            )

        bd.commit()
        print("Alterações confirmadas no banco de dados.")

    except mysql.connector.Error as erro:
        print(f"Erro no processo ETL: {erro}")

    finally:
        if cursor:
            cursor.close()
        if bd.is_connected():
            bd.close()

# Executando a função
if __name__ == "__main__":
    etl()