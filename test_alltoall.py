from neuron import h
pc = h.ParallelContext()
rank = int(pc.id())
nhost = int(pc.nhost())

srcdata = [(1000+rank, 100*d + rank) for d in range(nhost)]

if rank == 0: print ('\nsrcdata')
for r in range(nhost):
  if r == rank:
    print (r, srcdata)
  pc.barrier()

destdata = pc.py_alltoall(srcdata)

if rank == 0: print ('\ndestdata')
for r in range(nhost):
  if r == rank:
    print (r, destdata)
  pc.barrier()

h.quit()


