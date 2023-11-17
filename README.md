<p>
<a href="https://www.murphysec.com/dr/kctlQJ59tVrS2Opo61">
    <img src="https://www.oscs1024.com/platform/badge/binkuolo/fastapi.svg?size=small">
</a>
<a href="https://github.com/binkuolo/fastapi/blob/main/LICENSE">
    <img alt="GitHub" src="https://img.shields.io/github/license/binkuolo/fastapi?style=flat-square">
</a>

# 运行项目
Python版本 
>python3.10

安装依赖包
`pip install -r requirements.txt`

运行项目
```shell
# 普通
uvicorn app:app --reload
# 指定IP和端口
python -m uvicorn app:app --reload --host 10.133.68.144 --port 9000
```