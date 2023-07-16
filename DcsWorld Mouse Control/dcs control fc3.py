# this script match fc3 best
# vjoy z axis haven't been actived yet
import ctypes

class vjoyAxis():
	def __init__(self, x, y, z, th_l, th_r):
		self.x, self.y, self.z = x, y, z
		self.th_l, self.th_r = th_l, th_r
		
class modeState():
	def __init__(self, stick, throttle, mouselock, vjoy_botton):
		self.stick = stick
		self.th = throttle
		self.mouselock = mouselock
		self.btn = vjoy_botton

class sensitive():
	def __init__(self, mou, x, y, th):
		self.mou = mou
		self.x, self.y = x, y
		self.th = th


def check_overflow(a, min, max):
	if a < min:
		a = min
	elif a > max:
		a = max

def wheel_th(sens_mo, sens_th):
	res = 0
	if mouse.wheelUp:
		res += 20*sens_mo*sens_th
	if mouse.wheelDown:
		res -= 20*sens_mo*sens_th
	
	return res


if starting:
	# set max and min value
	axis_max = vJoy[0].axisMax
	axis_min = -vJoy[0].axisMax
	
	# set axis center value
	center_axis_x = 0
	center_axis_y = 0
	
	Axis = vjoyAxis(0, 0, 0, axis_min, axis_min)
	IsActive = modeState(False, False, False, False)
	Sens = sensitive(15.0, 0.7, 0.9, 1.9)


# hold mouse2 to active vjoy stick
control_active = mouse.getButton(1)
# throttle modifier
throttle_both = keyboard.getKeyDown(Key.RightShift)
throttle_left = keyboard.getKeyDown(Key.RightAlt)
throttle_right = keyboard.getKeyDown(Key.RightControl)


# check whether vjoy stick is enabled
if control_active :
	IsActive.stick = True
	IsActive.th = True
	IsActive.mouselock = True
	IsActive.btn = True

else:
	IsActive.stick = False
	IsActive.th = False
	IsActive.mouselock = False
	IsActive.btn = False
	
	if Axis.x != center_axis_y :
		Axis.x = 0
	if Axis.y != center_axis_y :
		Axis.y = 0


# stick
if IsActive.stick :
	Axis.x += mouse.deltaX*Sens.x*Sens.mou*0.48
	Axis.y += mouse.deltaY*Sens.y*Sens.mou

# throttle
if IsActive.th :
	"""
	if mouse.wheelUp :
		keyboard.setKeyDown(Key.NumberPadPlus)
	elif mouse.wheelDown :
		keyboard.setKeyDown(Key.NumberPadMinus)
	"""
	if throttle_both:
		if Axis.th_l > Axis.th_r :
			Axis.th_r = Axis.th_l
		else:
			Axis.th_l = Axis.th_r
		Axis.th_l += wheel_th(Sens.mou, Sens.th)
		Axis.th_r += wheel_th(Sens.mou, Sens.th)
	if throttle_left:
		Axis.th_l += wheel_th(Sens.mou, Sens.th)
	if throttle_right:
		Axis.th_r += wheel_th(Sens.mou, Sens.th)
	

# vjoy botton
if IsActive.btn :
	# note: botton number begin with 0
	vJoy[0].setButton(8, mouse.getPressed(2))

# lock mouse
if IsActive.mouselock :
	# set x and y value to fit your own screen
	ctypes.windll.user32.SetCursorPos(960,600)  # lock mouse at the center of screen


# axis value overflow protection
check_overflow(Axis.x, axis_min, axis_max)
check_overflow(Axis.y, axis_min, axis_max)
check_overflow(Axis.th_l, axis_min, axis_max)
check_overflow(Axis.th_r, axis_min, axis_max)


# map axis to vjoy
vJoy[0].x = int(round(Axis.x))
vJoy[0].y = Axis.y
vJoy[0].slider = Axis.th_l
vJoy[0].dial = Axis.th_r


# for debug
# diagnostics.watch(vJoy[0].x)
# diagnostics.watch(vJoy[0].y)
# diagnostics.watch(vJoy[0].slider)
# diagnostics.watch(vJoy[0].dial)
