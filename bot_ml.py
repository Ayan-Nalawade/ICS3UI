import random
import numpy as np
from collections import deque
import sys as _sys

class GameState:
    """Minimal game state for simulation."""

    __slots__ = (
        "p_col", "p_row", "b_col", "b_row",
        "h_walls", "v_walls", "p_sticks", "b_sticks", "to_move",
    )

    def __init__(self):
        self.p_col = 2
        self.p_row = 0
        self.b_col = 3
        self.b_row = 5
        self.h_walls = set()
        self.v_walls = set()
        self.p_sticks = 4
        self.b_sticks = 4
        self.to_move = True

    def copy(self):
        s = GameState()
        s.p_col, s.p_row = self.p_col, self.p_row
        s.b_col, s.b_row = self.b_col, self.b_row
        s.h_walls = set(self.h_walls)
        s.v_walls = set(self.v_walls)
        s.p_sticks, s.b_sticks = self.p_sticks, self.b_sticks
        s.to_move = self.to_move
        return s

    def is_terminal(self):
        if self.p_row == 5 or self.b_row == 0:
            return True
        return len(self.legal_moves(nearby_only=True)) == 0

    def result(self):
        """Return +1 if bot wins, -1 if player wins, 0 otherwise."""
        if self.b_row == 0:
            return 1.0
        if self.p_row == 5:
            return -1.0
        if not self.legal_moves(nearby_only=True):
            if self.to_move:
                return -1.0
            else:
                return 1.0
        return 0.0

    def _occupied(self, col, row):
        return (col == self.p_col and row == self.p_row) or (
            col == self.b_col and row == self.b_row
        )

    def legal_moves(self, nearby_only=False):
        """Return all legal moves for the player whose turn it is.

        Each move is a tuple (action_type, *args):
          'up' / 'down' / 'left' / 'right'
          'h_wall', col, wall_row
          'v_wall', wall_col, row

        When *nearby_only* is True only wall positions within 2 squares
        of either player are returned.
        """
        moves = []
        is_bot = self.to_move
        if is_bot:
            col = self.b_col
            row = self.b_row
            sticks = self.b_sticks
        else:
            col = self.p_col
            row = self.p_row
            sticks = self.p_sticks

        if (
            row < 5
            and (col, row) not in self.h_walls
            and not self._occupied(col, row + 1)
        ):
            moves.append(("up",))
        if (
            row > 0
            and (col, row - 1) not in self.h_walls
            and not self._occupied(col, row - 1)
        ):
            moves.append(("down",))
        if (
            col > 0
            and (col - 1, row) not in self.v_walls
            and not self._occupied(col - 1, row)
        ):
            moves.append(("left",))
        if (
            col < 5
            and (col, row) not in self.v_walls
            and not self._occupied(col + 1, row)
        ):
            moves.append(("right",))

        if sticks > 0:
            if nearby_only:
                player_row, player_col = self.p_row, self.p_col
                bot_row, bot_col = self.b_row, self.b_col
                seen = set()
                for row, col in [(player_row, player_col), (bot_row, bot_col)]:
                    for drow in range(-2, 3):
                        for dcol in range(-2, 3):
                            wall_row = row + drow
                            wall_col = col + dcol
                            if 0 <= wall_col < 6 and 0 <= wall_row < 5:
                                key = ("h", wall_col, wall_row)
                                if key not in seen and (wall_col, wall_row) not in self.h_walls:
                                    seen.add(key)
                                    moves.append(("h_wall", wall_col, wall_row))
                            if 0 <= wall_col < 5 and 0 <= wall_row < 6:
                                key = ("v", wall_col, wall_row)
                                if key not in seen and (wall_col, wall_row) not in self.v_walls:
                                    seen.add(key)
                                    moves.append(("v_wall", wall_col, wall_row))
            else:
                for wcol in range(6):
                    for wrow in range(5):
                        if (wcol, wrow) not in self.h_walls:
                            moves.append(("h_wall", wcol, wrow))
                for wcol in range(5):
                    for wrow in range(6):
                        if (wcol, wrow) not in self.v_walls:
                            moves.append(("v_wall", wcol, wrow))

        random.shuffle(moves)
        return moves

    def apply(self, move):
        """Return a new GameState after applying *move* (does not mutate self)."""
        s = self.copy()
        kind = move[0]

        if kind == "up":
            if s.to_move:
                s.b_row += 1
            else:
                s.p_row += 1
        elif kind == "down":
            if s.to_move:
                s.b_row -= 1
            else:
                s.p_row -= 1
        elif kind == "left":
            if s.to_move:
                s.b_col -= 1
            else:
                s.p_col -= 1
        elif kind == "right":
            if s.to_move:
                s.b_col += 1
            else:
                s.p_col += 1
        elif kind == "h_wall":
            _, wcol, wrow = move
            s.h_walls.add((wcol, wrow))
            if s.to_move:
                s.b_sticks -= 1
            else:
                s.p_sticks -= 1
        elif kind == "v_wall":
            _, wcol, wrow = move
            s.v_walls.add((wcol, wrow))
            if s.to_move:
                s.b_sticks -= 1
            else:
                s.p_sticks -= 1

        s.to_move = not s.to_move
        return s

    def encode(self):
        """Encode this state as a 134-dim float vector (for legacy ML use)."""
        f = np.zeros(134, dtype=np.float32)
        idx = 0
        f[self.p_col * 6 + self.p_row] = 1.0
        idx += 36
        f[idx + self.b_col * 6 + self.b_row] = 1.0
        idx += 36
        for wcol in range(6):
            for wrow in range(5):
                if (wcol, wrow) in self.h_walls:
                    f[idx] = 1.0
                idx += 1
        for wcol in range(5):
            for wrow in range(6):
                if (wcol, wrow) in self.v_walls:
                    f[idx] = 1.0
                idx += 1
        f[idx] = self.p_sticks / 4.0
        idx += 1
        f[idx] = self.b_sticks / 4.0
        return f


def _bfs_path(state, is_bot):
    """BFS from the player to its goal, returning list of (col, row) positions.

    Returns None if no path exists.
    """
    if is_bot:
        start = (state.b_col, state.b_row)
        goal_row = 0
    else:
        start = (state.p_col, state.p_row)
        goal_row = 5



    visited = {start}
    queue = deque()
    queue.append((start, [start]))

    while queue:
        (col, row), path = queue.popleft()
        if row == goal_row:
            return path

        for drow, dcol in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
            next_col, next_row = col + dcol, row + drow
            if next_col < 0 or next_col > 5 or next_row < 0 or next_row > 5:
                continue
            if (next_col, next_row) in visited:
                continue
            if state._occupied(next_col, next_row):
                continue
            if drow == 1 and (col, row) in state.h_walls:
                continue
            if drow == -1 and (col, row - 1) in state.h_walls:
                continue
            if dcol == -1 and (col - 1, row) in state.v_walls:
                continue
            if dcol == 1 and (col, row) in state.v_walls:
                continue
            visited.add((next_col, next_row))
            queue.append(((next_col, next_row), path + [(next_col, next_row)]))

    return None


def _move_toward_goal(state):
    """If a path to the goal exists, return the first move along it."""
    is_bot = state.to_move
    path = _bfs_path(state, is_bot)
    if path is None or len(path) < 2:
        return None

    col, row = path[0]
    next_col, next_row = path[1]
    dcol, drow = next_col - col, next_row - row

    if drow == 1:
        return ("up",)
    if drow == -1:
        return ("down",)
    if dcol == -1:
        return ("left",)
    if dcol == 1:
        return ("right",)
    return None


def _fmt_move(move):
    """Return a human-readable string for a move tuple."""
    kind = move[0]
    if kind in ("up", "down", "left", "right"):
        return kind
    if kind == "h_wall":
        col = chr(ord("A") + move[1])
        row = move[2] + 1
        return f"h_wall {col}{row}-{col}{row+1}"
    if kind == "v_wall":
        col = chr(ord("A") + move[1])
        col2 = chr(ord("A") + move[1] + 1)
        row = move[2] + 1
        return f"v_wall {col}{row}-{col2}{row}"
    return str(move)


def _fmt_pos(col, row):
    return f"{chr(ord('A') + col)}{row + 1}"


def _heuristic_opponent_move(state, block_chance=0.4):
    """Pick a move for the opponent (player) using BFS + path-blocking."""
    if state.p_sticks > 0 and random.random() < block_chance:
        bot_path = _bfs_path(state, is_bot=True)
        if bot_path and len(bot_path) >= 3:
            candidates = []
            for i in range(1, len(bot_path) - 1):
                col, row = bot_path[i - 1]
                next_col, next_row = bot_path[i]
                dcol, drow = next_col - col, next_row - row
                if drow == 1 and (col, row) not in state.h_walls:
                    candidates.append(("h_wall", col, row))
                elif drow == -1:
                    wall_row = row - 1
                    if 0 <= wall_row < 5 and (col, wall_row) not in state.h_walls:
                        candidates.append(("h_wall", col, wall_row))
                elif dcol == -1:
                    wall_col = col - 1
                    if 0 <= wall_col < 5 and (wall_col, row) not in state.v_walls:
                        candidates.append(("v_wall", wall_col, row))
                elif dcol == 1 and (col, row) not in state.v_walls:
                    candidates.append(("v_wall", col, row))
            if candidates:
                wall = random.choice(candidates)
                if wall in state.legal_moves(nearby_only=False):
                    return wall

    opp_path = _bfs_path(state, is_bot=False)
    if opp_path and len(opp_path) >= 2:
        col, row = opp_path[0]
        next_col, next_row = opp_path[1]
        dcol, drow = next_col - col, next_row - row
        if drow == 1:
            move = ("up",)
        elif drow == -1:
            move = ("down",)
        elif dcol == -1:
            move = ("left",)
        elif dcol == 1:
            move = ("right",)
        else:
            move = None
        if move is not None and move in state.legal_moves(nearby_only=False):
            return move

    moves = state.legal_moves(nearby_only=True)
    if moves:
        return random.choice(moves)
    return None


def _block_opponent_path(state):
    """Place a wall on the opponent's shortest path."""
    opp_path = _bfs_path(state, is_bot=False)
    if opp_path and len(opp_path) >= 3:
        for i in range(1, len(opp_path) - 1):
            col, row = opp_path[i - 1]
            next_col, next_row = opp_path[i]
            dcol, drow = next_col - col, next_row - row
            if drow == 1 and (col, row) not in state.h_walls and state.b_sticks > 0:
                return ("h_wall", col, row)
            if drow == -1:
                wall_row = row - 1
                if 0 <= wall_row < 5 and (col, wall_row) not in state.h_walls and state.b_sticks > 0:
                    return ("h_wall", col, wall_row)
            if dcol == -1:
                wall_col = col - 1
                if 0 <= wall_col < 5 and (wall_col, row) not in state.v_walls and state.b_sticks > 0:
                    return ("v_wall", wall_col, row)
            if dcol == 1 and (col, row) not in state.v_walls and state.b_sticks > 0:
                return ("v_wall", col, row)
    return None


def pick_action_blocker(state, verbose=False):
    """Block the opponent's shortest path, otherwise BFS-move toward goal.

    This is a purely deterministic strategy -- no ML, no weights.
    Uses 4 walls to trap the opponent, then sprints to the goal.
    """
    if state.b_sticks > 0:
        wall = _block_opponent_path(state)
        if wall is not None:
            if verbose:
                print(f"  blocker from {_fmt_pos(state.b_col, state.b_row)}: "
                      f"blocking opp with {_fmt_move(wall)}")
            return wall

    bfs = _move_toward_goal(state)
    if bfs is not None:
        if verbose:
            print(f"  blocker from {_fmt_pos(state.b_col, state.b_row)}: "
                  f"moving with {_fmt_move(bfs)}")
        return bfs

    moves = state.legal_moves(nearby_only=True)
    if verbose:
        print(f"  blocker from {_fmt_pos(state.b_col, state.b_row)}: "
              f"fallback ({len(moves)} moves)")
    if moves:
        return random.choice(moves)
    return None


if __name__ == "__main__":
    if "--eval" in _sys.argv:
        arg_index = _sys.argv.index("--eval")
        if len(_sys.argv) > arg_index + 1:
            n = int(_sys.argv[arg_index + 1])
        else:
            n = 200
        print(f"Evaluating on {n} games vs heuristic opponent…")
        wins = 0
        for _ in range(n):
            state = GameState()
            while not state.is_terminal():
                if state.to_move:
                    m = pick_action_blocker(state)
                else:
                    m = _heuristic_opponent_move(state)
                if m is None:
                    break
                state = state.apply(m)
            if state.result() > 0:
                wins += 1
        print(f"Bot wins: {wins}/{n} ({100 * wins // n}%)")
    else:
        print("Usage: python bot_ml.py --eval [N]")
