import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db
from .models import Item, User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return render_template('index.html', items=items)

@main_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        new_item = Item(name=name, description=description)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create.html')

@main_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form.get('description', '')
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit.html', item=item)

@main_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/usuarios')
def listar_usuarios():
    q = request.args.get('q', '').strip()
    if q:
        usuarios = User.query.filter(User.nombre.contains(q)).all()
    else:
        usuarios = User.query.all()
    return render_template('listar_usuarios.html', usuarios=usuarios, q=q)

@main_bp.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()

        errores = []
        if not nombre:
            errores.append('El nombre es obligatorio.')
        if not correo:
            errores.append('El correo es obligatorio.')
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append('El correo no tiene un formato válido.')
        if not telefono:
            errores.append('El teléfono es obligatorio.')
        elif not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', telefono):
            errores.append('El teléfono no tiene un formato válido.')

        if not errores:
            existe = User.query.filter_by(correo=correo).first()
            if existe:
                errores.append('El correo ya está registrado.')

        if errores:
            for e in errores:
                flash(e, 'danger')
            return render_template('crear_usuario.html', nombre=nombre, correo=correo, telefono=telefono)

        nuevo = User(nombre=nombre, correo=correo, telefono=telefono)
        db.session.add(nuevo)
        db.session.commit()
        flash('Usuario creado exitosamente.', 'success')
        return redirect(url_for('main.crear_usuario'))

    return render_template('crear_usuario.html')

@main_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = User.query.get_or_404(id)
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()

        errores = []
        if not nombre:
            errores.append('El nombre es obligatorio.')
        if not correo:
            errores.append('El correo es obligatorio.')
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo):
            errores.append('El correo no tiene un formato válido.')
        if not telefono:
            errores.append('El teléfono es obligatorio.')
        elif not re.match(r'^\+?[\d\s\-\(\)]{7,20}$', telefono):
            errores.append('El teléfono no tiene un formato válido.')

        if not errores and correo != usuario.correo:
            existe = User.query.filter_by(correo=correo).first()
            if existe:
                errores.append('El correo ya está registrado por otro usuario.')

        if errores:
            for e in errores:
                flash(e, 'danger')
    return render_template('editar_usuario.html', usuario=usuario)

@main_bp.route('/usuarios/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente.', 'success')
    return redirect(url_for('main.listar_usuarios'))

        usuario.nombre = nombre
        usuario.correo = correo
        usuario.telefono = telefono
        db.session.commit()
        flash('Usuario actualizado exitosamente.', 'success')
        return redirect(url_for('main.listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)
