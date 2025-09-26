from flask import Flask, request, jsonify, session
from datetime import datetime
from flask_cors import CORS
import pymysql
import pymysql.cursors


app= Flask(__name__)
app.secret_key = "clave_super_secreta"  
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}},supports_credentials=True)

config={
    "host":"localhost",
    "user":"root",
    "password":"1014961053",
    "database":"sena_bicicletas"
    
}

def conexion():
    return pymysql.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        cursorclass= pymysql.cursors.DictCursor
    )
    
    
@app.route("/")
def principal():
    return jsonify({"mensaje":"el backend esta en uso"}),200


#-------------------------login

@app.route("/iniciar",methods=["POST"])
def iniciar():
    with conexion() as conn:
        with conn.cursor() as cur:
            datos=request.get_json()
            correo = datos.get("correo")
            password = datos.get("password")
            cur.execute("select * from usuarios where correo = %s",(correo,))
            datos = cur.fetchone()
            if datos:
                
                cur.execute("select * from usuarios where correo=%s and password=%s",(correo,password))
                dato2 = cur.fetchall()
                if dato2:
                    session["correo"]= correo
                    return jsonify({"mensaje":"iniciar","datos":dato2}),200
                else:
                    return jsonify({"mensaje":"contraseña incorrecta"}),400
            else:
                return jsonify({"mensaje":"usuario no existe"}),400
# 


# -----------------------usuario

@app.route("/usuario")
def consultar():
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from usuarios")
            datos= cur.fetchall()
            return jsonify({"mensaje":datos}),200
        
        
@app.route("/usuario",methods=["POST"])
def agregar():
    with conexion() as conn:
        with conn.cursor() as cur:
            datos = request.get_json()
            nombre = datos.get("nombre")
            correo = datos.get("correo")
            password = datos.get("password")
            rol = datos.get("rol")
            estrato = datos.get("estrato")
            cur.execute("insert into usuarios(nombre,correo,password,rol,estrato)values(%s,%s,%s,%s,%s)",(nombre,correo,password,rol,estrato))
            conn.commit()
            return jsonify({"mensaje":"usuario creado correctamente"}),201
        
        
@app.route("/usuario/<int:id>",methods=["DELETE"])
def eliminar(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("delete from usuarios where id = %s",(id,))
            conn.commit()
            return jsonify({"mensaje":"usuario eliminado"}),200
        
        
@app.route("/usuario_solo/<int:id>")
def individual(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from usuarios where id = %s",(id,))
            datos = cur.fetchone()
            return jsonify({"mensaje":datos}),200
        
@app.route("/usuario/<int:id>",methods=["PUT"])
def actualizar(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            datos = request.get_json()
            nombre = datos.get("nombre")
            correo = datos.get("correo")
            password = datos.get("password")
            rol = datos.get("rol")
            estrato = datos.get("estrato")
            cur.execute("update usuarios set nombre=%s,correo=%s,password=%s,rol=%s,estrato=%s where id=%s",(nombre,correo,password,rol,estrato,id))
            conn.commit()
            return jsonify({"mensaje":"usuario actualizado correctamente"})
        

# -------------------------------------bicicletas

@app.route("/bicicleta")
def main_bicicletas():
    with conexion() as conn, conn.cursor() as cur:
        cur.execute("select * from bicicletas")
        return jsonify({"mensaje":cur.fetchall()})
        
@app.route("/bicicleta",methods=["POST"])
def agregar_bicicletas():
    with conexion() as conn:
        with conn.cursor() as cur:
            datos = request.get_json()
            marca = datos.get("marca")
            color = datos.get("color")
            estado = datos.get("estado")
            precio_alquiler = datos.get("precio_alquiler")
            cur.execute("insert into bicicletas(marca,color,estado,precio_alquiler)values(%s,%s,%s,%s)",(marca,color,estado,precio_alquiler))
            conn.commit()
            return jsonify({"mensaje":"bicicleta creada correctamente"}),201
        
        
@app.route("/bicicleta/<int:id>",methods=["DELETE"])
def eliminar_bicicleta(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("delete from bicicletas where id = %s",(id,))
            conn.commit()
            return jsonify({"mensaje":"bicicleta eliminado"}),200
        
        
@app.route("/bicicleta_solo/<int:id>")
def individual_bicicleta(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from bicicletas where id = %s",(id,))
            datos = cur.fetchone()
            return jsonify({"mensaje":datos}),200
        
@app.route("/bicicleta/<int:id>",methods=["PUT"])
def actualizar_bicicleta(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            datos = request.get_json()
            marca = datos.get("marca")
            color = datos.get("color")
            precio_alquiler = datos.get("precio_alquiler")
            estado = datos.get("estado")
            cur.execute("update usuarios set marca=%s,color=%s,precio_alquiler=%s,estado=%s,estrato=%s where id=%s",(marca,color,precio_alquiler,estado,id))
            conn.commit()
            return jsonify({"mensaje":"bicicleta actualizada correctamente"})
        
#------------------------------------------------- eventos 
from flask import request, jsonify

@app.route("/eventos", methods=["GET"])
def consultar_eventos():
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM eventos ORDER BY fecha ASC")
            datos = cur.fetchall()
            return jsonify({"mensaje": datos}), 200


@app.route("/eventos", methods=["POST"])
def agregar_eventos():
    datos = request.get_json()
    titulo = datos.get("titulo")
    descripcion = datos.get("descripcion")
    lugar = datos.get("lugar")
    fecha = datos.get("fecha")

    if not (titulo and descripcion and lugar and fecha):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO eventos (titulo, descripcion, lugar, fecha) VALUES (%s, %s, %s, %s)",
                (titulo, descripcion, lugar, fecha)
            )
            conn.commit()
            return jsonify({"mensaje": "Evento creado correctamente"}), 201


@app.route("/eventos/<int:id>", methods=["DELETE"])
def eliminar_eventos(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM eventos WHERE id = %s", (id,))
            conn.commit()
            return jsonify({"mensaje": "Evento eliminado"}), 200


@app.route("/eventos/<int:id>", methods=["GET"])
def individual_eventos(id):
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM eventos WHERE id = %s", (id,))
            datos = cur.fetchone()
            if not datos:
                return jsonify({"error": "Evento no encontrado"}), 404
            return jsonify({"mensaje": datos}), 200


@app.route("/eventos/<int:id>", methods=["PUT"])
def actualizar_eventos(id):
    datos = request.get_json()
    titulo = datos.get("titulo")
    descripcion = datos.get("descripcion")
    lugar = datos.get("lugar")
    fecha = datos.get("fecha")

    if not (titulo and descripcion and lugar and fecha):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE eventos SET titulo=%s, descripcion=%s, lugar=%s, fecha=%s WHERE id=%s",
                (titulo, descripcion, lugar, fecha, id)
            )
            conn.commit()
            return jsonify({"mensaje": "Evento actualizado correctamente"}), 200



# -------------------------------- como usuario


@app.route("/bicicleta_disponible")
def consultar_bicicleta_disponible():
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from bicicletas where estado in('disponible')")
            datos= cur.fetchall()
            return jsonify({"mensaje":datos}),200
        
@app.route("/participar_evento", methods=["POST"])
def participar():
    datos = request.get_json()
    usuario_id = datos.get("usuario_id")
    evento_id = datos.get("evento_id")
    
    if not usuario_id or not evento_id:
        return jsonify({"mensaje": "usuario_id y evento_id son requeridos"}), 400

    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM eventos_participantes
                WHERE usuario_id=%s AND evento_id=%s
            """, (usuario_id, evento_id))
            if cur.fetchone():
                return jsonify({"mensaje": "Ya estás inscrito en este evento"}), 400

            cur.execute("""
                INSERT INTO eventos_participantes (usuario_id, evento_id)
                VALUES (%s, %s)
            """, (usuario_id, evento_id))
            conn.commit()
            
    return jsonify({"mensaje": "Inscripción exitosa"}), 201


@app.route("/cancelar_evento", methods=["POST"])
def cancelar_evento():
    datos = request.get_json()
    usuario_id = datos.get("usuario_id")
    evento_id = datos.get("evento_id")
    
    if not usuario_id or not evento_id:
        return jsonify({"mensaje": "usuario_id y evento_id son requeridos"}), 400

    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM eventos_participantes
                WHERE usuario_id=%s AND evento_id=%s
            """, (usuario_id, evento_id))
            if not cur.fetchone():
                return jsonify({"mensaje": "No estás inscrito en este evento"}), 400

            cur.execute("""
                DELETE FROM eventos_participantes
                WHERE usuario_id=%s AND evento_id=%s
            """, (usuario_id, evento_id))
            conn.commit()
            
    return jsonify({"mensaje": "Inscripción cancelada"}), 200


@app.route("/alquileres/start", methods=["POST"])
def iniciar_alquiler():
    datos = request.get_json()
    usuario_id = datos.get("usuario_id")
    bicicleta_id = datos.get("bicicleta_id")
    valor_base = datos.get("valor_base") 
    
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO alquileres (usuario_id, bicicleta_id, valor_base)
                VALUES (%s, %s, %s)
            """, (usuario_id, bicicleta_id, valor_base))
            
            cur.execute("UPDATE bicicletas SET estado='no_disponible' WHERE id=%s", (bicicleta_id,))
            conn.commit()
            
    return jsonify({"mensaje": "Alquiler iniciado"}), 201

@app.route("/alquileres/<int:id>/end", methods=["POST"])
def finalizar_alquiler():
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM alquileres WHERE id=%s", (id,))
            alquiler = cur.fetchone()
            if not alquiler:
                return jsonify({"mensaje": "Alquiler no encontrado"}), 404
            valor_total = float(alquiler["valor_base"])
            cur.execute("SELECT estrato FROM usuarios WHERE id=%s", (alquiler["usuario_id"],))
            estrato = cur.fetchone()["estrato"]
            if estrato in [1, 2]:
                valor_total *= 0.9  
            elif estrato in [3, 4]:
                valor_total *= 0.95  
            valor_total = round(valor_total, 2)
            ahora = datetime.now()
            cur.execute("""
                UPDATE alquileres
                SET fecha_fin=%s, valor_total=%s
                WHERE id=%s
            """, (ahora, valor_total, id))
            cur.execute("UPDATE bicicletas SET estado='disponible' WHERE id=%s", (alquiler["bicicleta_id"],))
            conn.commit()
            return jsonify({
                "mensaje": "Alquiler finalizado",
                "alquiler_id": id,
                "bicicleta_id": alquiler["bicicleta_id"],
                "usuario_id": alquiler["usuario_id"],
                "fecha_inicio": str(alquiler["fecha_inicio"]),
                "fecha_fin": str(ahora),
                "valor_total": valor_total
            }), 200


@app.route("/admin")
def main():
    with conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("select * from")
            
            
if __name__ == "__main__":
    app.run(debug=True)