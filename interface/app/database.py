import sqlite3


con = sqlite3.connect('../db/dados.db', check_same_thread=False)



def tabela():
    try:
        cursor = con.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS paes (
                    id integer primary key autoincrement,
                    data_pedido DATE,
                    com_margarina_pedidos integer,
                    sem_margarina_pedidos integer,
                    com_margarina_g_cont integer,
                    sem_margarina_g_cont integer,
                    com_margarina_p_cont integer,
                    sem_margarina_p_cont integer)""")
        
        con.commit()
        print('tabela criada com sucesso')
    except Exception as e:
        print(e)

tabela()