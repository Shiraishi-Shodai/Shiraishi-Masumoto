# 起動方法
docker-compose up -d

# ターミナルに接続
docker-compose exec django /bin/bash
→root@(コンテナ名):/code# 

# ターミナル終了コマンド
exit

# 変更を反映される方法
docker-compose restart
