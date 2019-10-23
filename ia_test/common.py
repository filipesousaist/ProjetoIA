import copy

# Sample used for both inputs and ouputs
class Sample:
	init = None
	goal = None
	tickets = None
	limit_exp = None
	limit_depth = None
	path = None
	any_order = None
	time = None

# Validation logic
def validate_path(model, sample):
	if not sample.path:
		return "path is empty"

	# Copy everything
	tickets = list(sample.tickets)
	init = list(sample.init)
	goal = list(sample.goal)

	if sample.path[0][1] != init:
		return "init not expected"

	if not sample.any_order and sample.path[-1][1] != goal \
			or sample.any_order and sorted(sample.path[-1][1]) != sorted(goal):
		return "goal not reached"

	path = copy.deepcopy(sample.path)
	del path[0]

	agents = len(init)

	for [tickets_used, next_states] in path:
		for agent_index in range(agents):
			next_state = next_states[agent_index]
			agent_ticket = tickets_used[agent_index]
			state = init[agent_index]
			if tickets[agent_ticket] == 0:
				return "no more tickets"
			else:
				tickets[agent_ticket] -= 1
				if [agent_ticket, next_state] in model[state]:
					init[agent_index] = next_state
				else:
					return "invalid action"

	# Validation successful
	return None