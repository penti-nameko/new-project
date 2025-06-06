# ベースイメージ
FROM python:3.11-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要ファイルをコピー
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ポートを開ける（ヘルスチェック用）
EXPOSE 8080

# 起動コマンド
CMD ["python", "bot.py"]
