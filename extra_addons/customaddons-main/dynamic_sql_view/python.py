for f in [
    r"C:\Users\Operador\PycharmProjects\odoo18\extra_addons\customaddons-main\dynamic_sql_view\security\security.xml",
    r"C:\Users\Operador\PycharmProjects\odoo18\extra_addons\customaddons-main\dynamic_sql_view\views\dynamic_view_form.xml",
]:
    data = open(f, "rb").read()
    if data.startswith(b"\xef\xbb\xbf"):
        open(f, "wb").write(data[3:])   # elimina los 3 bytes del BOM
        print(f"BOM eliminado en {f}")
    else:
        print(f"Sin BOM: {f}")
