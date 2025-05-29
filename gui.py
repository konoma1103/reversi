import tkinter as tk
from rule import ReversiRule

class ReversiGUI(tk.Frame):

    def __init__(self, side_length:int, master=None):
        """GUIを初期化し、リバーシの盤面を描画
        
            Args:
                side_length(int): 盤面の1辺の長さ(px)
        """
        super().__init__(master)
        self.side_length = side_length

        self.master.title('リバーシ')

        self.reversirule = ReversiRule()

        # 現在のターンを表示するラベルの生成
        self.label = tk.Label(self)
        self.label.pack()

        # 盤面の状態を1つ前に戻す操作をするボタンの生成
        self.button = tk.Button(self, text='ターンを1つ戻る', command=self.turn_back)
        self.button.pack()

        # キャンバスの生成
        self.canvas = tk.Canvas(
            self,
            width=self.side_length,
            height=self.side_length,
            bg='green'
        )
        self.canvas.pack()

        # 描画の更新
        self.update()

        # クリック判定の設定
        self.canvas.bind('<Button-1>', self.click)


    def draw_board(self):
        """マス目の描画を行う関数
        """ 
        # 縦線の描画
        for i in range(1, 8):
            x = (self.side_length / 8) * i
            self.canvas.create_line(x, 0, x, self.side_length)
            
        # 横線の描画
        for i in range(1, 8):
            y = (self.side_length / 8) * i
            self.canvas.create_line(0, y, self.side_length, y)


    def draw_stone(self, x:int, y:int, turn:int):
        """石を描画する関数

            Args:
                x (int): 石を描画する位置の行番号
                y (int): 石を描画する位置の列番号
                turn(int): 現在のターンを表す（1→先攻,0→後攻）
        """
        # 先攻ターンのときは黒の石を描画
        if turn:
            color = 'black'
        # 後攻ターンのときは白の石を描画
        else:
            color = 'white'

        # 石を描画する座標を計算
        x1 = (self.side_length / 8) * y + 5
        y1 = (self.side_length / 8) * x + 5
        x2 = x1 + (self.side_length / 8) - 10
        y2 = y1 + (self.side_length / 8) - 10

        # 石の描画
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)


    def click(self, event):
        """クリックされた位置に石を置く処理を行う関数
        """
        # クリックされた位置の行番号,列番号を取得
        x = int(event.y // (self.side_length / 8))
        y = int(event.x // (self.side_length / 8))

        # 取得した位置が合法手か判定し、配列の値を更新
        legal = self.reversirule.judge_legal(x, y)

        if legal:
            # ターンの切り換え
            self.turn_change()
            # 描画の更新
            self.update()
        
    
    def update(self):
        """描画の更新を行う関数
        """
        # キャンバス内にある全ての図形を削除
        self.canvas.delete('all')

        # マス目を描画
        self.draw_board()

        # ラベルに表示する文字列の更新
        self.label_change()

        # マス目を1つずつ探索し、状態を表す値を取得
        for i in range(len(self.reversirule.space_status)):
            for j in range(len(self.reversirule.space_status[i])):
                status = self.reversirule.space_status[i][j]

                # 参照したマスに石が存在しない場合、スキップする
                if status == None:
                    continue

                # 石の描画
                self.draw_stone(i, j, status)


    def turn_change(self):
        """ターンの切り替え処理を行う関数
        """
        # # 先攻ターンだったときは後攻ターンに切り換え
        # if self.reversirule.turn == 1:
        #     self.reversirule.turn = 0

        # # 後攻ターンだったときは先攻ターンに切り換え
        # elif self.reversirule.turn == 0:
        #     self.reversirule.turn = 1
        
        self.reversirule.turn = [1, 0][self.reversirule.turn]

    def label_change(self):
        """現在のターンを表示するラベルのテキストを変更する関数
        """
        # 先攻ターンのとき、ラベルの表示
        if self.reversirule.turn == 1:
            self.label['text'] = '黒のターン'

        # 後攻ターンのとき、ラベルの表示
        elif self.reversirule.turn == 0:
            self.label['text'] = '白のターン'

    
    def turn_back(self):
        """1つ前のターンに戻る操作を行う関数
        """
        # キャンバス内にある全ての図形を削除
        self.canvas.delete('all')

        # マス目を描画
        self.draw_board()

        # ラベルに表示する文字列の更新
        self.label_change()

        # ターンの変更
        self.turn_change()

        # ラベルに表示する文字列の変更
        self.label_change()

        # 盤面の状態の更新
        self.reversirule.space_status = self.reversirule.previous_space_status

        # マス目を1つずつ探索し、状態を表す値を取得
        for i in range(len(self.reversirule.previous_space_status)):
            for j in range(len(self.reversirule.previous_space_status[i])):
                status = self.reversirule.previous_space_status[i][j]

                # 参照したマスに石が存在しない場合、スキップする
                if status == None:
                    continue

                # 石の描画
                self.draw_stone(i, j, status)


game = ReversiGUI(560)
game.pack()
game.mainloop()