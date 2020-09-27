запуск 

`ansible-playbook install.yml`

Конфиги для приложения находятся в директории group_vars/all
Открыть доступ с других ip для веб приложения roles/nginx/templates/allow_ip.conf



ссылки для проверки:

`curl -X GET 'http://51.178.109.166/payMethods/calculate?invoicePayMethod=6&withdrawPayMethod=4&base=invoice&amount=5'`

`curl -X GET 'https://51.178.109.166/payMethods'`

`curl --header "Content-Type: application/json" -X POST --data '{"invoicePayMethod":6,"withdrawPayMethod":4,"base":"invoice","amount":5.1}' 'http://51.178.109.166/bids'`
