import time


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)
        return

    def pop(self):
        item = self.items[len(self.items) - 1]
        del self.items[-1]
        return item

    def top(self):
        return self.items[-1]

    def size(self):
        return len(self.items)


class State:
    def __init__(self, snake_loc, seeds_scores):
        self.snake_body_loc = snake_loc
        self.seeds_score = seeds_scores

    def __eq__(self, other):
        return self.snake_body_loc == other.snake_body_loc and self.seeds_score == other.seeds_score

    def __hash__(self):
        seeds_tuple = tuple(self.seeds_score)
        snake_loc_tuple = tuple(self.snake_body_loc)
        return hash((snake_loc_tuple, seeds_tuple))

    def hits_itself(self, snake_new_head, on_seed):
        if len(self.snake_body_loc) == 1:
            return False
        elif len(self.snake_body_loc) == 2:
            tail = self.snake_body_loc[1]
            head = self.snake_body_loc[0]
            if snake_new_head == tail:
                if not on_seed:
                    if (height == 2 and head[1] == tail[1]) or (width == 2 and head[0] == tail[0]):
                        return False
                    else:
                        return True
                else:
                    return True

        else:
            for i in range(len(self.snake_body_loc) - 1):
                if self.snake_body_loc[i] == snake_new_head:
                    return True
        return False

    def is_on_seed(self):
        snake_head = self.snake_body_loc[0]
        for i in range(len(self.seeds_score)):
            if seeds_loc_list[i] == snake_head and self.seeds_score[i] > 0:
                return i, True

        return -1, False


def add_if_exists(new_node):
    if new_node is not None:
        ids_stack.push(new_node)
        nodes_list.append(new_node)


class Node:
    def __init__(self, parent_id, new_state, direction, depth):
        self.id = len(nodes_list)
        self.parent_id = parent_id
        self.state = new_state
        self.direction = direction
        self.depth = depth

    def expand(self, set_of_states, depth_limit):
        if self.depth >= depth_limit:
            return False

        snake_head_loc = self.state.snake_body_loc[0]
        right_side_node = self.move("R", (snake_head_loc[0] % height, (snake_head_loc[1] + 1) % width), set_of_states)
        add_if_exists(right_side_node)
        bottom_node = self.move("D", ((snake_head_loc[0] + 1) % height, snake_head_loc[1] % width), set_of_states)
        add_if_exists(bottom_node)
        left_side_node = self.move("L", (snake_head_loc[0] % height, (snake_head_loc[1] - 1) % width), set_of_states)
        add_if_exists(left_side_node)
        upper_node = self.move("U", ((snake_head_loc[0] - 1) % height, snake_head_loc[1] % width), set_of_states)
        add_if_exists(upper_node)

    def move(self, direction, snake_new_head, set_of_states):
        index, on_seed = self.state.is_on_seed()
        if self.state.hits_itself(snake_new_head, on_seed):
            return None
        new_snake_loc, new_seeds_score = self.move_snake(index, on_seed, snake_new_head)
        return self.create_new_node(new_snake_loc, new_seeds_score, direction, set_of_states)

    def move_snake(self, index, on_seed, new_head):
        new_seed_scores = self.state.seeds_score.copy()
        new_snake_loc = self.state.snake_body_loc.copy()
        new_snake_loc.insert(0, new_head)

        if on_seed and self.id != 0:
            new_seed_scores[index] -= 1
        if not on_seed:
            del new_snake_loc[-1]

        return new_snake_loc, new_seed_scores

    def create_new_node(self, new_snake_loc, new_seeds_score, direction, set_of_states):
        global duplicate_states
        new_state = State(new_snake_loc, new_seeds_score)
        hashed_new_state = hash(new_state)
        if hashed_new_state in set_of_states:
            duplicate_states += 1
            if hash_key_depth[hashed_new_state] <= self.depth + 1:
                return None
        else:
            set_of_states.add(hashed_new_state)

        hash_key_depth[hashed_new_state] = self.depth + 1
        new_node = Node(self.id, new_state, direction, self.depth + 1)
        return new_node

    def is_goal_state(self):
        last_seed_index = -1
        for i in range(len(self.state.seeds_score)):
            if self.state.seeds_score[i] != 0:
                if self.state.seeds_score[i] == 1:
                    if last_seed_index != -1:
                        return False
                    else:
                        last_seed_index = i
                else:
                    return False

        if seeds_loc_list[last_seed_index] == self.state.snake_body_loc[0]:
            return True
        else:
            return False


def get_seeds_info():
    seed_cnt = int(input())
    locations = []
    scores = []
    for i in range(seed_cnt):
        seed = input().split(",")
        scores.append(int(seed[2]))
        locations.append((int(seed[0]), int(seed[1])))

    return locations, scores


def get_location():
    line = input().split(",")
    given_height = int(line[0])
    given_width = int(line[1])
    return given_height, given_width


def print_solution(goal_node, depth_limit, visited_states):
    reverse_path = ""
    node = goal_node
    while node is not None:
        if node.parent_id is None:
            node = None
        else:
            reverse_path += node.direction
            node = nodes_list[node.parent_id]

    print("Completed in ", depth_limit, " moves!")
    print("Path to goal: ", reverse_path[::-1])
    print("Number of visited states: ", visited_states)
    print("Number of unique states: ", len(hash_key_depth))


def create_first_node():
    init_state = State([(snake_init_height, snake_init_width)], seeds_score)
    hashed_init_state = hash(init_state)
    hash_key_depth[hashed_init_state] = 0
    first_node = Node(None, init_state, None, 0)
    nodes_list.append(first_node)
    return first_node, hashed_init_state


def start_ids():
    global duplicate_states
    first_node, hashed_init_state = create_first_node()
    ids_stack.push(first_node)
    set_of_states = set()
    set_of_states.add(hashed_init_state)
    depth_limit = 1
    visited_states = 0
    while not ids_stack.top().is_goal_state():
        expanding_node = ids_stack.pop()
        if expanding_node.depth <= depth_limit:
            expanding_node.expand(set_of_states, depth_limit)

        if ids_stack.size() == 0:
            visited_states += duplicate_states + len(nodes_list)
            duplicate_states = 0
            set_of_states = set()
            set_of_states.add(hashed_init_state)
            ids_stack.push(first_node)
            hash_key_depth.clear()
            nodes_list.clear()
            hash_key_depth[hashed_init_state] = 0
            nodes_list.append(first_node)
            depth_limit += 1

    print_solution(ids_stack.top(), depth_limit, visited_states)


# main
height, width = get_location()
snake_init_height, snake_init_width = get_location()
nodes_list = []
hash_key_depth = {}
duplicate_states = 0
ids_stack = Stack()
seeds_loc_list, seeds_score = get_seeds_info()
start = time.time()
start_ids()
finish = time.time()
print("IDS finished in : %f milli-seconds" % ((finish - start) * 1000))
