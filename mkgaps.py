from neuron import h
pc = new ParallelContext()

#gap info is in the form of
#(sid1, gid1, "sec1", x1,    sid2, gid2, "sec2", x2,  g)

gaps = [] # [(sidhg, sidv, halfgap)]

def mkgap(sid1, gid1, "sec1", x1,  sid2, gid2, "sec2", x2):
  if pc.gid_exists(sid1):
    mkhalfgap(sid1, gid1, "sec1", x1, sid2, g)
  if pc.gid_exists(sid2):
    mkhalfgap(sid2, gid2, "sec2", x2, sid1, g)

def mkhalfgap(sidhg, gid, secname, x, sidv, g):
  cell = pc.gid2cell(gid)
  sec = cell.__getattr__(secname)

  hg = h.HalfGap(sec(x))
  hg.g = g
  pc.source_var(seg._ref_v, sidv, sec=sec)
  pc.target_var(hg, hg._ref_vgap, sidhg)
  gaps.append((sidhg, sidv, hg)) # keep in existance
