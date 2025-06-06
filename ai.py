import numpy as np

PIECE_TO_INDEX = {
    "wK": 0, "wQ": 1, "wR": 2, "wB": 3, "wN": 4, "wp": 5,
    "bK": 6, "bQ": 7, "bR": 8, "bB": 9, "bN": 10, "bp": 11
}

INDEX_TO_PIECE = { v:k for k, v in PIECE_TO_INDEX.items()}

def encode_board(board):
    """
    Encodes the 8x8 board into a (12, 8, 8) tensor (channel per piece type).
    """
    encoded = np.zeros((12, 8, 8), dtype=np.float32)
    for r in range(8):
        for c in range(8):
            square = board[r][c]
            if square != "--":
                idx = PIECE_TO_INDEX[square]
                encoded[idx, r, c] = 1
    return encoded

def decode_move_index(index):
    """
    Converts a flat index (0-4095) back to a move (start_row, start_col, end_row, end_col).
    """
    start = index // 64
    end = index % 64
    return(start // 8, start % 8 , end // 8, end % 8)

def encode_move(start_row, start_col, end_row, end_col):
    """
    Converts a move into a flat index (0-4095) for a classifier output.
    """
    start = start_row * 8 + start_col
    end = end_row * 8 + end_col
    return start * 64 + end 