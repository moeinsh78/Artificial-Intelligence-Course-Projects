import time


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

    def calc_heuristic(self):
        return 4.8 * sum(self.seeds_score)

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


def add_to_queue(new_node):
    key = new_node.cost + new_node.heuristic_cost
    i = 0
    if len(a_star_queue) > 0:
        while True:
            if key < a_star_queue[i].cost + a_star_queue[i].heuristic_cost:
                i += 1
            else:
                break
            if i == len(a_star_queue):
                break

    a_star_queue.insert(i, new_node)
    return


def check_if_goal(new_node):
    if new_node is not None:
        if new_node.is_goal_state():
            return True
        else:
            nodes_list.append(new_node)
            add_to_queue(new_node)
            # a_star_queue.append(new_node)
            # a_star_queue.sort(key=lambda i: i.cost + i.heuristic_cost, reverse=True)
            return False


class Node:
    def __init__(self, parent_id, new_state, direction, cost):
        self.id = len(nodes_list)
        self.parent_id = parent_id
        self.state = new_state
        self.direction = direction
        self.cost = cost
        self.heuristic_cost = new_state.calc_heuristic()

    def expand(self):
        snake_head_loc = self.state.snake_body_loc[0]
        right_side_node = self.move("R", (snake_head_loc[0] % height, (snake_head_loc[1] + 1) % width))
        if check_if_goal(right_side_node):
            return right_side_node
        bottom_node = self.move("D", ((snake_head_loc[0] + 1) % height, snake_head_loc[1] % width))
        if check_if_goal(bottom_node):
            return bottom_node
        left_side_node = self.move("L", (snake_head_loc[0] % height, (snake_head_loc[1] - 1) % width))
        if check_if_goal(left_side_node):
            return left_side_node
        upper_node = self.move("U", ((snake_head_loc[0] - 1) % height, snake_head_loc[1] % width))
        if check_if_goal(upper_node):
            return upper_node

        return None

    def move(self, direction, snake_new_head):
        index, on_seed = self.state.is_on_seed()
        if self.state.hits_itself(snake_new_head, on_seed):
            return None
        new_snake_loc, new_seeds_score = self.move_snake(index, on_seed, snake_new_head)
        return self.create_new_node(new_snake_loc, new_seeds_score, direction)

    def move_snake(self, index, on_seed, new_head):
        new_seed_scores = self.state.seeds_score.copy()
        new_snake_loc = self.state.snake_body_loc.copy()
        new_snake_loc.insert(0, new_head)

        if on_seed and self.id != 0:
            new_seed_scores[index] -= 1
        if not on_seed:
            del new_snake_loc[-1]

        return new_snake_loc, new_seed_scores

    def create_new_node(self, new_snake_loc, new_seeds_score, direction):
        global duplicate_states
        new_state = State(new_snake_loc, new_seeds_score)
        hashed_new_state = hash(new_state)
        if hashed_new_state in set_of_states:
            duplicate_states += 1
            return None
        else:
            set_of_states.add(hashed_new_state)
            new_node = Node(self.id, new_state, direction, self.cost + 1)
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


def print_result(goal_node):
    reverse_path = ""
    node = goal_node
    while node is not None:
        if node.parent_id is None:
            node = None
        else:
            reverse_path += node.direction
            node = nodes_list[node.parent_id]

    print("Completed in ", len(reverse_path), " moves!")
    print("Path to goal: ", reverse_path[::-1])
    print("Number of states: ", len(nodes_list) + duplicate_states)
    print("Number of unique states: ", len(set_of_states) + 1)


def start_a_star():
    init_state = State([(snake_init_height, snake_init_width)], seeds_score)
    first_node = Node(None, init_state, None, 0)
    nodes_list.append(first_node)
    a_star_queue.append(first_node)
    goal_node = None
    while goal_node is None:
        expanding_node = a_star_queue.pop(-1)
        goal_node = expanding_node.expand()

    print_result(goal_node)


# main
height, width = get_location()
snake_init_height, snake_init_width = get_location()
nodes_list = []
a_star_queue = []
set_of_states = set()
duplicate_states = 0
seeds_loc_list, seeds_score = get_seeds_info()
start = time.time()
start_a_star()
finish = time.time()
print("Weighted A-Star finished in : %f milli-seconds" % ((finish - start) * 1000))
