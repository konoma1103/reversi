class ReversiRule:
    
    def __init__(self):
        
        # どちらのターンかを表す値（1:先攻, 0:後攻）
        self.turn = 1

        # マスごとの状態を表す配列
        self.space_status = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, 0, 1, None, None, None],
            [None, None, None, 1, 0, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
          ]

        # 方向定数
        self.dxy = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))

        # 1つ前のターンの盤面を保存する配列
        self.previous_space_status = [[None]*8 for _ in range(8)]


    def judge_legal(self, x: int, y: int)-> bool:
        """打った手が合法手か判定する関数

            Args:
                x (int): 打った手のX座標
                y (int): 打った手のY座標

            Returns:
                bool: 打った手が合法手かどうか
        """
        # 打った手が合法手なのか保持する変数
        legal = False

        # 既にマスに石がある場合は合法手でないと判定
        if self.space_status[x][y] is not None:
            return legal
        
        # 盤面の状態を更新する前に保存しておく
        self.previous_space_status = [i[:] for i in self.space_status]

        # 打った手で相手の石を裏返せるかの判断
        for dx,dy in self.dxy:
            x_next = x + dx
            y_next = y + dy

            # 任意の方向へ1マス進んだ先がフィールド内であるかの判断
            if (x_next < 0 or 7 < x_next) or (y_next < 0 or 7 < y_next):
                continue

            # 任意の方向へ1マス進んだ先に相手の石があるかの判断
            if self.space_status[x_next][y_next] != self.turn and self.space_status[x_next][y_next] != None:
                
                # 同じ方向のマスに自分の石があるかの判断
                for i in range(7):
                    x_next += dx
                    y_next += dy

                    # 進んだ先がフィールド内であるかの判断(try文で代用可)
                    if (x_next < 0 or 7 < x_next) or (y_next < 0 or 7 < y_next):
                        break
                    
                    else:
                        next_stone = self.space_status[x_next][y_next]
                        # 進んだ先に自分の石があるかの判断
                        if next_stone == self.turn:
                            
                            # 打った位置に自分の石を配置し、挟まれた敵の石を裏返す
                            self.flip(x, y, dx, dy, x_next, y_next, self.turn)

                            # 打った手が合法手であることを保存する
                            legal = True

                            # この方向への探索を終了する
                            break

                        elif next_stone is None:
                            break
        return legal

    
    def flip(self, x:int, y:int, dx:int, dy:int, x_next:int, y_next:int, turn:int)->None:
        """石の状態を更新する関数

            打った座標に石を配置し、挟まれた敵の石を裏返す

            Args:
                x (int): 石を置いた位置のx座標
                y (int): 石を置いた位置のy座標
                dx(int): 裏返しの方向のx座標
                dy(int): 裏返しの方向のy座標
                x_next(int): 裏返す方向にあった自分の石のx座標
                y_next(int): 裏返す方向にあった自分の石のy座標
                turn (int): 現在が先攻か後攻かを判別する変数
        """
        # 探索する座標が石を置いた座標と一致するまで繰返し
        while x_next != x or y_next != y:
            # 探索する座標を進める
            x_next -= dx
            y_next -= dy

            # 石を反転
            self.space_status[x_next][y_next] = turn


    def judge_end(self):
        """ゲームの終了を判定する関数
        """
        # 盤面のマスが全て埋まったら終了
        if self.space_status is not None:
            self.judge_result()
        
        # 合法手がなくなったら終了


    def judge_result(self):
        """勝敗を判定する関数
        """