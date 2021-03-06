﻿
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 50
explore_faction = 2.

def traverse_nodes(node, state):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        state:      The state of the game.

    Returns:        A node from which the next stage of the search can proceed.

    """
    while not state.is_terminal:
 #       if state.getGap[1] > state.y:
 #           if node.untried_action
  #          node.untried_action.remove(False)
        if node.untried_actions != []:
            return expand_leaf(node, state)
        else:
            me = list(node.child_nodes.values())
            node = max(me, key = lambda c: c.wins/c.visits + explore_faction*sqrt(2*log(c.parent.visits)/c.visits))
            state.apply_move(node.parent_action)
    return node


def expand_leaf(node, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        state:  The state of the game.

    Returns:    The added child node.

    """
    move = choice(node.untried_actions)
    state.apply_move(move) 
    new_node = MCTSNode(parent=node, parent_action=move, action_list=state.legal_moves)
    node.child_nodes[move] = new_node
    node.untried_actions.remove(move)
    return new_node


def rollout(state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        state:  The state of the game.
	"""
    while not state.is_terminal:
        m = choice(state.legal_moves)
        # over the gap
        #if state.getGap[1] > state.y:
        #   state.apply_move(False)
		# below the gap
       # elif state.getGap[2] < state.y:
            #state.apply_move(True)
        #else:
        state.apply_move(m)

def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node != None:
        node.visits += 1
        node.wins += won
        node = node.parent


def think(state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    root_node = MCTSNode(parent=None, parent_action=None, action_list=state.legal_moves)

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state.copy()

        # Start at root
        node = root_node

        # Traverse
        node = traverse_nodes(node, sampled_game)

        # rollout
        rollout(sampled_game)

        # backpropagate
        backpropagate(node, sampled_game.winner)

    # estimated win rate.
    list_child = list(root_node.child_nodes.values())
    best_child = max(list_child, key = lambda c: c.wins/c.visits)

    #if best_child.wins / best_child.visits == -100 and len(root_node.action_list) == 1 and root_node.action_list[0] == False:
    #   return True;
    """
    sorted_children = sorted(list_child, key = lambda c: c.wins/c.visits)
    if len(list_child) == 2 and sorted_children[1].wins / sorted_children[1].visits > -0.75:
        print (sorted_children[1].wins / sorted_children[1].visits)
        return choice([True, False])
    
    numWinners = None
    for i in range (len(sorted_children)):
        if sorted_children[i].wins == -1:
            numWinners = i - 1
            break
    if numWinners == -1:
        return sorted_children[0].parent_action
    else:
        return sorted_children[0].parent_action
    """
    return best_child.parent_action
