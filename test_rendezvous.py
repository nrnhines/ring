from neuron import h
pc = h.ParallelContext()
rank = int(pc.id())
nhost = int(pc.nhost())

N = 10

have = {}
for i in range(rank, N, nhost):
  ran = h.Random()
  ran.Random123(i)
  ran.discunif(0,5)

  rval = ran.repick()
  if not have.has_key(rval):
    have[rval] = []
  have[rval].append(i)

for r in range(nhost):
  if (r == rank):
    print ('\n%d has' % r)
    for rval, item in have.items():
      print rval, item
  pc.barrier()

want = {}
for _ in range(5):
  rval = ran.repick()
  want[rval] = []

for r in range(nhost):
  if r == rank:
    print('\n%d want' %r)
    print want.keys()
  pc.barrier()

###############################

#fill in the values of each want[rval] with the
#values of i of the have dictionaries.

#Solution: A rendezvous rank function:
def rendezvous(x):
  return hash(x)%nhost

#1) Everyone sends the keys they own to the rendezvous rank.
src = [None]*nhost
for key in have:
  r = rendezvous(key)
  if src[r] == None:
    src[r] = []
  src[r].append(key)

dest = pc.py_alltoall(src)

rendezvous_have = {} # {rval:[haveranks]}
for r, item in enumerate(dest):
  if item != None:
    for rval in item:
      if rval not in rendezvous_have:
        rendezvous_have[rval] = []
      rendezvous_have[rval].append(r)

#2) Everyone sends the keys they want to the rendezvous rank.
src = [None]*nhost
for key in want:
  r = rendezvous(key)
  if src[r] == None:
    src[r] = []
  src[r].append(key)

dest = pc.py_alltoall(src)
rendezvous_want = {} # {rval:[wantranks]}
for r, item in enumerate(dest):
  if item != None:
    for rval in item:
      if rval not in rendezvous_want:
        rendezvous_want[rval] = []
      rendezvous_want[rval].append(r)

#3) The rendezvous rank sends back to the owners,which ranks want which keys.
src = [None]*nhost
for have_rval, item in rendezvous_have.items():
  if have_rval in rendezvous_want:
    ranks_that_want = rendezvous_want[have_rval]
    for have_rank in item:
      if src[have_rank] == None:
        src[have_rank] = []
      src[have_rank].append((have_rval,ranks_that_want))

dest = pc.py_alltoall(src)
#[[(rval,wantranks)]]

#4) The owners send the objects to the ranks that want them.
src = [None]*nhost
for lst in dest:
  if lst != None:
    for rval,wantranks in lst:
      assert(rval in have)
      for r in wantranks:
        if src[r] == None:
          src[r] = []
        for i in have[rval]:
          src[r].append((rval, i))

dest = pc.py_alltoall(src)
#[[(rval,i)]]

for lst in dest:
  if lst != None:
    for rval, i in lst:
      want[rval].append(i)

########
for r in range(nhost):
  if r == rank:
    print("\n%d want"%r)
    for rval, vals in want.items():
      print (rval, vals)
  pc.barrier()

h.quit()
