from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

from trace_examples import trace_itmorn, trace_answer_unlock
from robot_mouse_track.mouse_track import MouseTrack
from robot_mouse_track.risk_motion.motion_jump import JumpMotion
from robot_mouse_track.risk_motion.motion_vertical_horizontal_linear import VerticalHorizontalLinearMotion
from robot_mouse_track.risk_motion.motion_linear import LinearMotion
from robot_mouse_track.risk_motion.motion_constant_velocity import ConstantVelocityMotion
from robot_mouse_track.risk_motion.motion_slow import SlowMotion
from robot_mouse_track.risk_motion.motion_similar import SimilarMotion, calc_vec

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 设置跨域


@app.route("/predict", methods=["POST"])
def index():
    trace = request.get_json()
    print(trace)
    mouse_track = MouseTrack(trace)
    mouse_track.show_track()
    lst_res = []
    rule_mouse_jump = JumpMotion(th_velocity=20, th_acceleration=1.4)
    flag, (exceed_times_velocity, exceed_times_acceleration) = rule_mouse_jump.judge_risk(mouse_track)
    print(flag, "JumpMotion", exceed_times_velocity, exceed_times_acceleration)
    lst_res.append([flag, "JumpMotion", exceed_times_velocity, exceed_times_acceleration])

    rule_mouse_jump = VerticalHorizontalLinearMotion()
    flag, (exceed_times_x, exceed_times_y) = rule_mouse_jump.judge_risk(mouse_track)
    print(flag, "VerticalHorizontalLinearMotion", exceed_times_x, exceed_times_y)
    lst_res.append([flag, "VerticalHorizontalLinearMotion", exceed_times_x, exceed_times_y])

    rule_mouse_jump = LinearMotion()
    flag, exceed_times = rule_mouse_jump.judge_risk(mouse_track)
    print(flag, "LinearMotion", exceed_times)
    lst_res.append([flag, "LinearMotion", exceed_times])

    rule_mouse_jump = ConstantVelocityMotion()
    flag, exceed_times = rule_mouse_jump.judge_risk(mouse_track)
    print(flag, "ConstantVelocityMotion", exceed_times)
    lst_res.append([flag, "ConstantVelocityMotion", exceed_times])

    rule_mouse = SlowMotion()
    flag, exceed_times = rule_mouse.judge_risk(mouse_track)
    print(flag, "SlowMotion", exceed_times)
    lst_res.append([flag, "SlowMotion", exceed_times])

    lst_vec_bank = []
    mouse_track1 = MouseTrack(trace_itmorn)
    vec1 = calc_vec(mouse_track1)
    lst_vec_bank.append(vec1)

    mouse_track2 = MouseTrack(trace_answer_unlock)
    vec_now = calc_vec(mouse_track2)

    rule_mouse = SimilarMotion()
    flag, exceed_times = rule_mouse.judge_risk(vec=vec_now, lst_vec_bank=lst_vec_bank)
    print(flag, "SimilarMotion", exceed_times)
    lst_res.append([flag, "SimilarMotion", exceed_times])

    return jsonify(lst_res)


if __name__ == '__main__':
    app.run()