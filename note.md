## 开始

---

使用 PyCharm 创建一个基础 Python 项目

---

```bash
# 下载 django
pip install django
```

---

```bash
# 创建一个 django 项目
django-admin startproject backend
```

---

使用 Idea 的 Mark Directory as Sources Root 将刚刚创建的 backend 文件夹标记，
即源代码目录，**backend 下只能存放源代码，像 docs、logs、data 等目录只能与其同级**。

---

打开 Idea 设置，搜索 Django，勾选 Enable Django Support，设置 Django project root 和 Settings

---

在 backend 目录下创建一个 apps 目录，用于存放 app，注意，创建出来的 apps.py 中的 XxxConfig 的 name 属性
似乎需要加个 apps. 前缀
```bash
# 创建 app
cd ./backend/apps
django-admin startapp ninjaapi
```

---

在 backend 同级位置创建一个 requirements.txt 文件，用于存放项目依赖。 
推荐 requirments.txt 中不要有任何注释，因为 pip install -r requirements.txt 时，可能解析出错。
目前不强制要求指定库版本。

---

注意，下载的第三方库，有些是需要修改 settings.py 文件的，如 INSTALLED_APPS 等，请务必注意。
故，本项目的 settings.py 文件是非常重要的文件，对未来再开发项目有着重要意义。

---

配置完第三方库的 INSTALLED_APPS 等后，需要执行 python manage.py migrate 数据库迁移命令。

---

创建用户的命令：
```bash
python manage.py createsuperuser --username admin --email admin@example.com
```

---

项目结构：
```txt
python_web_development/
├── backend/
│   ├── apps/
│   ├── backend/
│   ├── static/
│   ├── templates/
│   └── manage.py
│
├── docs/
├── logs/
├── data/
│
├── .env
├── .gitignore
├── requirements.txt
├── note.md
└── readme.md
```

---

### Django REST framework
练习经典的组合：Django + Django REST framework

### Django Ninja
主要目的是练习异步编程 + 只提供 API 接口，不涉及前端


## 编程规格
此处为本项目严格遵循的个人要求的编程规格说明

1. 每个文件夹的命名不允许使用蛇形，直接将 `_` 删掉，如 `user_info` 改为 `userinfo`
2. 打开 Idea 的设置，Editor -> Inspections -> Proofreading -> Typo，关闭拼写检查，这样可以杜绝强迫症现象，
   虽然可能会出现单词拼写错误，但是写 Lua 模组的经验告诉我，那根本不是个事。
3. 文件夹的命名不需要参考 java 的规范：不要复数，由于 django 项目生成的文件全是复数，所以我要求向其看起，
   每个文件夹的命名能复数的都是复数。
4. 【推荐优先如此】参考 Django 风格，每个字符串都用单引号包裹，形如：'xxx'
5. 注释不要在行末尾，就在行头


### django-ninja 使用规范
#### version 1.0
在 {app_name}/views.py 同级目录下，创建一个 routers.py 文件，用于存放 django-ninja 的路由（纯净一点的话，可以删除 views.py 文件），
该文件要求定义一个 NinjaAPI 类实例，该实例将在 urls.py 中被 import 并使用（import 的目的是加载 routers.py 文件）。


## 使用第三方库
### python-dotenv


## 总结
**要频繁记录！做过的事情，必须要及时记录下来！**

