
from flet import *
import datetime
from table import mytable, tb, tb_total, calldb
from database import tabela
import sqlite3
import flet


conexao = sqlite3.connect('../db/dados.db', check_same_thread=False)
cursor = conexao.cursor()





class App(UserControl):
    def __init__(self):
        super().__init__()
   
        self.dia = TextField(label="Qual o dia do pedido?")
        self.pao_c_margarina_sol = TextField(label="Quantos pães com margarina foram solicitados?", input_filter= NumbersOnlyInputFilter())
        self.pao_s_margarina_sol = TextField(label="Quantos pães sem margarina foram solicitados?", input_filter= NumbersOnlyInputFilter(), autofocus=True)
        self.pao_c_margarina_receb = TextField(label="Quantos pães com margarina foram recebidos?", input_filter= NumbersOnlyInputFilter())
        self.pao_s_margarina_receb = TextField(label="Quantos pães sem margarina foram recebidos?", input_filter= NumbersOnlyInputFilter())
        self.pao_c_margarina_cob = TextField(label="Quantos pães com margarina foram cobrados?", input_filter= NumbersOnlyInputFilter())
        self.pao_s_margarina_cob = TextField(label="Quantos pães sem margarina foram cobrados?", input_filter= NumbersOnlyInputFilter())

        self.inputcon = Card(
            width= 700,
            height= 400,
            offset=transform.Offset(4,0),
            animate_offset= animation.Animation(600,curve="easeIn"),
            elevation=30,
            content = Container(
                padding = 20,
                content = Column([
                    Row([
                        Text("Adicionar pedidos", size=20, weight="bold"),
                        IconButton(icon="close", icon_size=30, on_click=self.hidecon)
                                     
                                    
                    ],  alignment= "SpaceBetween", scroll= flet.ScrollMode.ALWAYS,),

                    Row([ElevatedButton(
                                "Selecione a data do pedido",
                                icon=icons.CALENDAR_MONTH,
                                on_click = lambda e: self.page.open(
                                    DatePicker(
                                        first_date=datetime.datetime(year=2024, month=1, day=1),
                                        last_date=datetime.datetime(year=2024, month=12, day=31),
                                        on_change=self.handle_change,
                                        
                                        
                                    )
                                )
                            )]),
                    
                    Row([self.pao_c_margarina_sol,
                        self.pao_s_margarina_sol]),

                    Row([self.pao_c_margarina_receb,
                        self.pao_s_margarina_receb]),

                    Row([self.pao_c_margarina_cob,
                        self.pao_s_margarina_cob]),
                    
                    Row([
                        ElevatedButton("Inserir dados", on_click=self.add_dados),
                        ElevatedButton("Limpar dados", on_click=self.limpar_dados),
                    ])     
                ], scroll= flet.ScrollMode.ALWAYS)),
            )
        
        





    
    def salvar(self):
        if not self.dia.value:
            self.dia.error_text = "Digite o dia do pedido"
            self.page.update()

        if not self.pao_c_margarina_sol.value:
            self.pao_c_margarina_sol.error_text = "Digite a quantidade de pães com margarina solicitados"
            self.page.update()

        if not self.pao_s_margarina_sol.value:
            self.pao_s_margarina_sol.error_text = "Digite a quantidade de pães sem margarina solicitados"
            self.page.update()

        if not self.pao_c_margarina_receb.value:
            self.pao_c_margarina_receb.error_text = "Digite a quantidade de pães com margarina recebidos"
            self.page.update()

        if not self.pao_s_margarina_receb.value:
            self.pao_s_margarina_receb.error_text = "Digite a quantidade de pães sem margarina recebidos"
            self.page.update()

        if not self.pao_c_margarina_cob.value:
            self.pao_c_margarina_cob.error_text = "Digite a quantidade de pães com margarina cobrados"
            self.page.update()

        if not self.pao_s_margarina_cob.value:
            self.pao_s_margarina_cob.error_text = "Digite a quantidade de pães sem margarina cobrados"
            self.page.update()  
        else:

            self.data_pedido = self.dia.value
            self.pao_com_marg_sol = self.pao_c_margarina_sol.value
            self.pao_sem_marg_sol = self.pao_s_margarina_sol.value
            self.pao_com_marg_receb = self.pao_c_margarina_receb.value
            self.pao_sem_marg_receb = self.pao_s_margarina_receb.value
            self.pao_com_marg_cob = self.pao_c_margarina_cob.value
            self.pao_sem_marg_cob = self.pao_s_margarina_cob.value

            
            self.total_paes_sol = int(self.pao_com_marg_sol) + int(self.pao_sem_marg_sol)
            self.total_paes_reb = int(self.pao_com_marg_receb) + int(self.pao_sem_marg_receb)
            self.total_paes_cob = int(self.pao_com_marg_cob) + int(self.pao_sem_marg_cob)

            self.diferenca= int(self.total_paes_cob) - int(self.total_paes_reb)

            
            

           
            self.page.add(
                Text(f"Você solicitou {self.total_paes_sol} pães no dia {self.data_selecionada.value} e chegaram {self.total_paes_reb}, tendo uma diferença de {self.diferenca} pães")
            )
            self.page.update()
           


    def add_dados(self,e):
        #self.salvar()
        tabela()
        try:
            cursor.execute("""INSERT INTO paes (data_pedido, 
                                                com_margarina_pedidos, 
                                                sem_margarina_pedidos, 
                                                com_margarina_g_cont, 
                                                sem_margarina_g_cont, 
                                                com_margarina_p_cont, 
                                                sem_margarina_p_cont) 
                            VALUES (?,?,?,?,?,?,?)""", 
                                [self.data_selecionada.value, 
                                self.pao_c_margarina_sol.value, 
                                self.pao_s_margarina_sol.value, 
                                self.pao_c_margarina_receb.value, 
                                self.pao_s_margarina_receb.value, 
                                self.pao_c_margarina_cob.value, 
                                self.pao_s_margarina_cob.value])
            
            conexao.commit()
            print('Dados salvos com sucesso')

            self.inputcon.offset = transform.Offset(4,0)

            self.page.snack_bar = SnackBar(Text("Cadastrado com sucesso"), bgcolor="green")

            self.page.snack_bar.open = True

            tb.rows.clear()
            tb_total.rows.clear()

            calldb()
            tb.update()
            tb_total.update()
            self.page.update()

        except Exception as e:
            print(e)

    def limpar_dados(self, e):
        self.pao_c_margarina_sol.value = "" 
        self.pao_s_margarina_sol.value = "" 
        self.pao_c_margarina_receb.value = "" 
        self.pao_s_margarina_receb.value = "" 
        self.pao_c_margarina_cob.value = "" 
        self.pao_s_margarina_cob.value = ""
        self.inputcon.update()

    def handle_change(self,e):
        self.data_selecionada = Text(e.control.value.strftime('%Y-%m-%d'))


    def showinput(self,e):
        self.inputcon.offset = transform.Offset(0.7,-0.5)
        self.inputcon.alignment=alignment.center
        self.pao_c_margarina_sol.focus()
        self.inputcon.update()

    def hidecon(self,e):
        self.inputcon.offset = transform.Offset(4,0)
        self.inputcon.update()


        

    
    def build(self):

        self.view = Column([
            Text("Controle Pães Graúna", size=30, weight="bold"),
            ElevatedButton("Inserir pedido", on_click=self.showinput), mytable, self.inputcon
        ]) 
        
        return self.view
    