https://www.youtube.com/watch?v=jBzwzrDvZ18&t=15943s

[Python Backend Web Development Course (with Django) - YouTube](https://www.youtube.com/watch?v=jBzwzrDvZ18&t=15943s)

([7:25:48](https://www.youtube.com/watch?v=jBzwzrDvZ18&t=26748s)) Building A Weather App With Django - Part 1

## Djangoでweather appの作成

/Users/tk/dev/myapp/myprojects/weather フォルダを作ってターミナルでweatherフォルダに移動して、djangoプロジェクトを作る　

そして、weatherdetectorフォルダに移動して、startappをする

```shell
cd /Users/tk/dev/myapp/myprojects/weather
django-admin startproject weatherdetector
cd weatherdetector
python manage.py startapp weather
```

/weatherdetector/templates フォルダを作成して、動画リンクのweather app から/templates/index.htmlをコピーする

python manage.py runserver でdjangoが正常に機能していることを確認する

templatesフォルダとアプリを認識させるため、/weatherdetector/setting.py に追加する（一部）

```python
INSTALLED_APP = [
    'weather',
]


TEMPLATES = [
    {
        'DIRS': [BASE_DIR/'templates'],
}
]
```

ルートディレクトリにindex.htmlを認識させるために、/weatherdetector/weatherフォルダにurls.pyを作成して以下を書く

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]
```

ページをレンダリングするためのindex関数を作る

/weather/views.py に以下を書く

```python
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')
```

プロジェクトフォルダにアプリで設定したURLを認識させるために /weatherdetector/urls.py に以下を追加する

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls'))
]
```

ここで、python manage.py runserver をすると以下の画面が表示される

![](/Users/tk/Documents/MrakText/画像/72841d8bcb6af0068c44c393eac34ef9bda1b353.png)

上画像の /templates/index.html のページの検索バーに入力された文字を受け取るために、/weather/views.py を編集する

```python
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST['city']
    else:
        city = ''
    return render(request, 'index.html', {'city': city})
```

検索バーに入力された文字列を使ってopenweathermap.orgのapiから天気情報を得る

/weather/views.py を編集する

```python
from django.shortcuts import render
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=7be23f71527265b91f0681dd53127d81').read()
        json_data = json.loads(res)
        data = {
            "country_code": str(json_data["sys"]["country"]),
            "coordinate": str(json_data["coord"]["lon"]) + " " + str(json_data["coord"]["lat"]),
            "temp": str(json_data["main"]["temp"]) + "k",
            "pressure": str(json_data["main"]["pressure"]),
            "humidity": str(json_data["main"]["humidity"]),
        }
    else:
        city = ""
        data = {}
    return render(request, 'index.html', {'city': city, 'data': data})
```

（res = urllib の行のappid= の部分にはサイトからコピーしたapiキーを入れる）

これで、apiから撮ってきたデータをindex.html で変数として扱える
