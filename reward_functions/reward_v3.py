def reward_function(params):
    # 1. Pull only the allowed parameters
    all_on_track      = params['all_wheels_on_track']
    dist_center       = params['distance_from_center']
    track_width       = params['track_width']
    speed             = params['speed']
    steering          = abs(params['steering_angle'])
    progress          = params['progress']
    is_offtrack       = params['is_offtrack']
    is_crashed        = params['is_crashed']
    waypoints         = params['waypoints']
    closest_wp        = params['closest_waypoints']

    # 2. Immediate failure check
    if is_offtrack or is_crashed:
        return float(1e-3)

    # 3. Base reward: how centred are we?
    #    Normalized to [0,1], where 1 = perfectly on centre line.
    reward = max(0.0, (0.5*track_width - dist_center) / (0.5*track_width))

    # 4. Speed bonus (only if we’re reasonably centred)
    if dist_center < 0.15 * track_width:
        # scale speed (0.5–1 m/s) into a [0,0.5] bonus
        reward += (speed - 0.5) / (1.0 - 0.5) * 0.5

    # 5. Steering penalty: discourage >15°  
    if steering > 15:
        reward *= 0.7

    # 6. Progress incentive: small nudge (max +0.1)  
    reward += (progress / 100.0) * 0.1

    # 7. Always return a float
    return float(reward)
