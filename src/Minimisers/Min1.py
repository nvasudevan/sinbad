import os, tempfile, shutil
import Minimiser, AmbiParse
import Utils


class Min1(Minimiser.Minimiser):

    def __init__(self, ambimin):
        Minimiser.Minimiser.__init__(self, ambimin)


    def minimise(self):
        td = tempfile.mkdtemp()
        n = 1
        currgp = self.ambimin.gf
        while n <= self.ambimin.mincnt: 
            print "[%s]currgp: %s" % (str(n),currgp)
            is_amb, sen, acc_out = self.find_ambiguity(currgp, self.ambimin.lf, None)
            assert is_amb
            mincfg = AmbiParse.parse(acc_out) 
            new_gp = os.path.join(td,"%s.acc" % str(n))
            self.write_cfg(mincfg, new_gp)
            Utils.print_stats(currgp, self.ambimin.lf, sen, is_amb)
            currgp = new_gp
            n += 1

#        if os.path.exists(td):
#            shutil.rmtree(td)

