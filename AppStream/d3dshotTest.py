import d3dshot
import time

d = d3dshot.create(capture_output="numpy")

d.display = d.displays[0]

print (d.display)

d.capture()
time.sleep(3)  # Capture is non-blocking so we wait explicitely
d.stop()

frame_stack = d.get_frame_stack((0, 1, 2, 3), stack_dimension="last")
frame_stack.shape
frame_stack.
print(frame_stack.shape)