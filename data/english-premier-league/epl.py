import os
import requests
import pandas as pd
import io
from datetime import datetime

# Tạo thư mục "data" nếu chưa tồn tại
if not os.path.exists('data'):
    os.makedirs('data')

# Lấy năm hiện tại
current_year = datetime.now().year

# Tạo danh sách các năm cho 10 mùa gần nhất
season_years = list(range(current_year - 10, current_year + 1))

# Lưu dữ liệu của từng mùa vào từng file CSV tương ứng
for year in season_years:
    # Tạo URL cho mùa bóng đá
    url = f"https://www.football-data.co.uk/mmz4281/{year % 100:02d}{(year + 1) % 100:02d}/E0.csv"

    # Lấy dữ liệu từ URL và lưu vào DataFrame
    response = requests.get(url)
    data = pd.read_csv(io.StringIO(response.content.decode('utf-8')))

    # Đổi tên file CSV trước khi lưu
    file_name = f"season-{year % 100:02d}.csv"
    if os.path.exists(file_name):
        new_name = f"season-{year % 100:02d}_1.csv"
        os.rename(file_name, new_name)
        file_name = new_name

    # Lưu DataFrame vào file CSV với tên tương ứng với mùa
    data.to_csv(os.path.join('data', file_name), index=False)
