python3 -m venv venv
source venv/bin/activate
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simpl --default-timeout=1000 --no-cache-dir -r requirements.txt
python3 main.py
#allure generate test-output - o allure-report --clean