make_line('line')

ob = OBJET2()
ob.set(BORO=ke_to_rigidity(10e6, ELECTRON_MASS))
ob.add(Y=0, T=0.1, D=1)
add(ob)

#test values
tv = [x+0.1234567890123456789 for x in xrange(1,10)]

q1 = QUADRUPO(XL=tv[0], R_0=tv[1],B_0=tv[2],  XPAS=(10,20,10))
add(q1)
add(END())

output_lines =  output().split('\n')
quad_line = [a.strip() for a in output_lines].index("'QUADRUPO'")
bits = output_lines[quad_line + 2].split()

for x in xrange(3):
	error = tv[x]- float(bits[x])
	print repr(tv[x]), bits[x], error
	if error > 1e-12:
		print "value does not match to 12 decimals"
		raise ValueError, "error to big: %s"  % error


run()

res_lines = res().split('\n')


# find QUADRUPO output in res file
for n, l in enumerate(res_lines[quad_line+1:]):
	if "QUADRUPO" in l:
		#print l
		#print n
		quad_line = n+quad_line+1
		break

#print '\n'.join(res_lines[quad_line: quad_line+10])
for x in xrange(3):
	#print res_lines[quad_line+x+3].split()[-2]

	error = tv[x]- float(res_lines[quad_line+x+3].split()[-2])
	print repr(tv[x]), res_lines[quad_line+x+3].split()[-2], error
	if error > 1e-3:
		print "value does not match to 3 decimals"
		raise ValueError, "error to big: %s"  % error


