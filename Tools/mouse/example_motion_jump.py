from trace_examples import trace_selenium_jump
from robot_mouse_track.mouse_track import MouseTrack
from robot_mouse_track.risk_motion.motion_jump import JumpMotion

if __name__ == '__main__':
    mouse_track = MouseTrack(trace_selenium_jump)
    mouse_track.show_track()
    rule_mouse_jump = JumpMotion(th_velocity=20, th_acceleration=1.4)
    flag, (exceed_times_velocity, exceed_times_acceleration) = rule_mouse_jump.judge_risk(mouse_track)
    print(flag,exceed_times_velocity,exceed_times_acceleration)

