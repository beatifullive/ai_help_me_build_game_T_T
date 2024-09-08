import pygame
import sys
import time

# 初始化Pygame
pygame.init()

# 设置屏幕大小
screen = pygame.display.set_mode((1000, 800))  # 增加宽度以显示信息
pygame.display.set_caption("象棋游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 加载资源
def load_piece_images():
    piece_names = ["车", "马", "象", "士", "将", "炮", "兵", "卒"]
    piece_images = {}
    for name in piece_names:
        piece_images[f"{name}_red"] = pygame.image.load(f"xiangqiyoux/{name}_red.png")
        piece_images[f"{name}_black"] = pygame.image.load(f"xiangqiyoux/{name}_black.png")
    return piece_images

piece_images = load_piece_images()

# 定义棋盘和棋子
class Board:
    def __init__(self):
        self.tiles = self.create_tiles()
        self.pieces = self.create_pieces()
        self.red_score = 0
        self.black_score = 0
        self.red_thinking_time = 0
        self.black_thinking_time = 0
        self.red_total_time = 0
        self.black_total_time = 0
        self.start_time = time.time()

    def create_tiles(self):
        tiles = []
        for row in range(10):
            row_tiles = []
            for col in range(9):
                row_tiles.append({"row": row, "col": col})
            tiles.append(row_tiles)
        return tiles

    def create_pieces(self):
        pieces = []
        # 红方棋子
        pieces.append(Piece("车", RED, (0, 0), piece_images["车_red"]))
        pieces.append(Piece("马", RED, (0, 1), piece_images["马_red"]))
        pieces.append(Piece("象", RED, (0, 2), piece_images["象_red"]))
        pieces.append(Piece("士", RED, (0, 3), piece_images["士_red"]))
        pieces.append(Piece("将", RED, (0, 4), piece_images["将_red"]))
        pieces.append(Piece("士", RED, (0, 5), piece_images["士_red"]))
        pieces.append(Piece("象", RED, (0, 6), piece_images["象_red"]))
        pieces.append(Piece("马", RED, (0, 7), piece_images["马_red"]))
        pieces.append(Piece("车", RED, (0, 8), piece_images["车_red"]))
        pieces.append(Piece("炮", RED, (2, 1), piece_images["炮_red"]))
        pieces.append(Piece("炮", RED, (2, 7), piece_images["炮_red"]))
        for i in range(0, 9, 2):
            pieces.append(Piece("兵", RED, (3, i), piece_images["兵_red"]))
        
        # 黑方棋子
        pieces.append(Piece("车", BLACK, (9, 0), piece_images["车_black"]))
        pieces.append(Piece("马", BLACK, (9, 1), piece_images["马_black"]))
        pieces.append(Piece("象", BLACK, (9, 2), piece_images["象_black"]))
        pieces.append(Piece("士", BLACK, (9, 3), piece_images["士_black"]))
        pieces.append(Piece("将", BLACK, (9, 4), piece_images["将_black"]))
        pieces.append(Piece("士", BLACK, (9, 5), piece_images["士_black"]))
        pieces.append(Piece("象", BLACK, (9, 6), piece_images["象_black"]))
        pieces.append(Piece("马", BLACK, (9, 7), piece_images["马_black"]))
        pieces.append(Piece("车", BLACK, (9, 8), piece_images["车_black"]))
        pieces.append(Piece("炮", BLACK, (7, 1), piece_images["炮_black"]))
        pieces.append(Piece("炮", BLACK, (7, 7), piece_images["炮_black"]))
        for i in range(0, 9, 2):
            pieces.append(Piece("卒", BLACK, (6, i), piece_images["卒_black"]))
        
        return pieces

    def draw(self, screen):
        screen.fill(WHITE)
        for row in self.tiles:
            for tile in row:
                pygame.draw.rect(screen, BLACK, (tile["col"] * 80, tile["row"] * 80, 80, 80), 1)
        for piece in self.pieces:
            piece.draw(screen)
        self.draw_info(screen)
        self.draw_river(screen)

    def draw_info(self, screen):
        font = pygame.font.Font("simhei.ttf", 16)  # 使用中文字体
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        red_score_text = f"红方积分: {self.red_score}"
        black_score_text = f"黑方积分: {self.black_score}"
        red_thinking_time_text = f"红方思考时间: {self.red_thinking_time:.2f}秒"
        black_thinking_time_text = f"黑方思考时间: {self.black_thinking_time:.2f}秒"
        red_total_time_text = f"红方累计时间: {self.red_total_time:.2f}秒"
        black_total_time_text = f"黑方累计时间: {self.black_total_time:.2f}秒"

        texts = [
            current_time,
            red_score_text,
            black_score_text,
            red_thinking_time_text,
            black_thinking_time_text,
            red_total_time_text,
            black_total_time_text
        ]

        for i, text in enumerate(texts):
            rendered_text = font.render(text, True, BLACK)
            screen.blit(rendered_text, (820, 10 + i * 40))

    def draw_river(self, screen):
        font = pygame.font.Font("simhei.ttf", 48)  # 使用中文字体
        river_text = "楚河        汉界"
        rendered_text = font.render(river_text, True, BLACK)
        screen.blit(rendered_text, (240, 360))

    def update_thinking_time(self, turn):
        current_time = time.time()
        if turn == RED:
            self.red_thinking_time = current_time - self.start_time
        else:
            self.black_thinking_time = current_time - self.start_time

    def switch_turn(self, turn):
        current_time = time.time()
        if turn == RED:
            self.red_total_time += current_time - self.start_time
            self.red_thinking_time = 0
        else:
            self.black_total_time += current_time - self.start_time
            self.black_thinking_time = 0
        self.start_time = current_time

    def get_piece_at(self, position):
        for piece in self.pieces:
            if piece.position == position:
                return piece
        return None

    def move_piece(self, piece, new_position):
        if not self.is_valid_move(piece, new_position):
            return False
        target_piece = self.get_piece_at(new_position)
        if target_piece:
            if target_piece.color != piece.color:
                self.pieces.remove(target_piece)  # 吃掉对方棋子
            else:
                return False  # 不能移动到己方棋子的位置
        piece.move(new_position)
        return True

    def is_valid_move(self, piece, new_position):
        row, col = new_position
        if row < 0 or row >= 10 or col < 0 or col >= 9:
            return False
        if piece.name == "车":
            return self.is_valid_rook_move(piece, new_position)
        elif piece.name == "马":
            return self.is_valid_knight_move(piece, new_position)
        elif piece.name == "象":
            return self.is_valid_elephant_move(piece, new_position)
        elif piece.name == "士":
            return self.is_valid_guard_move(piece, new_position)
        elif piece.name == "将":
            return self.is_valid_king_move(piece, new_position)
        elif piece.name == "炮":
            return self.is_valid_cannon_move(piece, new_position)
        elif piece.name == "兵" or piece.name == "卒":
            return self.is_valid_pawn_move(piece, new_position)
        return False

    def is_valid_rook_move(self, piece, new_position):
        row, col = piece.position
        new_row, new_col = new_position
        if row != new_row and col != new_col:
            return False
        if row == new_row:
            step = 1 if new_col > col else -1
            for c in range(col + step, new_col, step):
                if self.get_piece_at((row, c)):
                    return False
        if col == new_col:
            step = 1 if new_row > row else -1
            for r in range(row + step, new_row, step):
                if self.get_piece_at((r, col)):
                    return False
        return True

    def is_valid_knight_move(self, piece, new_position):
        row, col = piece.position
        new_row, new_col = new_position
        if (abs(new_row - row), abs(new_col - col)) not in [(2, 1), (1, 2)]:
            return False
        if abs(new_row - row) == 2:
            if self.get_piece_at(((row + new_row) // 2, col)):
                return False
        if abs(new_col - col) == 2:
            if self.get_piece_at((row, (col + new_col) // 2)):
                return False
        return True

    def is_valid_elephant_move(self, piece, new_position):
        row, col = piece.position
        new_row, new_col = new_position
        if abs(new_row - row) != 2 or abs(new_col - col) != 2:
            return False
        if piece.color == RED and new_row > 4:
            return False
        if piece.color == BLACK and new_row < 5:
            return False
        if self.get_piece_at(((row + new_row) // 2, (col + new_col) // 2)):
            return False
        return True

    def is_valid_guard_move(self, piece, new_position):
        row, col = piece.position
        new_row, new_col = new_position
        if abs(new_row - row) != 1 or abs(new_col - col) != 1:
            return False
        if new_col < 3 or new_col > 5:
            return False
        if piece.color == RED and new_row > 2:
            return False
        if piece.color == BLACK and new_row < 7:
            return False
        return True

    def is_valid_king_move(self, piece, new_position):
        row, col = piece.position
        new_row, new_col = new_position
        if abs(new_row - row) + abs(new_col - col) != 1:
            return False
        if new_col < 3 or new_col > 5:
            return False
        if piece.color == RED and new_row > 2:
            return False
        if piece.color == BLACK and new_row < 7:
            return False
        return True

    def is_valid_cannon_move(self, piece, new_position):
        row, col = piece.position
        new_row, new_col = new_position
        if row != new_row and col != new_col:
            return False
        if row == new_row:
            step = 1 if new_col > col else -1
            count = 0
            for c in range(col + step, new_col, step):
                if self.get_piece_at((row, c)):
                    count += 1
            if count > 1 or (count == 0 and self.get_piece_at(new_position)):
                return False
            if count == 1 and not self.get_piece_at(new_position):
                return False
        if col == new_col:
            step = 1 if new_row > row else -1
            count = 0
            for r in range(row + step, new_row, step):
                if self.get_piece_at((r, col)):
                    count += 1
            if count > 1 or (count == 0 and self.get_piece_at(new_position)):
                return False
            if count == 1 and not self.get_piece_at(new_position):
                return False
        return True

    def is_valid_pawn_move(self, piece, new_position):
        row, col = piece.position
        new_row, new_col = new_position
        if piece.color == RED:
            if new_row < row:
                return False
            if row <= 4 and new_row == row:
                return False
        if piece.color == BLACK:
            if new_row > row:
                return False
            if row >= 5 and new_row == row:
                return False
        if abs(new_row - row) + abs(new_col - col) != 1:
            return False
        return True

    def check_king_face_to_face(self):
        red_king = None
        black_king = None
        for piece in self.pieces:
            if piece.name == "将" and piece.color == RED:
                red_king = piece
            elif piece.name == "将" and piece.color == BLACK:
                black_king = piece
        if red_king and black_king and red_king.position[1] == black_king.position[1]:
            col = red_king.position[1]
            min_row = min(red_king.position[0], black_king.position[0])
            max_row = max(red_king.position[0], black_king.position[0])
            for row in range(min_row + 1, max_row):
                if self.get_piece_at((row, col)):
                    return False
            return True
        return False

    def check_victory(self):
        red_king = any(piece.name == "将" and piece.color == RED for piece in self.pieces)
        black_king = any(piece.name == "将" and piece.color == BLACK for piece in self.pieces)
        if not red_king:
            self.black_score += 2
            return "黑方胜利"
        if not black_king:
            self.red_score += 2
            return "红方胜利"
        if self.check_king_face_to_face():
            if turn == RED:
                self.black_score += 2
                return "黑方胜利"
            else:
                self.red_score += 2
                return "红方胜利"
        return None

class Piece:
    def __init__(self, name, color, position, image):
        self.name = name
        self.color = color
        self.position = position
        self.image = image

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.position[1] * 80, self.position[0] * 80))
        else:
            font = pygame.font.Font("simhei.ttf", 36)  # 使用中文字体
            text = font.render(self.name, True, self.color)
            screen.blit(text, (self.position[1] * 80 + 20, self.position[0] * 80 + 20))

    def move(self, new_position):
        self.position = new_position

def draw_buttons(screen):
    font = pygame.font.Font("simhei.ttf", 36)
    restart_button = pygame.Rect(820, 400, 160, 50)
    quit_button = pygame.Rect(820, 460, 160, 50)
    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, RED, quit_button)
    restart_text = font.render("重新开始", True, BLACK)
    quit_text = font.render("退出游戏", True, BLACK)
    screen.blit(restart_text, (830, 410))
    screen.blit(quit_text, (830, 470))
    return restart_button, quit_button

def reset_game():
    global board, turn, selected_piece, victory_message, running
    board = Board()
    turn = RED
    selected_piece = None
    victory_message = None
    running = True

# 初始化棋盘和棋子
board = Board()

# 主游戏循环
running = True
selected_piece = None
turn = RED  # 红方先行
victory_message = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if restart_button.collidepoint(x, y):
                reset_game()
            elif quit_button.collidepoint(x, y):
                running = False
            else:
                col, row = x // 80, y // 80
                if selected_piece:
                    if board.move_piece(selected_piece, (row, col)):
                        victory_message = board.check_victory()
                        if victory_message:
                            print(victory_message)
                            running = False
                        turn = BLACK if turn == RED else RED  # 切换回合
                        board.switch_turn(turn)
                    selected_piece = None
                else:
                    piece = board.get_piece_at((row, col))
                    if piece and piece.color == turn:
                        selected_piece = piece

    # 更新思考时间
    board.update_thinking_time(turn)

    # 绘制游戏元素
    board.draw(screen)

    # 绘制按钮
    restart_button, quit_button = draw_buttons(screen)

    # 更新屏幕
    pygame.display.flip()

# 显示胜利信息
if victory_message:
    font = pygame.font.Font("simhei.ttf", 72)
    text = font.render(victory_message, True, RED if "红方" in victory_message else BLACK)
    screen.blit(text, (200, 400))
    pygame.display.flip()
    pygame.time.wait(3000)

# 显示积分信息
font = pygame.font.Font("simhei.ttf", 36)
score_text = f"红方积分: {board.red_score}  黑方积分: {board.black_score}"
text = font.render(score_text, True, BLACK)
screen.blit(text, (200, 500))
pygame.display.flip()
pygame.time.wait(3000)

# 退出Pygame
pygame.quit()
sys.exit()

def draw_buttons(screen):
    font = pygame.font.Font("simhei.ttf", 36)
    restart_button = pygame.Rect(820, 400, 160, 50)
    quit_button = pygame.Rect(820, 460, 160, 50)
    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, RED, quit_button)
    restart_text = font.render("重新开始", True, BLACK)
    quit_text = font.render("退出游戏", True, BLACK)
    screen.blit(restart_text, (830, 410))
    screen.blit(quit_text, (830, 470))
    return restart_button, quit_button

def reset_game():
    global board, turn, selected_piece, victory_message, running
    board = Board()
    turn = RED
    selected_piece = None
    victory_message = None
    running = True

# 初始化棋盘和棋子
board = Board()

# 主游戏循环
running = True
selected_piece = None
turn = RED  # 红方先行
victory_message = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if restart_button.collidepoint(x, y):
                reset_game()
            elif quit_button.collidepoint(x, y):
                running = False
            else:
                col, row = x // 80, y // 80
                if selected_piece:
                    if board.move_piece(selected_piece, (row, col)):
                        victory_message = board.check_victory()
                        if victory_message:
                            print(victory_message)
                            running = False
                        turn = BLACK if turn == RED else RED  # 切换回合
                        board.switch_turn(turn)
                    selected_piece = None
                else:
                    piece = board.get_piece_at((row, col))
                    if piece and piece.color == turn:
                        selected_piece = piece

    # 更新思考时间
    board.update_thinking_time(turn)

    # 绘制游戏元素
    board.draw(screen)

    # 绘制按钮
    restart_button, quit_button = draw_buttons(screen)

    # 更新屏幕
    pygame.display.flip()

# 显示胜利信息
if victory_message:
    font = pygame.font.Font("simhei.ttf", 72)
    text = font.render(victory_message, True, RED if "红方" in victory_message else BLACK)
    screen.blit(text, (200, 400))
    pygame.display.flip()
    pygame.time.wait(3000)

# 显示积分信息
font = pygame.font.Font("simhei.ttf", 36)
score_text = f"红方积分: {board.red_score}  黑方积分: {board.black_score}"
text = font.render(score_text, True, BLACK)
screen.blit(text, (200, 500))
pygame.display.flip()
pygame.time.wait(3000)

# 退出Pygame
pygame.quit()
sys.exit()