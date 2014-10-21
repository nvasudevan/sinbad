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
            ambi_parse = AmbiParse.parse(self, acc_out)
            mincfg = ambi_parse.min_cfg()
            amb_subset = ambi_parse.ambiguous_subset()
            new_gp = os.path.join(td,"%s.acc" % str(n))
            self.write_cfg(mincfg, new_gp)
            self.print_stats(currgp, sen, is_amb, amb_subset)
            currgp = new_gp
            n += 1

#        if os.path.exists(td):
#            shutil.rmtree(td)

