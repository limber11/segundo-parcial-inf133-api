from flask import render_template

def registro():
    return render_template('registro.html')

def login():
    return render_template('login.html')

def perfil(user):
    return render_template('profile.html', user=user)

def usuarios(users):
    return render_template('usuarios.html', users=users)

def actualizar(user):
    return render_template('actualizar.html', user=user)
