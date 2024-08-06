import time
import sys

#ユーザーによる設定のヒント
#開始状態:q_0,受理状態:q_acc,拒否状態:q_rej
#受理状態(accept!)および拒否状態(reject!)、またはどの遷移規則にも当てはまらない場合(Error)に停止
#空白記号は__init__の中にあるself.blank_symbolで設定
#実行時にmanualとオプションをつけるとエンターで1ステップずつ確認しながら実行できる。

class TuringMachine:
    def __init__(self, tape_input, rules_file):
        self.blank_symbol = "_"
        self.tape = [self.blank_symbol] * 5 + list(tape_input) + [self.blank_symbol] * 5
        self.head_position = 5
        self.fix_position = 0
        self.current_state = "q_0"
        self.accept_state = "q_acc"
        self.reject_state = "q_rej"
        self.transition_rules = self.load_rules(rules_file)

    def load_rules(self, rules_file):
        rules = {}
        with open(rules_file, "r") as file:
            for line in file:
                current_state, read_symbol, write_symbol, next_state, direction = line.strip().split(",")
                rules[(current_state, read_symbol)] = (write_symbol, next_state, direction)
        return rules

    def step(self):
        current_symbol = self.tape[self.head_position]
        key = (self.current_state, current_symbol)

        if key in self.transition_rules:
            write_symbol, next_state, direction = self.transition_rules[key]
            self.tape[self.head_position] = write_symbol
            self.current_state = next_state

            if direction == "R":
                self.head_position += 1
                #print("R")#デバッグ
            elif direction == "L":
                self.head_position -= 1
                #print("L")#デバッグ
            self.print_tape()

            if self.current_state == self.accept_state:
                print("accept!")
                return True
            
            if self.current_state == self.reject_state:
                print("reject!")
                return True

            return False

        else:
            print("Error...halt")
            return True

    def epoch_tape(self):
        for search_leftend in range(len(self.tape)):
            if self.tape[search_leftend] != self.blank_symbol:
                self.tape = [self.blank_symbol] * 5 + self.tape[search_leftend:]
                self.fix_position = self.fix_position - search_leftend + 5 #固定点インデックスの更新
                self.head_position = self.head_position - search_leftend + 5 #ヘッドインデックスの更新
                if (self.head_position < 0) or (self.fix_position < 0):
                    self.tape = [self.blank_symbol] * abs(min(self.fix_position,self.head_position)) + self.tape
                    fix = self.fix_position
                    head = self.head_position
                    self.fix_position += abs(min(fix,head))
                    self.head_position += abs(min(fix,head))
                    
                for search_rightend in range(len(self.tape)):
                    if self.tape[-search_rightend-1] != self.blank_symbol:
                        if search_rightend != 0:
                            self.tape = self.tape[0:-search_rightend] + [self.blank_symbol] * 5
                        elif search_rightend == 0:
                            self.tape = self.tape + [self.blank_symbol] * 5

                        if (self.head_position > len(self.tape) - 1) or (self.fix_position > len(self.tape) - 1):
                            self.tape = self.tape + [self.blank_symbol] * max((self.fix_position-len(self.tape)+1),(self.head_position-len(self.tape)+1))
                        break

                break
            if search_leftend == len(self.tape)-1:#テープ上が空白記号のみになった場合
                self.tape = [self.blank_symbol] * (abs(self.fix_position - self.head_position)+1)
                if self.fix_position >= self.head_position:
                    self.head_position = 0
                    self.fix_position = len(self.tape)-1
                elif self.fix_position < self.head_position:
                    self.fix_position = 0
                    self.head_position = len(self.tape)-1

    def print_tape(self):
        # テープをエポック
        self.epoch_tape()

        # テープを表示し、ヘッドの位置に '*' を追加
        tape_with_spaces = [
            f" {symbol}|" for symbol in self.tape
        ]

        ###↓デバッグコード
        #print("tape_length:"+str(len(self.tape)))
        #print(self.tape)
        #print(self.head_position)
        #print(self.fix_position)
        #print(self.head_position-self.fix_position)
        #print(self.current_state)
        ###

        tape_with_spaces[self.fix_position] = ":" + tape_with_spaces[self.fix_position][1:]#固定点には:マーク
        tape_with_spaces[self.head_position] = "*" + tape_with_spaces[self.head_position][1:]#ヘッド位置には*マーク→:と*が重なったら*が上に乗る。

        print("".join(tape_with_spaces))

    def run(self,manual=False):
        self.print_tape()
        if manual == False:
            while not self.step():
                time.sleep(1)  # 各ステップの間隔
        elif manual == True:
            input()
            while not self.step():
                input()


# 使用例
# ファイルには規則が記載されています (例: "q_0,1,0,q_1,R")

rules_file = "rules.txt"
args = sys.argv
manual = "manual" in args # 引数にmanualを加えるとエンターで1ステップごと自分で進めるモード

# 標準入力から初期テープの内容を受け取る
tape_input = input("初期テープの内容を入力してください : ")

tm = TuringMachine(tape_input, rules_file)
tm.run(manual)
