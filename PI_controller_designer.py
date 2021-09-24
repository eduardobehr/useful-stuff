#! python3
import control as ct
from numpy import pi, tan, angle, abs, log10, sqrt
from matplotlib import pyplot as plt
s=ct.tf([1,0], [1])
G=10/(1+s)

mfnc = ct.margin(G)[1]
wcnc = ct.margin(G)[3]

print(f'{mfnc = :.3}; {wcnc = :.3}')

wcc = 1 # frequência de corte desejada (compensada)
mfc = 60 # margem de fase desejada (em graus)
'''
wz = Ki/Kp

abs(GC) = 1
Kp*sqrt(w0c**2+wz**2)/w0c*abs(G)=1

<(CG)=-180°
 atan(w0c/wz) - 90° + <(G) = -180
 wz = w0c/tan(- <G - 90°)
'''

Gwcc = ct.evalfr(G, 1j*(wcc))
angGc = ct.np.angle(Gwcc) # fase do G na freq. de corte desejada
angGc_deg = angGc*180/ct.np.pi

absGc = ct.np.abs(Gwcc)
magGc_dB = 20*ct.np.log10(absGc)

wz = abs(wcc/tan((-mfc + angGc_deg -90)*pi/180))
Kp = wcc/(sqrt(wcc**2+wz**2)*absGc)

print(f"{angGc_deg =  :.3}°, {absGc = :.4} ({magGc_dB:.4} dB)")
print(f"{wz = :.4}, {Kp = :.4}")

C = Kp*(s+wz)/s

CG = C*G

mfc_final = ct.margin(CG)[1]
wc_final = ct.margin(CG)[3]
print(f'{mfc_final = :.4}; {wc_final = :.4}')

if 1:
	central_freq = sqrt(wcnc*wcc)
	
	
	ct.bode_plot(G, dB=True)
	ct.bode_plot(C, dB=True)
	ct.bode_plot(CG, dB=True)
	plt.legend(["G", "C", "CG"])
	plt.show()
