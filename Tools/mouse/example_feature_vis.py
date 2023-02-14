from trace_examples import  trace_answer_unlock
from robot_mouse_track.mouse_track import MouseTrack

import matplotlib.pyplot as plt

# if __name__ == '__main__':
mouse_track = MouseTrack(trace_answer_unlock)

# 展示鼠标轨迹
mouse_track.show_track()

# 展示合速度
feature_dev_order1, feature_dev_order2 = mouse_track.get_feature_dev(order=2, mode="combine")  # contants.COMBINE
plt.plot(mouse_track.arr_trace[:len(feature_dev_order1),-1], feature_dev_order1)
plt.xlabel("time")
plt.ylabel("px/ms")
plt.show()
#
# plt.plot(mouse_track.arr_trace[:len(feature_dev_order2),-1], feature_dev_order2)
# plt.xlabel("time")
# plt.ylabel("px/ms^2")
# plt.show()

# 展示分速度
# feature_dev_order1, feature_dev_order2 = mouse_track.get_feature_dev(order=2, mode="decomposition") # contants.COMBINE
# plt.plot(mouse_track.arr_trace[:len(feature_dev_order1), -1], feature_dev_order1[:, 0])
# plt.xlabel("time")
# plt.ylabel("x-axis px/ms")
# plt.show()

feature_doa = mouse_track.get_feature_doa()
plt.plot(mouse_track.arr_trace[:len(feature_doa), -1], feature_doa)
plt.xlabel("time")
plt.ylabel("angle")
plt.show()
