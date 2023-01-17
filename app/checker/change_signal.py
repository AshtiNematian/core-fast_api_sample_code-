

def check_signal_changed(two_latest_actions):
    if len(two_latest_actions) != 2:
        return 0
    stale_action = two_latest_actions[-1]['action_df'][-1]['action']
    new_action = two_latest_actions[-2]['action_df'][-1]['action']
    if new_action != stale_action:
        return two_latest_actions[-2]['action_df'][-1]
    else:
        return 0