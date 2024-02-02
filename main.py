import random
import re


def main():
    # xdxxx形式の入力を受け取り、それに対応するサイコロの目を出力するプログラム
    input_dice = input("dice:")
    # xdxxx形式で入力されているかの判定
    # 正規表現を作成
    pattern = r"^(d[1-9][0-9]{0,2}|[1-9][0-9]{0,2}d[1-9][0-9]{0,2})$"
    # マッチするかの判定
    if not re.match(pattern, input_dice):
        print("Invalid input")
        return
    # 入力された値の前半と後半を分ける
    input_list = input_dice.split("d")
    # ダイスの数が指定されていない場合は1を挿入
    if input_list[0] == "":
        input_list[0] = "1"

    # ダイスの数と面数をint型に変換
    input_list = list(map(int, input_list))

    # 結果用のリストを作成
    result = []
    for i in range(input_list[0]):
        result.append(random.randint(1, input_list[1]))
    # 結果を出力
    print(f"({sum(result)}) < {result}")


if __name__ == "__main__":
    while True:
        main()
