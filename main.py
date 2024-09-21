import flet as ft
import datetime
import mysql
import db

#App info
NAME_APP = "Password Manager"
VERSION_APP = "1.0"

#Company Info
NAME_COMPANY = "xFerTech"


def main(page: ft.Page):
    #----------- Page setup
    #page.window_height = 700
    #page.window_width = 300
    page.padding = 0
    page.window_maximized = True
    page.title = NAME_APP+" "+VERSION_APP

    #---------- Methods
    def cargar_datos():
        db.initialize_db()
        table_rows = []
        for dato in db.get_all():
            celdas = [
                ft.DataCell(ft.Text(dato[0],weight="bold")),
                ft.DataCell(ft.Text(dato[1],weight="bold")),
                ft.DataCell(ft.Text(dato[2])),
                ft.DataCell(ft.Text(dato[3])),
                ft.DataCell(ft.TextField(value=dato[4],password=True, can_reveal_password=True,
                    read_only=True,border=ft.InputBorder.NONE)
                ),
                ft.DataCell(
                    ft.Row(
                        controls=[
                            ft.IconButton("edit",data=dato, icon_color="blue"),
                            ft.IconButton("delete",data=dato, icon_color="red",on_click=delete_pass),
                        ]
                    )
                ),
            ]
            table_rows.append(ft.DataRow(cells=celdas))
        table.rows=table_rows
        page.window_width = table.width
        page.update()
    def save_password_dialog(e):
        page.dialog.open = True
        page.update()
    
    def close_dialog(e):
        reset_form()
        page.close_dialog()

    def save_password(e):
        #Validar datos
        if confirm_password():
            #Save data
            page.snack_bar.open = True
            try:
                db.create_pass(
                    generate_id(),
                    txf_service.value,
                    txf_email.value,
                    txf_phone.value,
                    txf_password.value
                )
                reset_form()
                state_text.value = "Datos guardados con éxito"
                page.snack_bar.bgcolor = "green"
            except Exception as err:
                reset_form()
                state_text.value = "Error al guardar datos: "+err
                page.snack_bar.bgcolor = "red"
            page.close_dialog()
        else:
            txf_confirm_password.helper_text = "Las contraseñas no coinciden."
        cargar_datos()
        page.update()
    
    def edit_btn(e:ft.ControlEvent):
        header_form.value = "Editar"
        txf_service.value=e.control.data[0]
        txf_email.value=e.control.data[1]
        txf_phone.value=e.control.data[2]
        txf_password.value=e.control.data[3]
        txf_confirm_password.value=e.control.data[3]
        txf_confirm_password.read_only=True       
        page.dialog.open = True
        btn_submit.on_click=edit_password
        page.update()
    
    def edit_password(e:ft.ControlEvent):
        try:
            db.edit(
                txf_service.value,
                txf_email.value,
                txf_phone.value,
                txf_password.value,
            )
        except Exception as e:
            print(e)
        cargar_datos()
        page.update()

    def delete_pass(e:ft.ControlEvent):
        db.delete(e.control.data[0])
        cargar_datos()
        page.update()

    def search_password(e):
        #db.initialize_db()
        table_rows = []
        for dato in db.search(txf_search.value):
            celdas = [
                ft.DataCell(ft.Text(dato[0],weight="bold")),
                ft.DataCell(ft.Text(dato[1],weight="bold")),
                ft.DataCell(ft.Text(dato[2])),
                ft.DataCell(ft.Text(dato[3])),
                ft.DataCell(content=ft.TextField(value=dato[4],password=True, can_reveal_password=True,
                    read_only=True,border=ft.InputBorder.NONE)
                ),
                ft.DataCell(
                    ft.Row(width=30,
                        controls=[
                            ft.IconButton("edit",data=dato, icon_color="blue"),
                            ft.IconButton("delete",data=dato, icon_color="red"),
                        ]
                    )
                ),
            ]
            table_rows.append(ft.DataRow(cells=celdas))
        table.rows=table_rows
        page.window_width = table.width
        page.update()

    def generate_id():
        ahora = datetime.datetime.now()
        return str(ahora.day)+str(ahora.second)+str(ahora.microsecond)

    def reset_form():
        txf_confirm_password.helper_text = ""
        txf_service.value=""
        txf_email.value=""
        txf_phone.value=""
        txf_password.value=""
        txf_confirm_password.value=""

    def confirm_password():
        if txf_password.value == txf_confirm_password.value:
            return True
    
    def empy_form():
        #Validate entry
        if txf_service.value:
            return True

    #---------- Application
    #--Controls generales
    #Mensaje de estado
    state_text = ft.Text(size=18, text_align="center")
    state = page.snack_bar = ft.SnackBar(
            width=500,
            behavior=ft.SnackBarBehavior.FLOATING,
            content=state_text
        )
    #Cuadro de busqueda
    txf_search = ft.TextField(
        border_radius=50,height=40,width=400,
        border=ft.InputBorder.UNDERLINE,on_change=search_password,
        )
    #Cuadro de búsqueda
    row_search_box = ft.Row(
        controls=[
            ft.Text(value="Buscar servicio: ",),
            txf_search
        ]
    )

    #Fila de botones
    row_btns = ft.Row(
        controls=[
            ft.ElevatedButton(text="Nueva clave", on_click=save_password_dialog),
            #ft.ElevatedButton(text="Generador de claves"),
        ]
    )

    #-- Control panel
    row_controls = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            row_btns,
            row_search_box,
        ]
    )
    
    #- Entries to save a new password
    txf_service = ft.TextField(label="Servicio",autofocus=True,on_submit=save_password)
    txf_email = ft.TextField(label="Correo",on_submit=save_password)
    txf_phone = ft.TextField(label="Teléfono",prefix_text="+52 ",on_submit=save_password)
    txf_password = ft.TextField(label="Contraseña",password=True,can_reveal_password=True,on_submit=save_password)
    txf_confirm_password = ft.TextField(label="Confirmar contraseña",password=True,can_reveal_password=True,
        helper_style=ft.TextStyle(color="red"),on_submit=save_password,)
    btn_submit = ft.ElevatedButton(text="Guardar",bgcolor="blue",color="white",on_click=save_password)
    btn_cancel = ft.ElevatedButton(text="Cancelar",bgcolor="red",color="white", on_click=close_dialog)
    #Row controls
    row_btns = ft.Row(controls=[btn_submit, btn_cancel], alignment="center")

    #--Hader
    hader = ft.Container(
        bgcolor=ft.colors.GREY_100,
        height=50,
        content=ft.Row(
            expand=True,
            alignment="center",
            controls=[ft.Text(value=NAME_APP,size=25,weight="bold",italic=True)],
        )
    )

    #--Body
    #Table
    table = ft.DataTable(
        expand=True,
        vertical_lines=ft.BorderSide(3, "blue"),
        horizontal_lines=ft.BorderSide(1, "green"),
        heading_row_color=ft.colors.BLUE_200,
        heading_text_style=ft.TextStyle(size=18,weight="bold"),
        data_row_color="white",
        border=ft.border.all(2,"black"),
        border_radius=10,
        
        columns=[
            ft.DataColumn(ft.Text(value="ID")),
            ft.DataColumn(ft.Text(value="Servicio")),
            ft.DataColumn(ft.Text(value="Correo")),
            ft.DataColumn(ft.Text(value="Teléfono")),
            ft.DataColumn(ft.Text(value="Contraseña")),
            ft.DataColumn(ft.Text(value="Acciones")),
        ],
        rows=[
        ],
    )

    table_container = ft.Container(
        expand=True,
        padding=ft.padding.only(left=50, right=50),
        content=ft.Column(
            alignment="center",
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Row(controls=[table])
            ])
    )

    #Form
    header_form = ft.Text(value="Nueva contraseña")
    password_form = ft.AlertDialog(
            modal=True,
            title=header_form,
            content=ft.Container(
                padding=ft.padding.only(top=20),
                content=ft.Column(
                    width=300,scroll=ft.ScrollMode.ADAPTIVE,tight=True,
                    controls=[
                        txf_service,
                        txf_email,
                        txf_phone,
                        txf_password,
                        txf_confirm_password,
                        row_btns,
                    ]
                )
            )
        )
    page.dialog = password_form

    #-- Call Mathods
    cargar_datos()

    #---------- Add controls
    page.add(hader)
    page.add(row_controls)
    page.add(table_container)
    
    #Upudate page
    page.update()
    

ft.app(target=main)#,view=ft.WEB_BROWSER)