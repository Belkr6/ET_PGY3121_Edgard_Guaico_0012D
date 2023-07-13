

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}
        self.carrito=carrito 
        
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified=True
        
        print("Carrito guardado:", self.carrito)
        
    def agregar(self, Alimentos):
        alimentos_id = str(Alimentos.itemid)
        
        if alimentos_id not in self.carrito.keys():
            self.carrito[alimentos_id] = {
                "Alimentos_id": alimentos_id,
                "nombre": Alimentos.marca,
                "precio": Alimentos.precio,
                "cantidad": 1,
                "total": Alimentos.precio,
                "total_general" : 0,
                
                
            }
        else:
            item_existente = self.carrito[alimentos_id]
            item_existente["cantidad"] += 1
            item_existente["precio"] = Alimentos.precio
            item_existente["total"] += Alimentos.precio
            item_existente["total_general"] +=  item_existente["total"]
        
       
        
        print("Carrito guardado:", self.carrito)
        self.guardar_carrito()
        
    def calcular_total_general(self, costo_envio=1200):
        total_general = sum(item["total"] for item in self.carrito.values())
        impuesto = int(total_general * 0.1)  # Calcula el 10% del total y convierte a entero
        total_con_impuesto = int(total_general + impuesto)  # Suma el impuesto al total y convierte a entero
        total_con_envio = int(total_con_impuesto + costo_envio)  # Suma el costo del envío al total con impuestos y convierte a entero
        return total_con_envio, impuesto

    
       
        

    def eliminar(self, Alimentos):
        id = Alimentos.itemid
        if id in self.carrito: 
            del self.carrito[id]
            self.guardar_carrito()
    
    def restar(self, Alimentos):
        alimentos_id = str(Alimentos.itemid)
        for key, value in self.carrito.items():
            if key == alimentos_id:
                value["cantidad"] -= 1
                value["total"] -= float(Alimentos.precio)
                if value["cantidad"] < 1:
                    del self.carrito[key]
                break
        self.guardar_carrito()
     
    def limpiar(self):
        self.session["carrito"]={}
        self.session.modified=True 
