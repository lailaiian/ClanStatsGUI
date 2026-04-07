import requests
import tkinter as tk
from tkinter import ttk
# ---------- 設定 ----------!!!重要資料!!!
API_TOKEN = "保密"
CLAN_TAG = "保密"  # 記得 # 替換成 %23

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# ---------- 取得部落資訊 ----------
def get_clan_data():
    clan_url = f"https://api.clashofclans.com/v1/clans/{CLAN_TAG.replace('#','%23')}"
    resp = requests.get(clan_url, headers=headers)
    if resp.status_code != 200:
        tk.messagebox.showerror("錯誤", f"取得部落資料失敗: {resp.status_code}")
        return None
    return resp.json()

def get_members_data():
    members_url = f"https://api.clashofclans.com/v1/clans/{CLAN_TAG.replace('#','%23')}/members"
    resp = requests.get(members_url, headers=headers)
    if resp.status_code != 200:
        tk.messagebox.showerror("錯誤", f"取得部落成員失敗: {resp.status_code}")
        return []
    return resp.json().get("items", [])

root = tk.Tk()
root.title("部落成員資訊")

# 標題
clan_info = get_clan_data()
if clan_info:
    title = f"{clan_info.get('name')} ({clan_info.get('tag')}) 等級: {clan_info.get('clanLevel')} 成員數: {clan_info.get('members')}"
else:
    title = "部落資訊抓取失敗"
label = tk.Label(root, text=title, font=("Arial", 14))
label.pack(pady=10)

columns = ("玩家名稱", "標籤", "等級", "獎盃", "捐出", "收到")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

# 記錄排序方向
# False = 高→低（箭頭↓）
# True = 低→高（箭頭↑）
sort_orders = {col: False for col in columns}  
current_sort = {"col": None}  # 上一次點擊的欄位

def sort_column(col):
    global sort_orders, current_sort
    data = [(tree.set(k, col), k) for k in tree.get_children('')]
    if col in ["等級", "獎盃", "捐出", "收到"]:
        data = [(int(v), k) for v, k in data]

    # 判斷是否是同一欄位
    if current_sort["col"] == col:
        # 同欄位：切換排序方向
        reverse = not sort_orders[col]
        sort_orders[col] = reverse
    else:
        # 新欄位：固定高→低
        reverse = True
        sort_orders[col] = True

    # 排序
    data.sort(reverse=reverse)
    for index, (val, k) in enumerate(data):
        tree.move(k, '', index)

    # 更新目前排序欄位
    current_sort["col"] = col
    update_heading_arrow()

def update_heading_arrow():
    """更新標題箭頭顯示"""
    for col in columns:
        if current_sort["col"] == col:
            arrow = "↑" if sort_orders[col] else "↓"
            tree.heading(col, text=f"{col} {arrow}", command=lambda c=col: sort_column(c))
        else:
            tree.heading(col, text=col, command=lambda c=col: sort_column(c))

# 設定欄位標題
for col in columns:
    tree.heading(col, text=col, command=lambda c=col: sort_column(c))
    tree.column(col, width=100, anchor="center")

# 滾動條
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(side="left", fill="both", expand=True)

# 填入資料
members_data = get_members_data()
for member in members_data:
    tree.insert("", "end", values=(
        member.get("name", ""),
        member.get("tag", ""),
        member.get("expLevel", 0),
        member.get("trophies", 0),
        member.get("donations", 0),
        member.get("donationsReceived", 0)
    ))

root.mainloop()