
//función que envia el contenido a un elemento de tipo textarea
function CrearCarta(){
    var genero="";
    var a=document.getElementById("rut").value;
    var b=document.getElementById("nom").value;
    var c=document.getElementById("apeP").value;
    var d=document.getElementById("apeM").value;
    var e=document.getElementById("edad").value;
    var f=parseInt(document.getElementById("genero").value);
    var n=document.getElementById("fecha").value;
    
    var elementoGenero = document.getElementById('genero');
    var indiceSeleccionado = elementoGenero.selectedIndex;  //seleccionamos el indice elegido
    var gen=elementoGenero.options[indiceSeleccionado].text;
    
    /*
        if (f===1){
        gen='Mujer';
        }
        if (f===2){
        gen='Hombre';
        }
        if (f===3){
        gen='Otro Genero';
        }
        */

        var cadena= "Postulación Apoyo Ambiental: \n" +
                +"Rut: " + a + "\n" + "Nombre: " + b + "\n"+ "Ap. Paterno: " + c 
                + "\n" + "Ap. Materno: "+ d + "\n" + "Edad: " + e 
                + "\n" + "Fecha de nacimiento: " + n
                + "\n" + "Genero: " + gen;  
                
        document.getElementById("carta").value=cadena;
    }




    //función que cambia el color de fondo a orange
    function colorOrange(obj){
        obj.style.backgroundColor='orange';
    }

    function colorBlanco(obj){
        obj.style.backgroundColor='white';
    }

    function upperText(texto)
    {
        const x = texto;
        x.value= x.value.toUpperCase();
    }

    function colorFondo(obj){
        obj.style.backgroundColor='pink';
    }

    let url='https://api.thedogapi.com/v1/breeds';

        fetch(url)
            .then(response => response.json())
            .then(data => mostrarData(data))
            .catch(error=>console.log(error))
        
        const mostrarData=(data)=>{
            console.log(data)
            let body=""
            for(var i=0; i<data.length; i++)
            {
                body+=`<tr>
                    <td>${data[i].name}</td>
                    <td>${data[i].bred_for}</td>
                    <td>${data[i].breed_group}</td>
                    <td>${data[i].temperament}</td>
                    <td><img src='${data[i].image.url}' width="200px" height="200px"></td>
                    
                    </tr>`
            }
            document.getElementById('data').innerHTML=body
        }

