def track_reward(reward, saved_rewards):
    """
    Count the number of rewards / penalties
    @param reward: reward for last action
    @param saved_rewards: tupel of previous received rewards
    """
    saved_rewards = list(saved_rewards)
    if reward == -10:
        saved_rewards[0] += 1
    if reward == -110:
        saved_rewards[1] += 1
    if reward == -510:
        saved_rewards[2] += 1
    return tuple(saved_rewards)


def log_rewards(writer, saved_rewards, episode_reward, episode):
    """
    Log rewards for tensorboard
    @param writer: writer to write to into logs
    @param saved_rewards: Tuple with penalties (path, pick-up, illegal-move)
    @param episode_reward: reward for the current episode
    @param episode: current number of episode
    """
    writer.add_scalar('Path Penalty', saved_rewards[0], episode)
    writer.add_scalar('Illegal Pick-up / Drop-off', saved_rewards[1], episode)
    writer.add_scalar('Illegal Move', saved_rewards[2], episode)
    writer.add_scalar('Reward', episode_reward, episode)