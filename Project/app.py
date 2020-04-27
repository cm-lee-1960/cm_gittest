import os
from flask import Flask, session, escape
from flask import request, redirect

app = Flask(__name__, static_folder="static")
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.secret_key = 'changmin'

members = [
    {"id": "test1", "pw" : "1111"},
    {"id": "test2", "pw" : "2222"}
]

def get_text():
    text_temp = "<li><a href='{1}'>{0}</a></li>"
    text = [e for e in os.listdir('text') if e[0]!='.']
    return "\n".join([text_temp.format(t, f'Check/{t}') for t in text])

def get_menu():
    menu_temp = "<li><a href='{0}'>{0}</a></li>"
    menu = [e for e in os.listdir('content') if e[0]!='.']
    return "\n".join([menu_temp.format(m) for m in menu])

def get_menu2():
    menu_temp = "<li><a href='http://localhost:5005/content/{0}'>{0}</a></li>"
    menu = [e for e in os.listdir('content') if e[0]!='.']
    return "\n".join([menu_temp.format(m) for m in menu])

def get_template(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        template = f.read()
        
    return template

# 기본화면
@app.route("/")
def index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    return html

# 로그인 화면
@app.route("/login" , methods=['GET', 'POST'])
def login():
    with open('login.html', 'r', encoding="utf-8") as f:
        template = f.read()
    menu = get_menu()
    
    if request.method == 'GET':
        return template.format("", menu)
    
    elif request.method == 'POST':
       # 만약 회원이 아니면, "회원이 아닙니다."라고 알려주자
        m = [e for e in members if e['id'] == request.form['id']]
    if len(m) == 0:
        return template.format("<p>회원이 아닙니다.</p>", menu)
    
    if request.form['pw'] != m[0]['pw']:
        return template.format("<p>패스워드를 확인해 주세요.</p>", menu)
    
   # return redirect("content/calender?id=" + m[0]['id'])
    session['user'] = m[0]
    return redirect("content/calender")


#@app.route("/content/calender")
#def calender():
#    id = request.args.get('id', '')
#    template = get_template('template.html')
#    menu = get_menu()    
#    with open('content/calender.html', 'r', encoding='utf-8') as f:
#        html = f.read()    
#    return template.format(id, html, menu)

@app.route("/content/<title>" , methods=['GET', 'POST'])
def html(title):
    template = get_template('template.html')
    menu = get_menu()
    
    if title == 'Check':
        content = get_text()
    else:
        with open(f'content/{title}', 'r', encoding="utf-8") as f:
            content = f.read()
         
    # 일기를 저장할시에
    if request.method == 'POST':
        with open(f'text/{request.form["theme"]}', 'w', encoding="utf-8") as f:
            f.write(request.form['diary'])
        return redirect(f'{title}')

    if 'user' in session:
        name = session['user']['id']
        return template.format(name, content, menu)
    else:
        name = ''
      
@app.route("/content/Check/<title>")
def upload(title):
    template = get_template('template.html')
    menu = get_menu2()
    
    with open(f'text/{title}', 'r', encoding="utf-8") as f:
        content = f.read()
    
    if 'user' in session:
        name = session['user']['id']
        return template.format(name, content, menu)
    else:
        title = ''
        
app.run(port=5005)