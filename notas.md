Tutorial: https://www.youtube.com/watch?v=7t2alSnE2-I

Python online editor: https://code.labstack.com/XEhK3Znl

Deploy with: https://Deta.sh

TablePlus app: https://tableplus.com/windows

OpenApi Docsa: http://127.0.0.1:8000/docs

> python3 -m venv fastapi-env

> cd fastapi-env

> fastapi-env\Scripts\activate.bat 

> pip3 install fastapi

> python3 -m pip install --upgrade pip

> pip3 install uvicorn

> pip3 install SQLAlchemy (latest)

> pip install SQLAlchemy==1.3.24

> pip3 uninstall SQLAlchemy==1.3.24 (con esta no me anduvo, tuve que usar la ultima version)

> pip3 install -r requirements.txt

## Fundamentals

### Enums

```
class Index(str, Enum):
    FTSE100 = "FTSE 100"
    SNP500 = "S&P 500"
    DOWJONE = "Dow Jones"

class IntIndex(Enum):
    FTSE100 = 1
    SNP500 = 2
    DOWJONE = 3
```

Si en el endpoint pones un parametro de tipo enum, Swagger automaticamente te muestra un combo. (muestra los valores)


### Constructor con packaging en dict
    user = UserInDB(**user_dict)
    construye un pydantic model UserInDB pasando las key y valor como argumentos del constructor
        UserInDB(
            username = user_dict["username"],
            email = user_dict["email"],



### f-string formatting
f'mi super string {variable}'

para poder debugear el archivo principal se debe llamar main.py

crea un folder Blog, y adentro un __init__.py vacio.
Y se crea un main.py adentro. Para arrancar ese main hay que hacer

uvicorn blog.main:app --reload

>NOTA: No me anduvo el virtual environment. Lo corro sin Activate y anda.

Schemas: Se puede crear un archivo schemas.py para tener las clases de Entidad
luego se importan como

from . import schemas
y luego los parametros son de la forma blog:schemas.Blog

### SQL Alchemy

>NOTA: si no te encuentra las referencias tenes que ir a Python: select interpreter y ver en cual python.exe se instalo. Hace conflicto con el virtual env
y lo instalado localmente.

### Response Model
Con Response model podemos filtrar la salida del response, para no retornar todos los datos
Se pone el parametro response_model y se crea la clase BlogResponse

@app.get('/blog', response_model=List[schemas.BlogResponse])

class BlogResponse(BaseModel):
    title: str
    body: str

    class Config():
        orm_mode = True

### Hashing
>NOTA: A veces da error el import.. hacer requirements.txt varias veces y agarra.
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash(request.password)

### OpenApi Metadata
Se pueden agrupar los servicios usando 
```
tags=["blogs"]
@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
```

### ORM Relashionsip

* Tabla Blog, tiene un creador
user_id = Column(Integer, ForeignKey('users.id'))
creator = relashionsip("User", back_populates="blogs")

* Tabla User tiene una lista de blogs
blogs = relationship("Blog", back_populates="creator")

### Module routes
hacer carpeta routers y adentro **__init__.py**
dentro de esa carpeta cada router. blog.py, user.py
en main.py hay que importar las rutas

```
from .routers import user, blog

app.include_router(blog.router)
app.include_router(user.router)
```

blog.py

router = APIRouter()
y pones dentro todos los metodos get, post, put, etc.
en vez de @app.get, es @router.get
from .. import schemas (.. es el directorio anterior, . es el dir actual)
temporalmente se puede poner funciones en otro archivo y hacer database

### Router tags and prefix
No es necesario poner tag y prefijos a cada endpoint, se p uede hacer asi;

```
router = APIRouter(
    tags=["users"],
    prefix="/user"
)
```


### Dependency injection
db: Session = Depends(get_db) parece que solo funciona en router functions @router.get.
Para usarla en funciones comunes hay que pasarla por parametro.

### Modulos y Packages
Packages - Son los folders
    Para que python sepa que es package, debe tener __init__.py file.
Modules - Son los archivos .py

from package.module import objeto | class | etc    

### Structures
**Tuple**

```
tuple = 1,2,3,4  o (1,2,3,4) 

*primeros,ultimo = tuple #obtiene los primeros y el ultimo

person = ("Bob", 42, "Mechanic") 

name, _, profession = person #obtiene bob y mechanic, e ignora el del medio

name, *_ = person  #obiene solo name, e ignora el resto
```

**Lista**
```
list = [1,2,3,4]
for item in list:
	print(f'list item: {item}')
```

Si dentro de la lista hay un dict, se accede como elemento\[propiedad\]
Si dentro de la lista hay un obj, se accede como elemento.propiedad

### If else

```
if b > a:
  print("b is greater than a")
elif a == b:
  print("a and b are equal")
else:
  print("a is greater than b")
```

### List comprehension
Una forma resumida de hacer:

```
for x in array:
```

>*Ejemplo*
>
>lista = [{"name": 'nico', 'edad': 2}, {"name": 'nico2', 'edad': 2}]
>
>new_lista = [x['name'] for x in lista if 'nico2' in x['name']] 

### Dict comprehension
```
# Transformar array of dict --> dict con key name
array_dict = [
    {'name': 'nico', 'edad': 2, 'fec_nac': datetime.now()},
    {'name': 'juan', 'edad': 34, 'fec_nac': datetime.now()},
    {'name': 'carlos', 'edad': 54, 'fec_nac': datetime.now()}
]
#print(json.dumps(array_dict, indent=2, sort_keys=True, default=str))

dict_from_array = {item['name']:item for item in array_dict}
print(json.dumps(dict_from_array, indent=2, sort_keys=True, default=str))
```

### PACKING and UNPACKING

> Se usa:
>
> \* (for tuples) 
>
> ** (for dictionaries)


**Funcion usa packing para procesar los argumentos**
``` 
def mySum(*args):
    return sum(args)

print(mySum(1, 2, 3, 4, 5))
```    

**Se llama a la funcion haciando unpacking de los elementos del dictionary**
```
def fun(a, b, c):
    print(a, b, c)
 
# A call with unpacking of dictionary
d = {'a':2, 'b':4, 'c':10}
fun(**d)
```

**Algo parecido a destructuring en javascript (dict)**
```
current_user = {"id": 2, "email": "nerlijma@gmail.com", "username": "nerlijma"}
id, email = current_user["id"], current_user["email"]
print(id, email)
```

I also did something! oh my god!
I have a new requirement in feature/feature1


this change is not conflicting

This change needs to be merged!