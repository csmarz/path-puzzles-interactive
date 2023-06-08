import itertools
from pysat.solvers import MinisatGH

# Path instance
m, n = -1, -1
start_x, start_y, finish_x, finish_y = -1, -1, -1, -1
cr, cc = [], []

# Helpers
dirs = ['d', 'l', 'r', 'u']
move = { 'd': (1,0), 'l': (0,-1), 'r': (0,1), 'u': (-1,0) }
max_lit = 0 # to track the biggest integer used to represent literals

def is_valid(i, j):
  return 0 <= i < m and 0 <= j < n
def get_adjacents(i, j):
  return [(i+dx, j+dy) for dx, dy in move.values() if is_valid(i+dx, j+dy)]

# Cardinality constraints
def atMost(lits, bound):
  combinations = list(map(list, itertools.combinations(lits, bound+1)))
  return [[-v for v in comb] for comb in combinations]
def equals(lits, bound): return atMost(lits, bound) + atMost([-v for v in lits], len(lits)-bound)

def solve_puzzle(cfg):
  global m, n
  global start_x, start_y, finish_x, finish_y
  global cr, cc
  global max_lit

  m = cfg.get('m')
  n = cfg.get('n')
  start_x = cfg.get('start_x')
  start_y = cfg.get('start_y')
  finish_x = cfg.get('finish_x')
  finish_y = cfg.get('finish_y')
  cr = cfg.get('cr')
  cc = cfg.get('cc')

  lower_bound_row = sum([val for val in cr if val != -1])
  upper_bound_row = sum([(val if val != -1 else n) for val in cr])
  lower_bound_col = sum([val for val in cc if val != -1])
  upper_bound_col = sum([(val if val != -1 else m) for val in cc])
  ds = abs(finish_y - start_y) + abs(finish_x - start_x)
  lb = max(lower_bound_col, lower_bound_row, ds+1)
  ub = min(upper_bound_col, upper_bound_row)

  found = False
  for path_len in range(lb, ub + 1):
    solver = MinisatGH()

    # A bijective function that maps V(i,j,t) to a unique integer
    def V(i: int, j: int, t: int) -> int:
      return t + j*path_len + i*path_len*n + 1

    max_lit = V(m-1, n-1, path_len-1)

    # Configure start and finish cells
    solver.add_clause([V(start_x, start_y, 0)])
    solver.add_clause([V(finish_x, finish_y, path_len-1)])

    # Configure rule: if true for some cell (i,j), then one of its adjacent cells must be true
    for t in range(path_len - 1):
      for i in range(m):
        for j in range(n):
          adj = get_adjacents(i,j)
          if len(adj) != 0:
            solver.add_clause([-V(i,j,t)] + [V(ni,nj,t+1) for ni,nj in adj])

    # Configure rule: at time t, only one cell must be true
    for t in range(path_len):
      solver.add_clause([V(i,j,t) for i in range(m) for j in range(n)])
      AC = [V(i,j,t) for i in range(m) for j in range(n)]
      for a in range(m*n-1):
        for b in range(a+1, m*n):
          solver.add_clause([-AC[a], -AC[b]])

    # Configure rule: at each cell (i,j), it can be true for at most one time t
    for i in range(m):
      for j in range(n):
        for t1 in range(path_len-1):
          for t2 in range(t1+1, path_len):
            solver.add_clause([-V(i,j,t1), -V(i,j,t2)])

    # Contraint number setup
    memo = {}
    def C(i: int, j: int):
      global max_lit
      if (i,j) in memo: return memo[(i,j)]
      max_lit += 1
      memo[(i,j)] = max_lit
      return memo[(i,j)]

    for i in range(m):
      for j in range(n):
        cur_cell = [V(i,j,t) for t in range(path_len)]
        solver.add_clause([-C(i,j), *cur_cell])
        solver.append_formula([[C(i,j), -x] for x in cur_cell])

    # Configure constraint row
    for i in range(m):
      if cr[i] != -1:
        row_vars = [C(i,j) for j in range(n)]
        constraint_row = equals(lits=row_vars, bound=cr[i])
        solver.append_formula(constraint_row)

    # Configure constraint col
    for j in range(n):
      if cc[j] != -1:
        col_vars = [C(i,j) for i in range(m)]
        constraint_col = equals(lits=col_vars, bound=cc[j])
        solver.append_formula(constraint_col)

    # Running the SAT solver
    sat = solver.solve()

    if sat:
      solution = solver.get_model()
      def var_is_true(x):
        l, r = 0, len(solution) - 1
        while l <= r:
          mid = (l+r)//2
          if abs(solution[mid]) == x:
            return solution[mid] > 0
          elif abs(solution[mid]) > x:
            r = mid - 1
          else:
            l = mid + 1
        assert(False)
      # Get path
      path = []
      for t in range(path_len):
        for i, j in itertools.product(range(m), range(n)):
          if var_is_true(V(i,j,t)):
            path.append((i,j))
            break
      # Draw grid
      grid = [['.' for _ in range(n)] for _ in range(m)]
      grid[finish_x][finish_y] = 'u'
      for i in range(len(path) - 1):
        for d, delta in move.items():
          adj_x, adj_y = path[i][0]+delta[0], path[i][1] + delta[1]
          if path[i+1] == (adj_x,adj_y):
            grid[path[i][0]][path[i][1]] = d
      # Return 
      found = True; 
      return {'found': found, 'grid': grid}
      break

  if not found:
    return {'found': found, 'grid': []}