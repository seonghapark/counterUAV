import matplotlib.pyplot as plt

plt.style.use('ggplot')

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.titlesize'] = 13

f = open('C://Users//승윤//Desktop//purdue//연구자료//extractwav//sec_try.txt','r')

lines = f.readlines()
print(len(lines))

cost_history = []
accuracy_history = []
for line in lines:
    if 'Epoch: ' in line:
        #print(line.split('= ')[1].split('Test')[0], line.split('Test accuracy: ')[1])\
        cost_history.append(float(line.split('=')[1].split('Test')[0]))
        accuracy_history.append(float(line.split('Test accuracy: ')[1]))

fig = plt.figure(figsize=(10,8))
plt.plot(cost_history)
plt.ylabel("Cost")
plt.xlabel("Iterations")
plt.axis([0, len(cost_history), 0, max(cost_history)])
plt.show()

fig = plt.figure(figsize=(10,8))
plt.plot(accuracy_history)
plt.ylabel("Accucary")
plt.xlabel("Iterations")
plt.axis([0, len(accuracy_history), 0, max(accuracy_history)])
plt.show()

print(min(cost_history))

print(max(accuracy_history))







