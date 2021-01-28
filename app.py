from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudflask'
mysql = MySQL(app)
app.secret_key = 'my_secret_key'


# Departamentos
@app.route('/')
def home():
  cur = mysql.connection.cursor()
  cur.execute('''SELECT * FROM departamentos ''')
  data = cur.fetchall()
  return render_template('departamentos/list.html', departamentos=data)


@app.route('/form')
def form_depa():
  return render_template('departamentos/form.html')


@app.route('/create', methods=['POST'])
def add_depa():
  try:
    if request.method == 'POST':
      nom_departamento = request.form['nom_departamento']
      cur = mysql.connection.cursor()
      ver = cur.execute('SELECT * from departamentos where(  nom_departamento = %s )', (nom_departamento,))
      if ver > 0:
        flash('Ya existe este Departamento')
        return redirect('/form')
      else:
        cur.execute('INSERT INTO departamentos (nom_departamento) VALUES (%s)', (nom_departamento,))
        mysql.connection.commit()
        return redirect('/')
  except Exception as e:
    print(e)


@app.route('/delete/<id>', methods=['POST'])
def delete_depa(id):
  try:
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM departamentos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('home'))
  except:
    flash('Hay municipios relacionados con este departaamento')
    return redirect(url_for('home'))


@app.route('/edit/<id>')
def edit_depa(id):
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM departamentos WHERE id = %s ', (id))
  data = cur.fetchall()
  return render_template('departamentos/edit.html', departamentos=data)


@app.route('/update/<id>', methods=['POST'])
def update_depa(id):
  try:
    if request.method == 'POST':
      nom_departamento = request.form['nom_departamento']
      cur = mysql.connection.cursor()
      ver = cur.execute('SELECT * from departamentos where(  nom_departamento = %s ) and id != %s  ',
                        (nom_departamento, id))
      if ver > 0:
        flash('Ya existe este Departamento')
        return redirect('/form')
      else:
        cur.execute('UPDATE departamentos SET nom_departamento = %s WHERE id = %s ', (nom_departamento, id))
        mysql.connection.commit()
        return redirect('/')
  except Exception as e:
    print(e)


# Municipios
@app.route('/list/<id>')
def list_muni(id):
  cur = mysql.connection.cursor()
  cur.execute("""SELECT 
                  m.id, m.nom_municipios, d.nom_departamento, m.cod_minicipios
                  FROM
                  municipios m
                  INNER JOIN
                  departamentos d ON m.id_departamentos = d.id
                  WHERE
                  d.id = %s """, (id))
  data = cur.fetchall()
  return render_template('municipios/list.html', municipios=data)


@app.route('/from_muni')
def form_muni():
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM departamentos ')
  data = cur.fetchall()
  return render_template('municipios/form.html', departamentos=data)


@app.route('/creat', methods=['POST'])
def add_muni():
  try:
    print(request.method)
    if request.method == 'POST':
      nom_municipios = request.form['nom_municipios']
      cod_minicipios = request.form['cod_minicipios']
      id_departamentos = request.form['id_departamentos']
      cur = mysql.connection.cursor()
      print('hola')
      ver = cur.execute('SELECT * from municipios where(  nom_municipios = %s and cod_minicipios = %s )',
                        (nom_municipios, cod_minicipios))
      if ver > 0:
        flash('Ya existe este Departamento')
        return redirect(url_for('home'))
      else:

        cur.execute('INSERT INTO municipios (nom_municipios, cod_minicipios,id_departamentos ) VALUES (%s,%s,%s)',
                    (nom_municipios, cod_minicipios, id_departamentos))
        mysql.connection.commit()
        return redirect('/')
  except Exception as e:
    print(e)


@app.route('/delete_muni/<id>', methods=['POST'])
def delete_muni(id):
  try:
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM municipios WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('home'))
  except Exception as e:
    print(e)


@app.route('/edit_muni/<id>')
def edit_muni(id):
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM municipios WHERE id = %s ', (id))
  data = cur.fetchall()
  cur.execute('SELECT * FROM departamentos ')
  datas = cur.fetchall()
  return render_template('municipios/edit.html', municipios=data, departamentos=datas)


@app.route('/update_muni/<id>', methods=['POST'])
def update_muni(id):
  try:
    if request.method == 'POST':
      nom_municipios = request.form['nom_municipios']
      cod_minicipios = request.form['cod_minicipios']
      id_departamentos = request.form['id_departamentos']
      cur = mysql.connection.cursor()
      ver = cur.execute('SELECT * from municipios where(  nom_municipios = %s and cod_minicipios = %s ) and id != %s ',
                        (nom_municipios, cod_minicipios, id))
      if ver > 0:
        flash('Ya existe este Municipio')
        return redirect(url_for('form_muni'))
      else:

        cur.execute(
          'UPDATE municipios SET nom_municipios = %s, cod_minicipios = %s, id_departamentos = %s WHERE id = %s ',
          (nom_municipios, cod_minicipios, id_departamentos, id))
        mysql.connection.commit()
        return redirect(url_for('home'))
  except Exception as e:
    print(e)


if __name__ == "__main__":
  app.run(port=8000)
