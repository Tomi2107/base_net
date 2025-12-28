1    cd RedSocialX
2  python -m venv Socialenv  
3  Socialenv/Scripts/activate
4  python.exe -m pip install --upgrade pip
previa
1 incorpore todas las carpetas para que agregue las actualizaciones delassiete que hay en gith, + detalles en los videos..
nota: no llego a hacer las otras web mercado.. etc.. ni el deploy a aws..
2 pip install pip-upgrader
3 pip-upgrade dentro de la carpeta raiz e hizo upgrade de requirements.txt
4 python.exe -m pip install --upgrade pip para installar los paquetes
5 python manage.py makemigrations -> migrate
6 create superuser python manage.py createsuperuser primero agregue el .env dentro social dentro de core //core apli de proyecto no app 
7 Username: SocialRedX
8 Email address: tom.palmeyro@gmail.com
9 Password: SocialRedX21
 agregar NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd" a settinmgs antes de probar los siguientes npm comandos
10 npm install node.js version actuall -> npm install -g npm@10.9.0
11 npm install @tailwindcss/line-clamp ->  @tailwindcss/typography -> @tailwindcss/forms -> @tailwindcss/aspect-ratio
x npm install tailwindcss postcss autoprefixer
  npm install postcss-simple-vars
12 python manage.py tailwind start
13 python manage.py runserver en otra consola


desaparecio social-1 de postgress
cambie a social que si aparece, pidio migrations