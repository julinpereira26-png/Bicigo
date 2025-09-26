function bicicletas(){
    const contenido = document.getElementById("contenido")
    fetch("http://127.0.0.1:5000/bicicleta")
    .then(res=>res.json())
    .then(data=>{
        sessionStorage.setItem("valor_base", data.mensaje[0].valor_base)
        contenido.innerHTML="";
        data.mensaje.forEach(element => {
            contenido.innerHTML+=`
            <tr>
                <td>${element.id}</td>
                <td>${element.marca}</td>
                <td>${element.color}</td>
                <td>${element.estado}</td>
                <td>${element.precio_alquiler}</td>
                <td><button class="btn-alquilar" onclick="eliminar(${element.id})"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><path fill="#d6d0e0" d="M19 4h-3.5l-1-1h-5l-1 1H5v2h14M6 19a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V7H6z"/></svg></button></td>
                <td><button class="btn-alquilar" onclick="modificar(${element.id})"><svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24"><g fill="none" fill-rule="evenodd"><path d="m12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.018-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"/><path fill="#d6d0e0" d="M20.131 3.16a3 3 0 0 0-4.242 0l-.707.708l4.95 4.95l.706-.707a3 3 0 0 0 0-4.243l-.707-.707Zm-1.414 7.072l-4.95-4.95l-9.09 9.091a1.5 1.5 0 0 0-.401.724l-1.029 4.455a1 1 0 0 0 1.2 1.2l4.456-1.028a1.5 1.5 0 0 0 .723-.401z"/></g></svg></button></td>
            </tr>
            
            
            `
        });
    })
}
function eliminar(id) {
    fetch(`http://127.0.0.1:5000/bicicleta/${id}`, { method: "DELETE" })
    .then(res => {
        if (!res.ok) {
            throw new Error("Error al eliminar la bicicleta");
        }
        return res.json();
    })
    .then(data => {
        Swal.fire({
            title: "Bicicleta eliminada",
            text: "La bicicleta fue eliminada correctamente.",
            icon: "success",
            confirmButtonText: "Aceptar",
             scrollbarPadding: false, // 🔥 evita que se mueva el contenido
        }).then((result)=>{
            if (result.isconfirmed){
                window.location.reload()
            }
        })
    })
    .catch(error => {
        Swal.fire({
            title: "Error",
            text: "No se pudo eliminar la bicicleta.",
            icon: "error",
            confirmButtonText: "Intentar de nuevo",
             scrollbarPadding: false, // 🔥 evita que se mueva el contenido
  
        });
        console.error(error);
    });
}

function agregar_usuario(){
    console.log("js iniciado")
    const correo = document.getElementById("correo").value
    const password = document.getElementById("password").value
    const nombre = document.getElementById("nombre").value
    const estrato = document.getElementById("estrato").value
    
    const datos={
        nombre:nombre,
        estrato:estrato,
        correo:correo,
        password:password,
        rol:"usuario"
    }
    fetch("http://127.0.0.1:5000/usuario",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(datos)})
    .then(res=>res.json())
    .then(data=>{
        Swal.fire({
                title: "usuario creado",
                text: "usuario registrado con existo",
                icon: "succes",
                confirmButtonText: "Aceptar",
                 scrollbarPadding: false, // 🔥 evita que se mueva el contenido
  
        }).then(result)
    })
}

function validar(){
    console.log("js iniciado")
    const correo = document.getElementById("correo").value
    const password = document.getElementById("password").value
    const datos={
        correo:correo,
        password:password
    }
    fetch("http://127.0.0.1:5000/iniciar",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(datos)})
    .then(res=>res.json())
    .then(data=>{
        if (data.mensaje ==="iniciar"){
            window.location.href="/templates/user/principal.html"
        }else if (data.mensaje ==="contraseña incorrecta"){
Swal.fire({
  icon: 'error',
  title: 'Contraseña incorrecta',
  text: 'Por favor digite de nuevo su contraseña',
  confirmButtonText: 'Aceptar',
  scrollbarPadding: false,
}).then(result);
}
    })
}

const contenido = document.getElementById("eventos-contenido");
// Mostrar eventos
function mostrareventos(){
    fetch("http://127.0.0.1:5000/eventos")
    .then(res => res.json())
    .then(data => {
        contenido.innerHTML = "";
        data.mensaje.forEach(element => {
            contenido.innerHTML += `
            <div class="evento-card">
                <h2>${element.titulo}</h2>
                <p><strong>📅 Fecha:</strong> ${element.fecha}</p>
                <p><strong>📍 Lugar:</strong> ${element.lugar}</p>
                <p>${element.descripcion}</p>
                <div class="acciones">
                    <button class="btn-editar" onclick="redirecevento(${element.id})">Editar</button>
                    <button class="btn-eliminar" onclick="eliminarEvento(${element.id})">Eliminar</button>
                </div>
            </div>
            `;
        });
    });
}

// Redirigir a la página de actualización
function redirecevento(id){
    localStorage.setItem("id_evento", id); // ✅ forma correcta
    window.location.href = "actualizar_evento.html";
}

// Eliminar evento
function eliminarEvento(id){
    if(!confirm("¿Seguro que quieres eliminar este evento?")) return;
    fetch(`http://127.0.0.1:5000/eventos/${id}`, { method: "DELETE" })
    .then(res => res.json())
    .then(respuesta => {
        alert(respuesta.mensaje);
        mostrareventos();
    });
}

// (Editar evento sería similar: traer datos, mostrarlos en un form, hacer PUT)

function alquilar(id_bicicleta){
    const id_usuario = sessionStorage.getItem("id_usuario")
    const valor_base = sessionStorage.getItem("valor_base")
    const id_bici = id_bicicleta
    const datos={
        usuario_id:id_usuario,
        bicicleta_id:id_bici,
        valor_base:valor_base
    }
    fetch(" http://127.0.0.1:5000/alquileres/start",{method:"POST",headers:{"Content-Type": "application/json"},body:JSON.stringify(datos)})
    .then(res=>res.json())
    .then(data=>{
        alert(data.mensaje)
    })

}
