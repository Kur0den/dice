import random
import re
import asyncio
import json
from os import environ as env

import websockets
from dotenv import load_dotenv
from misskey import Misskey

load_dotenv()
misskey_domain = "chpk.kur0den.net"


mk = Misskey(misskey_domain, i = env["MISSKEY_TOKEN"])
mk_id = mk.i()['id']
ws_url = f'wss://{misskey_domain}/streaming?i={env["MISSKEY_TOKEN"]}'


async def runner(): # めいんのたすく
    async with websockets.connect(ws_url) as ws: # type: ignore  ##websocketに接続
        await ws.send(json.dumps({
            'type': 'connect',
            'body': {
                'channel': 'main',
                'id': '1'
            } # mainチャンネルに接続
        }))
        while True:
            msg = json.loads(await ws.recv())
            if msg['body']['type'] == 'mention': # メンション時に反応
                note_id = msg['body']['body']['id']
                content = msg['body']['body']['text']
                # 正規表現を作成
                pattern = r"(d[1-9][0-9]{0,4}|[1-9][0-9]{0,4}d[1-9][0-9]{0,4})" # d100, 1d100のような形式にマッチ

                match = re.search(pattern, content)
                if match is None:
                    mk.notes_reactions_create(note_id=note_id, reaction="❌")
                    continue
                else:
                    mk.notes_reactions_create(note_id=note_id, reaction="🎲")
                # マッチした文字列を取得
                input_dice = re.search(pattern, content).group()
                # 入力された値の前半と後半を分ける
                input_list = input_dice.split("d")
                # ダイスの数が指定されていない場合は1を挿入
                if input_list[0] == "":
                    input_list[0] = "1"

                # ダイスの数と面数をint型に変換
                input_list = list(map(int, input_list))

                # 結果用のリストを作成
                result = []
                f_count = 0
                c_count = 0
                for i in range(input_list[0]):
                    rand_int = random.randint(1, input_list[1])
                    result.append(rand_int)

                    # 下5%をクリティカル、上5%をファンブルとしてカウント
                    percent = input_list[1] * 0.05
                    if rand_int <= percent:
                        c_count += 1
                    elif rand_int >= input_list[1] - percent:
                        f_count += 1
                # 結果を出力
                result_cut = False
                result_len = len(result)
                if len(result) > 10:
                    result = result[:10]
                    result_cut = True
                result = f"({sum(result)}) < {result}"

                if result_cut:
                    result = result[:-1] + ", ...]"
                result += f" ({input_list[0]})"

                if c_count > 0:
                    result += f"\nCritical x{c_count}"
                if f_count > 0:
                    result += f"\nFumble x{f_count}"
                if result_cut:
                    result += f"\n(The {result_len - 10} roll has been cut.)"



                user_name = msg['body']['body']['user']['username']
                user_host = msg['body']['body']['user']['host']
                if user_host == None:
                    text= f'@{user_name} {result}'
                else:
                    text = f'@{user_name}@{user_host} {result}'


                mk.notes_create(text=text, reply_id=note_id) # 結果を返信



print('ready')
asyncio.get_event_loop().run_until_complete(runner()) # runner()を実行
