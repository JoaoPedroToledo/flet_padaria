
from flet import *
import sqlite3
import flet

from database import tabela

conexao = sqlite3.connect('../db/dados.db', check_same_thread=False)
cursor = conexao.cursor()

mes = Dropdown(width=140,options=[
                dropdown.Option("01- Janeiro"),
                dropdown.Option("02- Fevereiro"),
                dropdown.Option("03- Março"),
                dropdown.Option("04- Abril"),
                dropdown.Option("05- Maio"),
                dropdown.Option("06- Junho"),
                dropdown.Option("07- Julho"),
                dropdown.Option("08- Agosto"),
                dropdown.Option("09- Setembro"),
                dropdown.Option("10- Outubro"),
                dropdown.Option("11- Novembro"),
                dropdown.Option("12- Dezembro"),
            ], on_change=lambda e:  calldb()
            )


 

def click():
    data = mes.value.split('-')
    print(data)
    meses = f"select * from paes where data_pedido BETWEEN'2024-{data[0]}-01' AND '2024-{data[0]}-31'"
    return meses


def build():
    
    view = Column([
        Text("Selecione o mês dos pedidos"),
        mes,
        ElevatedButton(text="OK", on_click=click),
    ], 
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    
    )

    return view

home = build()

tb=DataTable(
    columns=[
        DataColumn(Text("Ações")),
        DataColumn(Text("Data do Pedido")),
        DataColumn(Text("Pedidos c/ margarina")),
        DataColumn(Text("Pedidos s/ margarina")),
        DataColumn(Text("Contagem c/ margarina Grauna")),
        DataColumn(Text("Contagem s/ margarina Grauna")),
        DataColumn(Text("Contagem c/ margarina Padaria")),
        DataColumn(Text("Contagem s/ margarina Padaria")),
        DataColumn(Text("Diferença contagens")),
    ],
    rows=[]
)

tb_total=DataTable(
    columns=[
        DataColumn(Text("Total")),
        DataColumn(Text("Total Paes Pedidos")),
        DataColumn(Text("Total Paes Contados Grauna")),
        DataColumn(Text("Total Paes Contados Padaria")),
        DataColumn(Text("Diferença entre contagens")),

    ],
    rows=[]
)

tb_preco=DataTable(
    columns=[
        DataColumn(Text("Valores")),
        DataColumn(Text("c/ Margarina")),
        DataColumn(Text("s/ Margarina")),
        DataColumn(Text("Leite c/ Margarina")),
        DataColumn(Text("Leite s/ Margarina")),

    ],
    rows=[]
)

id_edit = Text()
dia_edit = TextField(label="Qual o dia do pedido?")
pao_c_margarina_sol_edit = TextField(label="Quantos pães com margarina foram solicitados?", input_filter= NumbersOnlyInputFilter())
pao_s_margarina_sol_edit = TextField(label="Quantos pães sem margarina foram solicitados?", input_filter= NumbersOnlyInputFilter())
pao_c_margarina_receb_edit = TextField(label="Quantos pães com margarina foram recebidos?", input_filter= NumbersOnlyInputFilter())
pao_s_margarina_receb_edit = TextField(label="Quantos pães sem margarina foram recebidos?", input_filter= NumbersOnlyInputFilter())
pao_c_margarina_cob_edit = TextField(label="Quantos pães com margarina foram cobrados?", input_filter= NumbersOnlyInputFilter())
pao_s_margarina_cob_edit = TextField(label="Quantos pães sem margarina foram cobrados?", input_filter= NumbersOnlyInputFilter())
total_edit = Text()

def formatar_tabela(t):
    t.bgcolor="grey"
    t.border=border.all(2, "#304864")
    t.data_row_color="#6697CE"



def hidelg(e):
    dlg.visible = False
    dlg.update()

def saveandupdate(e):
    try:
          myid= id_edit.value
          cursor.execute("UPDATE paes SET data_pedido=?, com_margarina_pedidos=?, sem_margarina_pedidos=?, com_margarina_g_cont=?, sem_margarina_g_cont=?, com_margarina_p_cont=?, sem_margarina_p_cont=? WHERE id=?",
                         ( dia_edit.value, pao_c_margarina_sol_edit.value, pao_s_margarina_sol_edit.value, pao_c_margarina_receb_edit.value, pao_s_margarina_receb_edit.value, pao_c_margarina_cob_edit.value, pao_s_margarina_cob_edit.value, myid))
          
          conexao.commit()
          print("Editados com sucesso")
         
          tb.rows.clear()
          tb_total.rows.clear()
         
          calldb()
          dlg.visible = False
          
          dlg.update()
          tb.update()
          tb_total.update()
    except Exception as e:
        print('1 - ',e)


dlg = Container(
     width= 750,
     height= 340,
     bgcolor=colors.GREY_200,
     padding=10,
     content= Column([
            Row([
                Text("Editar dados", size=20, weight="bold"),
                IconButton(icon="close", on_click=hidelg)
            ], alignment="spaceBetween", scroll= flet.ScrollMode.ALWAYS,),
            
            Row([
                dia_edit,
            ]),
            Row([
                pao_c_margarina_sol_edit, 
                pao_s_margarina_sol_edit,
            ]),
            Row([
                pao_c_margarina_receb_edit, 
                pao_s_margarina_receb_edit, 
            ]),
            Row([
                pao_c_margarina_cob_edit, 
                pao_s_margarina_cob_edit,
            ]),
            ElevatedButton("salvar edição dos dados", on_click=saveandupdate)
     ])
)


def showEdit(e):

    try:
        data_edit = e.control.data
        
        id_edit.value = data_edit['id']
        dia_edit.value = data_edit['data_pedido'] 
        pao_c_margarina_sol_edit.value = data_edit['com_margarina_pedidos'] 
        pao_s_margarina_sol_edit.value = data_edit['sem_margarina_pedidos'] 
        pao_c_margarina_receb_edit.value = data_edit['com_margarina_g_cont'] 
        pao_s_margarina_receb_edit.value = data_edit['sem_margarina_g_cont'] 
        pao_c_margarina_cob_edit.value = data_edit['com_margarina_p_cont'] 
        pao_s_margarina_cob_edit.value = data_edit['sem_margarina_p_cont'] 
        print('data: ',data_edit)
       
        dlg.visible = True
        dlg.update()
        
    except Exception as e:
        print(e)

def showDelete(e):
    try:
          myid= int(e.control.data['id'])
          cursor.execute("DELETE FROM paes WHERE id=?",(myid,))
          
          conexao.commit()
          print("Deletado com sucesso")
          
          tb.rows.clear()
          tb_total.rows.clear()
          calldb()

          dlg.visible = False
          dlg.update()
         

          tb.update()
          tb_total.update()
    except Exception as e:
        print('2 - ',e)

def calldb():
    
    if mes.value != None:
        print('estamos no table: ', click())
        cursor.execute(click())
        filtro_mes = cursor.fetchall()
        print(filtro_mes)


        #cursor.execute("select * from paes where 1")
        #paes = cursor.fetchall()

        total_pedidos = 0
        total_g_cont = 0
        total_p_cont = 0
        diferenca = 0
        diferenca_cont = 0

        if not filtro_mes == "":
            keys = ['id','data_pedido','com_margarina_pedidos','sem_margarina_pedidos','com_margarina_g_cont','sem_margarina_g_cont','com_margarina_p_cont','sem_margarina_p_cont']

            result = [dict(zip(keys,values)) for values in filtro_mes]
            
            for x in result:
                diferenca_cont = (x['com_margarina_g_cont'] + x['sem_margarina_g_cont']) - (x['com_margarina_p_cont'] + x['sem_margarina_p_cont'])
                tb.rows.append(DataRow(
                    cells=[
                        DataCell(Row([
                            IconButton(icon="create", icon_color="green", data=x, on_click=showEdit),
                            IconButton(icon="delete", icon_color="red", data=x, on_click=showDelete)

                        ])),

                        DataCell(Text(x["data_pedido"])),
                        DataCell(Text(x["com_margarina_pedidos"])),
                        DataCell(Text(x["sem_margarina_pedidos"])),
                        DataCell(Text(x["com_margarina_g_cont"])),
                        DataCell(Text(x["sem_margarina_g_cont"])),
                        DataCell(Text(x["com_margarina_p_cont"])),
                        DataCell(Text(x["sem_margarina_p_cont"])),
                        DataCell(Text(diferenca_cont)),
                        
                        ]))
                

                total_pedidos += x['com_margarina_pedidos'] + x['sem_margarina_pedidos']
                total_g_cont += x['com_margarina_g_cont'] + x['sem_margarina_g_cont']
                total_p_cont += x['com_margarina_p_cont'] + x['sem_margarina_p_cont']
                diferenca = total_g_cont - total_p_cont

            tb_total.rows.append(DataRow(
                cells=[
                    DataCell(Row([IconButton(icons.TIMELINE_SHARP, icon_color="green")])),
                    DataCell(Text(total_pedidos)),
                    DataCell(Text(total_g_cont)),
                    DataCell(Text(total_p_cont)),
                    DataCell(Text(diferenca)),

                    ]))
            tb_preco.rows.append(DataRow(
                cells=[
                    DataCell(Row([IconButton(icons.TIMELINE_SHARP, icon_color="green")])),
                    DataCell(Text(1.25)),
                    DataCell(Text(0.70)),
                    DataCell(Text(1.25)),
                    DataCell(Text(0.70)),

                    ]))
    

calldb()
dlg.visible = False

formatar_tabela(tb)
formatar_tabela(tb_total)
formatar_tabela(tb_preco)

mytable = Column([
    dlg,
    Row([tb],  scroll= flet.ScrollMode.ALWAYS,),
    
    Row([
           tb_total, tb_preco, 

    ], scroll= flet.ScrollMode.ALWAYS),
    
])